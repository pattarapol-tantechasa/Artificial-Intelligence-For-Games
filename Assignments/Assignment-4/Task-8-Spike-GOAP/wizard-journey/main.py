"""
Main entry point for the Wizard Potion Shop GOAP system.
Demonstrates planning, execution, and replanning.
"""

from world_state import WorldState
from actions import create_actions
from planner import GOAPPlanner
from simulation import Simulation


def main():
    """Main execution."""

    # TOGGLE THIS TO SHOW DIFFERENT STRATEGIES:
    # False = Use quest to get gold (default)
    # True  = Hunt and sell ingredients (alternative)
    QUEST_ALREADY_COMPLETE = False

    # 1. Create initial world state
    print("Creating wizard's initial world state...")
    initial_state = WorldState()

    # Set quest status based on scenario
    initial_state.quest_complete = QUEST_ALREADY_COMPLETE

    print(f"   Energy: {initial_state.energy}")
    print(f"   Gold: {initial_state.gold}")
    print(f"   Potions: {initial_state.potions}")
    print(f"   Location: Home")
    print(f"   Quest Available: {not QUEST_ALREADY_COMPLETE}")

    # 2. Load all actions
    print("\nLoading actions...")
    actions = create_actions()
    print(f"   Loaded {len(actions)} actions")

    # 3. Create planner
    print("\nCreating GOAP planner...")
    planner = GOAPPlanner(actions)

    # 4. Find a plan
    print("\nPlanning...")
    plan = planner.plan(initial_state)

    if plan:
        print(f"Plan found! ({len(plan)} steps)")
        print(f"   Cost: {sum(a.cost for a in plan)}")
        for i, action in enumerate(plan, 1):
            print(f"   {i}. {action.name}")
    else:
        print("No plan found!")
        return

    # 5. Run simulation

    sim = Simulation(initial_state)
    sim.run_plan(plan)

    print("\n" + "=" * 70)
    print("GOAP System Demonstration Complete!")
    print("=" * 70)
    print("\nTo see the alternative strategy:\n")
    print("1. Set QUEST_ALREADY_COMPLETE = False at top of main()")
    print("   Agent will do Quest for money to buy a MP Potion!\n")
    print("2. Set QUEST_ALREADY_COMPLETE = True at top of main()")
    print("   Agent will hunt and sell ingredients instead of using quest!\n")
    print("=" * 70)


if __name__ == "__main__":
    main()
