"""FogBot — a fog-of-war aware tactical bot.

Extends TacticalBot's logic with two fog-of-war strategies:

1. Stale-data compensation
   Each planet tracked by the facade carries a ``vision_age`` counter.
   When ``vision_age == 0`` the bot can see the planet right now (fresh).
   When ``vision_age > 0`` the last observation was N ticks ago — the
   planet's ship count is outdated. FogBot adjusts its estimate upward:

     estimated_ships = last_known_ships + growth_rate × vision_age

   This prevents sending an attack fleet that is too small because the
   target grew ships while off-screen.

2. Scouting
   Once per tick, FogBot identifies the highest-priority unseen planet
   (highest growth × vision_age score) and sends a tiny scout fleet of
   SCOUT_SHIPS toward it. As the scout travels it reveals planets along
   its path, refreshing the bot's intelligence.
"""

# --- Tuning constants ---
MIN_GARRISON        = 15    # minimum ships to keep on any planet
ATTACK_BUFFER       = 5     # extra ships sent on top of estimated target ships
GROWTH_WEIGHT       = 40    # how much to value high-production planets
DISTANCE_WEIGHT     = 1     # how much to penalise far-away planets
SCOUT_SHIPS         = 3     # ships used for a scouting mission
SCOUT_AGE_THRESHOLD = 15    # only scout planets unseen for this many ticks


class FogBot(object):

    def update(self, gameinfo):
        my_planets = list(gameinfo._my_planets().values())
        all_planets = list(gameinfo.planets.values())  # includes stale entries

        if not my_planets:
            return

        # ---- Scouting (once per tick) --------------------------------
        # Find the most important planet we haven't seen recently.
        stale_targets = [
            p for p in all_planets
            if p.vision_age > SCOUT_AGE_THRESHOLD and p.owner != gameinfo.ID
        ]
        if stale_targets:
            # Score: high-growth planets that have been dark the longest
            scout_target = max(stale_targets, key=lambda p: p.growth * p.vision_age)
            # Pick the closest owned planet that can spare SCOUT_SHIPS
            scout_src = min(
                [p for p in my_planets if p.ships > MIN_GARRISON + SCOUT_SHIPS],
                key=lambda p: p.distance_to(scout_target),
                default=None,
            )
            if scout_src is not None:
                gameinfo.planet_order(scout_src, scout_target, SCOUT_SHIPS)

        # ---- Tactical attacks ----------------------------------------
        targets = [p for p in all_planets if p.owner != gameinfo.ID]

        for src in my_planets:
            # 1. Skip planets too weak to attack from
            if src.ships <= MIN_GARRISON:
                continue

            ships_available = src.ships - MIN_GARRISON

            # 2. Find affordable targets using fog-adjusted ship estimates
            affordable = []
            for t in targets:
                # Compensate for stale data: planet may have grown ships
                estimated_ships = t.ships + t.growth * t.vision_age
                if ships_available > estimated_ships + ATTACK_BUFFER:
                    affordable.append((t, estimated_ships))

            if not affordable:
                continue

            # 3. Score each affordable target (use real growth, adjusted distance)
            def score(entry):
                t, _ = entry
                dist = src.distance_to(t, sqrt=True)
                return GROWTH_WEIGHT * t.growth - DISTANCE_WEIGHT * dist

            best_target, best_estimated = max(affordable, key=score)

            # 4. Send just enough ships to win against the adjusted estimate
            ships_to_send = best_estimated + ATTACK_BUFFER
            gameinfo.planet_order(src, best_target, ships_to_send)
