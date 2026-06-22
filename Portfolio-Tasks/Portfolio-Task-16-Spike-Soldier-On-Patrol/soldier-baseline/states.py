"""FSM State Classes for the Soldier on Patrol simulation.

Each state follows the same contract: enter() once, execute() every frame,
exit() once. The agent delegates all decision-making to its current state.
"""

from vector2d import Vector2D

DETECTION_RANGE = 200.0  # pixels — how far the soldier can "see" an enemy


class State:
    """Base class. All states inherit from this."""
    def enter(self, agent): pass
    def execute(self, agent, delta): return Vector2D(0, 0)
    def exit(self, agent): pass


class PatrolState(State):
    """High-level: soldier follows its patrol path.
    Constantly checks for enemies — if one is spotted, switches to AttackState.
    """

    def enter(self, agent):
        agent.color = 'ORANGE'

    def execute(self, agent, delta):
        # Priority check: enemy spotted → interrupt patrol and attack
        if agent.detect_enemy():
            agent.change_state(AttackState())
            return Vector2D(0, 0)

        # No enemy — delegate movement to the low-level path-following behaviour
        return agent.follow_path()


class AttackState(State):
    """High-level: soldier stands still and fires at the nearest enemy.
    Manages its own shoot cooldown timer as a low-level behaviour.
    Returns to PatrolState when no enemies remain.
    """

    SHOOT_RATE = 1.5  # seconds between shots

    def enter(self, agent):
        agent.color = 'RED'
        agent.vel = Vector2D(0, 0)  # kill momentum so agent stops immediately
        self.shoot_cooldown = 0.0  # fire immediately on entry

    def execute(self, agent, delta):
        # If all enemies are gone, go back to patrolling
        if not agent.detect_enemy():
            agent.change_state(PatrolState())
            return Vector2D(0, 0)

        # Tick the cooldown and fire when ready
        self.shoot_cooldown -= delta
        if self.shoot_cooldown <= 0:
            agent.shoot()
            self.shoot_cooldown = self.SHOOT_RATE

        # Soldier stops moving while attacking
        return Vector2D(0, 0)

    def exit(self, agent):
        pass
