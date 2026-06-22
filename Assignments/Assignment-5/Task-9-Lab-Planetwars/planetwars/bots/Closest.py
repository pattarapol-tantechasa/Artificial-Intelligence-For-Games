class Closest(object):
    def update(self, gameinfo):
        my_planets = gameinfo._my_planets()
        not_my_planets = gameinfo._not_my_planets()

        if not my_planets or not not_my_planets:
            return

        # Pick the source planet with the most ships
        src = max(my_planets.values(), key=lambda p: p.ships)

        # Pick the target closest to our source (distance_to returns squared distance by default)
        dest = min(not_my_planets.values(), key=lambda p: src.distance_to(p))

        if src.ships > 10:
            gameinfo.planet_order(src, dest, int(src.ships * 0.75))
