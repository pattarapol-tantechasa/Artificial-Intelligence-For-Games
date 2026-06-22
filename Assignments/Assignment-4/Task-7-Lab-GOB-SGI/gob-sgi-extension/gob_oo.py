"""
Goal Oriented Behaviour - Object Oriented Design

Created for COS30002 AI for Games, Lab
Extended design demonstrating OO refactoring of the simple GOB approach.

WHY OBJECT-ORIENTED?
====================

ADVANTAGES of OO approach:
    Reusability: Create multiple agents with different goals/behaviors
    Extensibility: Easy to subclass Agent for specialized behavior
    Clarity: Code structure mirrors real-world concepts (agents, goals, actions)
    Encapsulation: Goals and actions belong to agents, not global state
    Testability: Each class can be tested independently
    Maintainability: Changes to one agent don't affect others

DISADVANTAGES of OO approach:
    More boilerplate: Classes require more setup code
    Overkill for simple scenarios: Dictionary approach is simpler for prototyping
    Overhead: Object creation has more memory/runtime cost
    Learning curve: Requires understanding of classes and inheritance
    Not always appropriate: Some problems don't benefit from OO design

WHEN TO USE OO:
  • Multiple agents with independent behavior
  • Long-term maintainability
  • Production game code
  • When you need inheritance/polymorphism

WHEN TO AVOID OO:
  • Quick prototyping
  • Simple one-off simulations
  • Minimal code footprint needed
"""

VERBOSE = True


class Goal:
    """Represents a single goal with an insistence value."""

    def __init__(self, name: str, value: int):
        """
        Args:
            name: The goal name (e.g., 'Eat', 'Sleep')
            value: Current insistence value (how urgent the goal is)
        """
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Goal('{self.name}', {self.value})"


class Action:
    """Represents an action and its effects on goals."""

    def __init__(self, name: str, effects: dict):
        """
        Args:
            name: Action name (e.g., 'get raw food')
            effects: Dict mapping goal names to value changes
                    (e.g., {'Eat': -3, 'Health': 1})
        """
        self.name = name
        self.effects = effects  # {goal_name: change_value}

    def __repr__(self):
        return f"Action('{self.name}', {self.effects})"


class Agent:
    """
    An agent with goals and actions using Simple Goal Insistence (SGI).

    SGI Decision Making:
      1. Pick the most pressing goal (highest insistence value)
      2. Find the best action to satisfy that goal
      3. Apply the action (update goals)
      4. Repeat until all goals are satisfied (value = 0)
    """

    def __init__(self, name: str, goals: list, actions: list):
        """
        Args:
            name: Agent identifier
            goals: List of Goal objects
            actions: List of Action objects
        """
        self.name = name
        self.goals = goals
        self.actions = actions

    def action_utility(self, action: Action, goal: Goal) -> int:
        """
        Calculate utility of an action for achieving a specific goal.

        Args:
            action: Action to evaluate
            goal: Goal to evaluate against

        Returns:
            Utility value (higher = more beneficial)
            Returns 0 if action doesn't affect the goal
        """
        if goal.name in action.effects:
            # The action affects this goal
            # Utility is the negative of the effect (inverted because effects are negative)
            return -action.effects[goal.name]
        else:
            # Action doesn't affect this goal
            return 0

    def choose_action(self) -> Action:
        """
        Use SGI to choose the best action for the most pressing goal.

        Returns:
            The best Action object to take next
        """
        assert len(self.goals) > 0, 'Agent needs at least one goal'
        assert len(self.actions) > 0, 'Agent needs at least one action'

        # Step 1: Find the most insistent goal
        best_goal = max(self.goals, key=lambda g: g.value)

        if VERBOSE:
            print(f'BEST_GOAL: {best_goal.name} {best_goal.value}')

        # Step 2: Find the best action for that goal
        best_action = None
        best_utility = None

        for action in self.actions:
            # Does this action affect our best goal?
            if best_goal.name in action.effects:
                # Calculate utility of this action
                utility = self.action_utility(action, best_goal)

                # Is this the first valid action, or is it better than the current best?
                if best_action is None or utility > best_utility:
                    best_action = action
                    best_utility = utility

        return best_action

    def apply_action(self, action: Action):
        """
        Execute an action, updating all goal values.

        Args:
            action: Action to apply
        """
        for goal in self.goals:
            if goal.name in action.effects:
                # Apply the effect, but don't go below 0
                goal.value = max(goal.value + action.effects[goal.name], 0)

    def goals_satisfied(self) -> bool:
        """Check if all goals are satisfied (value = 0)."""
        return all(goal.value == 0 for goal in self.goals)

    def get_goals_string(self) -> str:
        """Return a string representation of current goals."""
        goals_dict = {goal.name: goal.value for goal in self.goals}
        return str(goals_dict)


class World:
    """Manages the simulation of an agent pursuing its goals."""

    def __init__(self, agent: Agent):
        self.agent = agent

    def print_actions(self):
        """Display all available actions."""
        print('ACTIONS:')
        for action in self.agent.actions:
            print(f" * [{action.name}]: {action.effects}")

    def run(self):
        """Run the simulation until all goals are satisfied."""
        HR = '-' * 40
        self.print_actions()
        print('>> Start <<')
        print(HR)

        while not self.agent.goals_satisfied():
            # Print current state
            print(f'GOALS: {self.agent.get_goals_string()}')

            # Choose and execute action
            action = self.agent.choose_action()
            print(f'BEST ACTION: {action.name}')
            self.agent.apply_action(action)

            # Print new state
            print(f'NEW GOALS: {self.agent.get_goals_string()}')
            print(HR)

        print('>> Done! <<')


# =============================================================================

def main():
    """Create an agent and run the simulation."""

    # Create goals (same as gob_simple.py)
    goals = [
        Goal('Eat', 4),
        Goal('Sleep', 3),
    ]

    # Create actions (same as gob_simple.py)
    actions = [
        Action('get raw food', {'Eat': -3}),
        Action('get snack', {'Eat': -2}),
        Action('sleep in bed', {'Sleep': -4}),
        Action('sleep on sofa', {'Sleep': -2}),
    ]

    # Create agent
    agent = Agent('Player', goals, actions)

    # Create world and run simulation
    world = World(agent)
    world.run()


if __name__ == '__main__':
    main()
