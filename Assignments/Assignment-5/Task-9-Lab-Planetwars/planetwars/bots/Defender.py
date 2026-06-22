class Defender(object):
    def update(self, gameinfo):
        my_planets = gameinfo._my_planets()
        not_my_planets = gameinfo._not_my_planets()
        enemy_fleets = gameinfo._enemy_fleets()

        if not my_planets:
            return

        # --- Defence phase ---
        # Check each visible enemy fleet to see if it's heading to one of our planets
        for fleet in enemy_fleets.values():
            target_id = fleet.dest.ID
            if target_id in my_planets:
                threatened = my_planets[target_id]
                # Only reinforce if our planet will be outnumbered on arrival
                if threatened.ships < fleet.ships:
                    # Find a safe friendly planet with spare ships (not the threatened one)
                    safe = {k: p for k, p in my_planets.items()
                            if k != target_id and p.ships > 10}
                    if safe:
                        reinforcer = max(safe.values(), key=lambda p: p.ships)
                        gameinfo.planet_order(reinforcer, threatened, int(reinforcer.ships * 0.75))
                        return  # handle one threat per tick

        # --- Attack phase (fallback when no threats detected) ---
        # Use BestWorst logic: strongest source attacks weakest target
        if not_my_planets:
            src = max(my_planets.values(), key=lambda p: p.ships)
            dest = min(not_my_planets.values(), key=lambda p: p.ships)
            if src.ships > 10:
                gameinfo.planet_order(src, dest, int(src.ships * 0.75))
