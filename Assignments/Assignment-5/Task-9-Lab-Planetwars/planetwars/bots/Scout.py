class Scout(object):
    def update(self, gameinfo):
        my_planets = gameinfo._my_planets()
        not_my_planets = gameinfo._not_my_planets()
        my_fleets = gameinfo._my_fleets()

        if not my_planets:
            return

        # --- Scout phase ---
        # Find planets we haven't seen recently (vision_age > 0 means stale info)
        stale_planets = {k: p for k, p in not_my_planets.items() if p.vision_age > 0}

        # Only send a scout if we have no fleets already in transit (avoid spam)
        already_scouting = {f.dest.ID for f in my_fleets.values()}

        if stale_planets:
            # Find the closest stale planet that we aren't already scouting
            unscouted = {k: p for k, p in stale_planets.items() if k not in already_scouting}
            if unscouted:
                src = max(my_planets.values(), key=lambda p: p.ships)
                probe_target = min(unscouted.values(), key=lambda p: src.distance_to(p))
                if src.ships > 2:
                    # Send just 1 ship — enough to reveal the planet on arrival
                    gameinfo.planet_order(src, probe_target, 1)
                    return

        # --- Attack phase ---
        # We have fresh info on all visible planets — commit a real attack
        if not_my_planets:
            src = max(my_planets.values(), key=lambda p: p.ships)
            dest = min(not_my_planets.values(), key=lambda p: p.ships)
            if src.ships > 10:
                gameinfo.planet_order(src, dest, int(src.ships * 0.75))
