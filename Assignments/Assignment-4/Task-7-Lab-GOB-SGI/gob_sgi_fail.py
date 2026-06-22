'''Goal Oriented Behaviour - SGI FAILURE CASE

Demonstrates a situation where Simple Goal Insistence (SGI) fails to work well.

FAILURE SCENARIO: Conflicting Goals with Negative Side Effects
================================================================
Two equally urgent goals (Eat and Sleep) but EVERY action has a negative side effect
on the other goal. The agent endlessly oscillates, solving one problem while creating
another.

Initial State:
- Goal: Eat (insistence = 10)
- Goal: Sleep (insistence = 10)

Actions available:
- drink coffee: reduces Sleep by 3 BUT increases Eat by 2 (side effect)
- eat heavy meal: reduces Eat by 3 BUT increases Sleep by 2 (side effect)

Expected Behavior:
The agent will oscillate endlessly:
1. Both goals at 10 → drink coffee (Sleep: 10→7, Eat: 10→12)
2. Eat at 12 (highest) → eat heavy meal (Eat: 12→9, Sleep: 7→9)
3. Sleep at 9 (tied/highest) → drink coffee (Sleep: 9→6, Eat: 9→11)
... and so on forever.

This demonstrates SGI's critical flaw: it's GREEDY and SHORT-SIGHTED. It only looks
at the current goal without considering that solving it will create new problems.

Created for COS30002 AI for Games, Lab
'''

VERBOSE = True
MAX_ITERATIONS = 20  # Limit iterations to show the failure pattern

# Global goals with initial values - CONFLICTING and HIGH
goals = {
    'Eat': 10,
    'Sleep': 10,
}

# Global (read-only) actions and effects - SIDE EFFECTS CREATE CONFLICT
# Each action solves one goal but WORSENS the other (negative side effects)
actions = {
    'drink coffee': { 'Sleep': -3, 'Eat': 2 },       # Reduces sleep but increases hunger!
    'eat heavy meal': { 'Eat': -3, 'Sleep': 2 },     # Reduces hunger but increases tiredness!
}


def apply_action(action):
    '''Change all goal values using this action. An action can change multiple
    goals (positive and negative side effects).
    Negative changes are limited to a minimum goal value of 0.
    '''
    for goal, change in actions[action].items():
        goals[goal] = max(goals[goal] + change, 0)


def action_utility(action, goal):
    '''Return the 'value' of using "action" to achieve "goal".

    For example::
        action_utility('get snack', 'Eat')

    returns a number representing the effect that getting a snack has on our
    'Eat' goal. Larger (more positive) numbers mean the action is more
    beneficial.
    '''
    if goal in actions[action]:
        # Is the goal affected by the specified action?
        return -actions[action][goal]
    else:
        # It isn't, so utility is zero.
        return 0


def choose_action():
    '''Return the best action to respond to the current most insistent goal.
    '''
    assert len(goals) > 0, 'Need at least one goal'
    assert len(actions) > 0, 'Need at least one action'

    # Find the most insistent goal
    best_goal, best_goal_value = max(goals.items(), key=lambda item: item[1])

    if VERBOSE: print('BEST_GOAL:', best_goal, goals[best_goal])

    # Find the best (highest utility) action to take.
    best_action = None
    best_utility = None
    for key, value in actions.items():
        # Does this action change the "best goal" we need to change?
        if best_goal in value:
            if best_action is None:
                best_action = key
                best_utility = action_utility(key, best_goal)
            else:
                current_utility = action_utility(key, best_goal)
                if current_utility > best_utility:
                    best_action = key
                    best_utility = current_utility

    return best_action


def print_actions():
    print('ACTIONS:')
    for name, effects in actions.items():
        print(" * [%s]: %s" % (name, str(effects)))


def run_until_all_goals_zero():
    HR = '-'*40
    print_actions()
    print('>> Start <<')
    print(HR)
    running = True
    iteration = 0

    while running and iteration < MAX_ITERATIONS:
        iteration += 1
        print(f'[ITERATION {iteration}]')
        print('GOALS:', goals)
        # What is the best action
        action = choose_action()
        print('BEST ACTION:', action)
        # Apply the best action
        apply_action(action)
        print('NEW GOALS:', goals)
        # Stop?
        if all(value == 0 for goal, value in goals.items()):
            running = False
        print(HR)

    # finished
    if iteration >= MAX_ITERATIONS:
        print(f'>> STUCK IN LOOP! Stopped after {MAX_ITERATIONS} iterations <<')
        print('ANALYSIS: Goals never reached zero. Agent oscillates between actions.')
        print('This demonstrates SGI FAILURE - the agent cannot escape this cycle.')
    else:
        print('>> Done! <<')


if __name__ == '__main__':
    run_until_all_goals_zero()
