class BestWorst(object):
    def update(self, gameinfo):
        
        print(f"[BestWorst.py] is working")
        if gameinfo._my_planets() and gameinfo._not_my_planets():
            src = max(gameinfo._my_planets().values(), key=lambda p: p.ships)
            dest = min(gameinfo._not_my_planets().values(), key=lambda p: p.ships)


            if src.ships > 10:
                gameinfo.planet_order(src, dest, int(src.ships * 0.75))
