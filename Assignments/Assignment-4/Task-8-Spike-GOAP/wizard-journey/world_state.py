"""
WorldState class for the Wizard Potion Shop GOAP system.
Represents the complete state of the game world.
"""


class WorldState:
    """Represents the complete state of the game world."""

    def __init__(self):
        # Location (mutually exclusive - exactly one is True)
        self.is_at_home = True
        self.is_at_shop = False
        self.is_at_forest = False

        # Resources
        self.energy = 50
        self.hunger = 0
        self.gold = 0
        self.ingredients = 0
        self.apple = 0
        self.potions = 0

        # Knowledge/Progress
        self.has_map = False
        self.quest_complete = False

    def copy(self):
        """Create a deep copy for exploring new states."""
        new_state = WorldState()
        new_state.__dict__.update(self.__dict__)
        return new_state

    def is_goal(self):
        """Check if this state satisfies the goal."""
        return self.potions >= 1 and self.is_at_home

    def __eq__(self, other):
        """States are equal if all attributes match."""
        if not isinstance(other, WorldState):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self):
        """Make state hashable for use in sets/dicts (needed for A* closed_set)."""
        return hash(tuple(sorted(self.__dict__.items())))

    def __repr__(self):
        """String representation for debugging."""
        return (
            f"WorldState("
            f"energy={self.energy}, hunger={self.hunger}, gold={self.gold}, "
            f"ingredients={self.ingredients}, apple={self.apple}, potions={self.potions}, "
            f"at_home={self.is_at_home}, at_shop={self.is_at_shop}, at_forest={self.is_at_forest}, "
            f"has_map={self.has_map}, quest_complete={self.quest_complete})"
        )
