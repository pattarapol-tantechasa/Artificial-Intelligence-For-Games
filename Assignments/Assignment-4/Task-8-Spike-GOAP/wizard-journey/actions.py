"""
All 11 action definitions for the Wizard Potion Shop GOAP system.
"""

from action import Action


def create_actions():
    """Create and return all 11 actions."""

    actions = []

    # 1. Find Potion Shop
    def find_shop_check(s):
        return s.has_map == False and s.energy > 30

    def find_shop_apply(s):
        new_s = s.copy()
        new_s.has_map = True
        new_s.energy -= 15
        return new_s

    actions.append(Action("Find Potion Shop", 20, find_shop_check, find_shop_apply))

    # 2. Travel to Shop
    def travel_to_shop_check(s):
        return (
            s.is_at_shop == False
            and s.has_map == True
            and s.energy > 30
        )

    def travel_to_shop_apply(s):
        new_s = s.copy()
        new_s.is_at_home = False
        new_s.is_at_forest = False
        new_s.is_at_shop = True
        new_s.energy -= 20
        new_s.hunger += 20
        return new_s

    actions.append(Action("Travel to Shop", 50, travel_to_shop_check, travel_to_shop_apply))

    # 3. Travel to Home
    def travel_to_home_check(s):
        return s.is_at_home == False and s.energy > 30

    def travel_to_home_apply(s):
        new_s = s.copy()
        new_s.is_at_shop = False
        new_s.is_at_forest = False
        new_s.is_at_home = True
        new_s.energy -= 20
        new_s.hunger += 20
        return new_s

    actions.append(Action("Travel to Home", 50, travel_to_home_check, travel_to_home_apply))

    # 4. Travel to Forest
    def travel_to_forest_check(s):
        return s.is_at_forest == False and s.energy > 30

    def travel_to_forest_apply(s):
        new_s = s.copy()
        new_s.is_at_home = False
        new_s.is_at_shop = False
        new_s.is_at_forest = True
        new_s.energy -= 20
        new_s.hunger += 20
        return new_s

    actions.append(Action("Travel to Forest", 50, travel_to_forest_check, travel_to_forest_apply))

    # 5. Complete Quest for Adventure Guild
    def complete_quest_check(s):
        return s.quest_complete == False and s.energy > 50

    def complete_quest_apply(s):
        new_s = s.copy()
        new_s.quest_complete = True
        new_s.energy -= 40
        new_s.hunger += 30
        new_s.gold += 30
        return new_s

    actions.append(Action("Complete Quest", 60, complete_quest_check, complete_quest_apply))

    # 6. Sell Monster Ingredients
    def sell_ingredients_check(s):
        return s.is_at_shop == True and s.ingredients > 0 and s.energy > 20

    def sell_ingredients_apply(s):
        new_s = s.copy()
        new_s.gold += 2
        new_s.ingredients -= 1
        new_s.energy -= 5
        return new_s

    actions.append(Action("Sell Ingredients", 5, sell_ingredients_check, sell_ingredients_apply))

    # 7. Eat Food
    def eat_food_check(s):
        return s.apple > 0 and s.hunger > 0

    def eat_food_apply(s):
        new_s = s.copy()
        new_s.hunger -= 10
        return new_s

    actions.append(Action("Eat Food", 10, eat_food_check, eat_food_apply))

    # 8. Rest
    def rest_check(s):
        return s.is_at_home == True

    def rest_apply(s):
        new_s = s.copy()
        new_s.energy = min(new_s.energy + 50, 100)
        return new_s

    actions.append(Action("Rest", 10, rest_check, rest_apply))

    # 9. Buy Potion
    def buy_potion_check(s):
        return s.gold > 10 and s.is_at_shop == True

    def buy_potion_apply(s):
        new_s = s.copy()
        new_s.gold -= 10
        new_s.potions += 1
        return new_s

    actions.append(Action("Buy Potion", 10, buy_potion_check, buy_potion_apply))

    # 10. Hunt Monster
    def hunt_monster_check(s):
        return s.is_at_forest == True and s.energy > 40

    def hunt_monster_apply(s):
        new_s = s.copy()
        new_s.ingredients += 20
        new_s.energy -= 25
        return new_s

    actions.append(Action("Hunt Monster", 30, hunt_monster_check, hunt_monster_apply))

    # 11. Gather Apple
    def gather_apple_check(s):
        return s.is_at_forest == True and s.energy > 20

    def gather_apple_apply(s):
        new_s = s.copy()
        new_s.apple += 2
        new_s.energy -= 10
        return new_s

    actions.append(Action("Gather Apple", 10, gather_apple_check, gather_apple_apply))

    return actions
