"""Game Controller — Emergent Group Behaviour (Baseline).

Spawns a flock of boid agents and wires up the update loop and input routing.
"""

from world import World
from graphics import window
from agent import Agent

game = None

NUM_AGENTS = 25

class Game():
    """Main game application class."""

    def __init__(self):
        self.world = World(window.width, window.height)

        for _ in range(NUM_AGENTS):
            agent = Agent(
                self.world,
                scale=30.0,
                mass=1.0,
                color='AQUA',
                max_speed=150,
                max_force=2000,
                vehicle_size=1.0,
                wander_jitter=15.0,
            )
            self.world.agents.append(agent)

    def input_mouse(self, x, y, button, modifiers):
        self.world.input_mouse(x, y, button, modifiers)

    def input_keyboard(self, symbol, modifiers):
        self.world.input_keyboard(symbol, modifiers)

    def update(self, delta):
        self.world.update(delta)
