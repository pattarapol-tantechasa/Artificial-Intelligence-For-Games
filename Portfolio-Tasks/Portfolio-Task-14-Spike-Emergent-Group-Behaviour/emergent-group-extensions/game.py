"""Game Controller — Emergent Group Behaviour (Extensions).

Spawns three factions:
  Prey      (cyan)   — 20 agents, flock + flee predators
  Predators (red)    —  3 agents, seek nearest prey
  Scavengers(yellow) —  7 agents, flock + trail predators from a distance
"""

from world import World
from graphics import window
from agent import Agent, PREY, PREDATOR, SCAVENGER

game = None


class Game():
    """Main game application class."""

    def __init__(self):
        self.world = World(window.width, window.height)
        self._spawn_prey(20)
        self._spawn_predators(3)
        self._spawn_scavengers(7)

    def _spawn_prey(self, count):
        for _ in range(count):
            agent = Agent(
                self.world,
                scale=30.0, mass=1.0,
                color='AQUA',
                max_speed=230, max_force=3200,
                vehicle_size=1.0,
                wander_jitter=15.0,
                faction=PREY,
                agent_radius=10.0,
            )
            self.world.agents.append(agent)

    def _spawn_predators(self, count):
        for _ in range(count):
            agent = Agent(
                self.world,
                scale=30.0, mass=1.5,
                color='RED',
                max_speed=200, max_force=2800,
                vehicle_size=1.6,
                wander_jitter=20.0,
                faction=PREDATOR,
                agent_radius=14.0,
            )
            self.world.agents.append(agent)
            self.world.predators.append(agent)

    def _spawn_scavengers(self, count):
        for _ in range(count):
            agent = Agent(
                self.world,
                scale=30.0, mass=1.0,
                color='YELLOW',
                max_speed=130, max_force=1800,
                vehicle_size=1.2,
                wander_jitter=12.0,
                faction=SCAVENGER,
                agent_radius=11.0,
            )
            self.world.agents.append(agent)

    def input_mouse(self, x, y, button, modifiers):
        self.world.input_mouse(x, y, button, modifiers)

    def input_keyboard(self, symbol, modifiers):
        self.world.input_keyboard(symbol, modifiers)

    def update(self, delta):
        self.world.update(delta)
