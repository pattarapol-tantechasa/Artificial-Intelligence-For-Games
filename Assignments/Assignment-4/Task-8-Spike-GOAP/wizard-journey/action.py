"""
Action class for the Wizard Potion Shop GOAP system.
Represents a single action the agent can perform.
"""


class Action:
    """
    Represents an action the agent can take.

    An action has:
    - name: human-readable name
    - cost: numeric cost (affects planning priority)
    - check: function to check preconditions (state -> bool)
    - apply: function to apply effects (state -> new_state)
    """

    def __init__(self, name, cost, check, apply_fn):
        """
        Initialize an action.

        Args:
            name: String name of the action
            cost: Numeric cost (lower is better)
            check: Function(state) -> bool that checks preconditions
            apply_fn: Function(state) -> WorldState that applies effects
        """
        self.name = name
        self.cost = cost
        self.check = check
        self.apply_fn = apply_fn

    def is_applicable(self, state):
        """Check if this action can be applied to the current state."""
        try:
            return self.check(state)
        except Exception:
            return False

    def apply(self, state):
        """
        Apply this action to a state, returning a new state.
        Returns None if preconditions are not met.
        """
        if not self.is_applicable(state):
            return None
        return self.apply_fn(state)

    def __repr__(self):
        return f"Action({self.name}, cost={self.cost})"
