"""TacticalBot — a bot that uses tactical analysis to make decisions.

Decision logic (applied independently per owned planet each tick):

  1. Skip planets below the minimum garrison threshold — don't strip
     a planet that is already weak.

  2. Find all "affordable" targets — planets we have enough ships to
     capture with a safety buffer left over.

  3. Score each affordable target by two criteria:
       - Proximity  : closer planets are cheaper to reach (ships arrive
                      sooner and we hold the planet longer).
       - Growth     : higher-growth planets produce more ships per tick,
                      so capturing them compounds over time.
     Final score = growth_weight * growth - distance_weight * distance

  4. Attack the highest-scoring target, sending just enough ships to
     win (dest.ships + ATTACK_BUFFER) rather than everything we have.
     This leaves a garrison behind for defence.

No randomness is used — every decision is deterministic and based on
the current game state visible through the fog-of-war facade.
"""

# --- Tuning constants ---
MIN_GARRISON   = 15    # minimum ships to keep on any planet
ATTACK_BUFFER  = 5     # extra ships sent on top of what the target has
GROWTH_WEIGHT  = 40    # how much to value high-production planets
DISTANCE_WEIGHT = 1    # how much to penalise far-away planets


# Shared dict: planet_id -> target planet
# planet_wars_draw.py reads this to draw targeting lines.
tactical_targets: dict = {}


class TacticalBot(object):

    def update(self, gameinfo):
        my_planets  = list(gameinfo._my_planets().values())
        targets     = list(gameinfo._not_my_planets().values())

        if not my_planets or not targets:
            tactical_targets.clear()
            return

        tactical_targets.clear()

        for src in my_planets:
            # 1. Skip planets that are too weak to safely launch from
            if src.ships <= MIN_GARRISON:
                continue

            # 2. Find targets we can actually afford to take
            ships_available = src.ships - MIN_GARRISON
            affordable = [
                t for t in targets
                if ships_available > t.ships + ATTACK_BUFFER
            ]

            if not affordable:
                continue

            # 3. Score each affordable target
            def score(target):
                dist = src.distance_to(target, sqrt=True)
                return GROWTH_WEIGHT * target.growth - DISTANCE_WEIGHT * dist

            best = max(affordable, key=score)

            # 4. Send just enough to win, keeping the garrison behind
            ships_to_send = best.ships + ATTACK_BUFFER
            gameinfo.planet_order(src, best, ships_to_send)

            # Record decision for the visualiser
            tactical_targets[src.ID] = best
