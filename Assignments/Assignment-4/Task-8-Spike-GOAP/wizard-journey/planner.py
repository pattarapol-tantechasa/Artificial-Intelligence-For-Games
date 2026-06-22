"""
GOAPPlanner: A* graph search planner for GOAP.
Searches through world states to find a sequence of actions that achieve the goal.
"""

import heapq
from typing import List, Optional
from action import Action
from world_state import WorldState


class GOAPPlanner:
    """A* graph search planner for GOAP."""

    def __init__(self, actions: List[Action]):
        """
        Initialize the planner with a list of available actions.

        Args:
            actions: List of Action objects
        """
        self.actions = actions

    def heuristic(self, state: WorldState) -> float:
        """
        Estimate cost from current state to goal.

        This is an admissible heuristic - it never overestimates.
        It estimates the minimum cost to satisfy all unsatisfied goal conditions.

        Goal conditions:
        - potions >= 1
        - is_at_home == True
        """
        cost = 0

        # Do we need to buy a potion?
        if state.potions < 1:
            # Do we have enough gold?
            if state.gold < 11:  # Need gold > 10
                # Cheapest way to get gold is Complete Quest (30 gold for cost 60)
                if not state.quest_complete:
                    cost += 60
                else:
                    # Quest already done, must hunt and sell
                    # Need 6+ ingredients to get 12+ gold (6 * 2 = 12)
                    # Hunt gives 20 ingredients for cost 30
                    cost += 30 + (5 * 5)  # Hunt + 5 sells
            # Still need to buy the potion
            cost += 20

        # Do we need to be home?
        if not state.is_at_home:
            # Travel to Home costs 50
            cost += 50

        return cost

    def plan(self, initial_state: WorldState) -> Optional[List[Action]]:
        """
        Find a sequence of actions from initial state to goal using A* search.

        Args:
            initial_state: Starting world state

        Returns:
            List of Action objects, or None if no plan exists
        """
        # Priority queue: (f_cost, counter, state, path_of_actions)
        open_set = [(0, 0, initial_state, [])]
        closed_set = set()
        counter = 0

        while open_set:
            f_cost, _, current_state, path = heapq.heappop(open_set)

            # Goal check
            if current_state.is_goal():
                return path

            # Skip if we've already explored this state
            if current_state in closed_set:
                continue
            closed_set.add(current_state)

            # Try all applicable actions
            for action in self.actions:
                if action.is_applicable(current_state):
                    next_state = action.apply(current_state)

                    if next_state and next_state not in closed_set:
                        # g_cost: sum of all costs in path so far + this action's cost
                        g_cost = sum(a.cost for a in path) + action.cost

                        # h_cost: heuristic estimate to goal
                        h_cost = self.heuristic(next_state)

                        # f_cost: g + h
                        f_cost_new = g_cost + h_cost

                        counter += 1
                        heapq.heappush(
                            open_set,
                            (f_cost_new, counter, next_state, path + [action]),
                        )

        # No plan found
        return None
