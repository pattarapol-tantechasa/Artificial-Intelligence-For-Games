"""NaiveBot — a simple baseline bot with no tactical reasoning.

Each tick, for every owned planet that has enough ships, this bot picks a
random target from all non-owned planets and sends half its ships there.
It does not consider distance, enemy strength, production value, or
incoming threats — purely random target selection with a basic ship
threshold to avoid sending empty or tiny fleets.

This bot serves as the baseline control for comparison against TacticalBot.
"""

import random


class NaiveBot(object):

    def update(self, gameinfo):
        my_planets = list(gameinfo._my_planets().values())
        targets = list(gameinfo._not_my_planets().values())

        if not my_planets or not targets:
            return

        for src in my_planets:
            # Only act if we have a meaningful number of ships
            if src.ships < 10:
                continue

            # Pick a completely random target — no reasoning applied
            dest = random.choice(targets)

            # Send half our ships so we don't leave the planet defenceless
            gameinfo.planet_order(src, dest, src.ships // 2)
