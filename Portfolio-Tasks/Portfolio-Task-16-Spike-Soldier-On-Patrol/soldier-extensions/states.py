"""FSM State Classes for the Soldier on Patrol simulation (Extensions).

Four high-level states: PatrolState, AttackState, FleeState, HealingState.
Transition priority order: Flee > Attack > Heal > Patrol
"""

from vector2d import Vector2D

DETECTION_RANGE = 200.0
FLEE_HEALTH_THRESHOLD = 30   # hp — enter flee/heal when below this
HEAL_EXIT_THRESHOLD = 80     # hp — leave healing only when above this (hysteresis)


class State:
    """Base class. All states share this contract."""
    def enter(self, agent): pass
    def execute(self, agent, delta): return Vector2D(0, 0)
    def exit(self, agent): pass
    def status(self): return ''


class PatrolState(State):
    """Soldier follows its waypoint path. Monitors for threats and health."""

    def enter(self, agent):
        agent.color = 'ORANGE'

    def execute(self, agent, delta):
        # Health critical + enemy → flee immediately
        if agent.health < FLEE_HEALTH_THRESHOLD and agent.detect_enemy():
            agent.change_state(FleeState())
            return Vector2D(0, 0)
        # Health low, no enemy → go heal
        if agent.health < FLEE_HEALTH_THRESHOLD and hasattr(agent.world, 'healing_station'):
            agent.change_state(HealingState())
            return Vector2D(0, 0)
        # Enemy in range → attack
        if agent.detect_enemy():
            agent.change_state(AttackState())
            return Vector2D(0, 0)
        # Default: follow patrol path
        return agent.follow_path()


class AttackState(State):
    """Soldier stops and fires. Manages ammo and a reload cycle (Extension 3)."""

    MAX_AMMO = 6
    SHOOT_RATE = 1.0    # seconds between shots
    RELOAD_TIME = 2.0   # seconds to reload full magazine

    def enter(self, agent):
        agent.color = 'RED'
        agent.vel = Vector2D(0, 0)
        self.shoot_cooldown = 0.0
        self.ammo = self.MAX_AMMO
        self.reloading = False
        self.reload_timer = 0.0

    def execute(self, agent, delta):
        # Health critical → flee, even mid-combat
        if agent.health < FLEE_HEALTH_THRESHOLD:
            agent.change_state(FleeState())
            return Vector2D(0, 0)
        # Threat cleared → back to patrol
        if not agent.detect_enemy():
            agent.change_state(PatrolState())
            return Vector2D(0, 0)
        # Reload cycle
        if self.reloading:
            self.reload_timer -= delta
            if self.reload_timer <= 0:
                self.reloading = False
                self.ammo = self.MAX_AMMO
        else:
            self.shoot_cooldown -= delta
            if self.shoot_cooldown <= 0 and self.ammo > 0:
                agent.shoot()
                self.ammo -= 1
                self.shoot_cooldown = self.SHOOT_RATE
                if self.ammo == 0:
                    self.reloading = True
                    self.reload_timer = self.RELOAD_TIME
        return Vector2D(0, 0)

    def exit(self, agent):
        pass

    def status(self):
        if self.reloading:
            return f'[Reloading {self.reload_timer:.1f}s]'
        return f'[Ammo {self.ammo}/{self.MAX_AMMO}]'


class FleeState(State):
    """Soldier runs away from the nearest enemy when health is critical."""

    def enter(self, agent):
        agent.color = 'PURPLE'

    def execute(self, agent, delta):
        if not agent.detect_enemy():
            # Safe — decide next action based on health
            if agent.health < FLEE_HEALTH_THRESHOLD and hasattr(agent.world, 'healing_station'):
                agent.change_state(HealingState())
            else:
                agent.change_state(PatrolState())
            return Vector2D(0, 0)
        nearest = agent._nearest_enemy()
        if nearest:
            return agent.flee(nearest.pos)
        return Vector2D(0, 0)


class HealingState(State):
    """Soldier navigates to the Healing Station and recovers health.
    Uses hysteresis: enters below 30hp, exits only when health reaches 80hp.
    """

    HEAL_RATE = 20  # hp per second recovered at station

    def enter(self, agent):
        agent.color = 'GREEN'

    def execute(self, agent, delta):
        # Threats always take priority over healing
        if agent.detect_enemy():
            if agent.health < FLEE_HEALTH_THRESHOLD:
                agent.change_state(FleeState())
            else:
                agent.change_state(AttackState())
            return Vector2D(0, 0)

        station = agent.world.healing_station
        dist = agent.pos.distance(station.pos)
        if dist > 20:
            return agent.arrive(station.pos, 'normal')
        # At station — recover health
        agent.health = min(agent.max_health, agent.health + self.HEAL_RATE * delta)
        if agent.health >= HEAL_EXIT_THRESHOLD:
            agent.change_state(PatrolState())
        return Vector2D(0, 0)
