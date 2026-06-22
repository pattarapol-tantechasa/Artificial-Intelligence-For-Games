"""
Simulation: Step-by-step execution and visualization of a GOAP plan.
Shows what the wizard does and how the world changes.
"""

from world_state import WorldState
from action import Action
from typing import List


class Simulation:
    """Runs and visualizes a GOAP plan step-by-step."""

    def __init__(self, initial_state: WorldState):
        """
        Initialize simulation with starting state.

        Args:
            initial_state: The starting world state
        """
        self.initial_state = initial_state

    def print_state(self, state: WorldState, title: str = "State"):
        """Pretty-print a world state."""
        location = "Unknown"
        if state.is_at_home:
            location = "Home"
        elif state.is_at_shop:
            location = "Potion Shop"
        elif state.is_at_forest:
            location = "Forest"

        print(f"\n{title}")
        print(f"   Location: {location}")
        print(f"   Energy: {state.energy} | Hunger: {state.hunger} | Gold: {state.gold}")
        print(f"   Potions: {state.potions} | Ingredients: {state.ingredients} | Apples: {state.apple}")
        print(
            f"   Knowledge: has_map={state.has_map}, quest_complete={state.quest_complete}"
        )

    def print_change(self, label: str, old_value, new_value):
        """Pretty-print a state change."""
        if old_value != new_value:
            print(f"      {label}: {old_value} -> {new_value}")

    def run_plan(self, plan: List[Action]):
        """
        Execute and visualize a plan step-by-step.

        Args:
            plan: List of Action objects to execute
        """
        print("\n" + "=" * 70)
        print("WIZARD POTION SHOP - GOAP SIMULATION")
        print("=" * 70)
        print("\nA young wizard prepares to venture into the Magical Forest.")
        print("To survive the dangers ahead, they need an MP Potion.")
        print("Let's watch them plan and execute their quest!\n")

        # Show initial state
        current_state = self.initial_state.copy()
        self.print_state(current_state, "STARTING STATE")

        if not plan:
            print("\nNo plan could be found!")
            return

        print(f"\nPLAN FOUND: {len(plan)} actions")
        for i, action in enumerate(plan, 1):
            print(f"   {i}. {action.name} (cost: {action.cost})")

        # Execute each action
        print("\n" + "=" * 70)
        print("EXECUTING PLAN")
        print("=" * 70)

        total_cost = 0

        for step, action in enumerate(plan, 1):
            print(f"\n[Step {step}] {action.name}")
            print(f"         Cost: {action.cost}")

            # Show what's about to happen
            old_state = current_state.copy()

            # Apply action
            current_state = action.apply(old_state)

            if current_state is None:
                print("         Action preconditions no longer met!")
                return

            # Show changes
            print("         Changes:")
            self.print_change("Energy", old_state.energy, current_state.energy)
            self.print_change("Hunger", old_state.hunger, current_state.hunger)
            self.print_change("Gold", old_state.gold, current_state.gold)
            self.print_change("Ingredients", old_state.ingredients, current_state.ingredients)
            self.print_change("Apples", old_state.apple, current_state.apple)
            self.print_change("Potions", old_state.potions, current_state.potions)
            self.print_change("Has Map", old_state.has_map, current_state.has_map)
            self.print_change("Quest Complete", old_state.quest_complete, current_state.quest_complete)

            location_old = (
                "Home" if old_state.is_at_home
                else "Shop" if old_state.is_at_shop
                else "Forest"
            )
            location_new = (
                "Home" if current_state.is_at_home
                else "Shop" if current_state.is_at_shop
                else "Forest"
            )
            if location_old != location_new:
                self.print_change("Location", location_old, location_new)

            total_cost += action.cost

        # Show final state
        self.print_state(current_state, "FINAL STATE")

        # Check goal
        if current_state.is_goal():
            print("\n" + "=" * 70)
            print("GOAL ACHIEVED!")
            print("=" * 70)
            print("The wizard has successfully obtained the MP Potion!")
            print("They return home, ready for the adventure ahead.")
            print(f"\nTotal Plan Cost: {total_cost}")
        else:
            print("\nGoal not reached!")
