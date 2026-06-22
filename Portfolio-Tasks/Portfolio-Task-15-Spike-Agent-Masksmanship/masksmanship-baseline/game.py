from world import World
from graphics import window
from agent import TargetAgent, AttackerAgent
from vector2d import Vector2D

game = None


class Game:
    def __init__(self):
        self.world = World(window.width, window.height)

        cx, cy = window.width, window.height

        # Static attacker on the left side
        attacker = AttackerAgent(self.world, Vector2D(cx * 0.15, cy * 0.5))
        self.world.attacker = attacker

        # Target patrols vertically on the right side
        waypoints = [
            Vector2D(cx * 0.75, cy * 0.2),
            Vector2D(cx * 0.75, cy * 0.8),
        ]
        target = TargetAgent(self.world, waypoints)
        self.world.target = target

    def input_mouse(self, x, y, button, modifiers):
        self.world.input_mouse(x, y, button, modifiers)

    def input_keyboard(self, symbol, modifiers):
        self.world.input_keyboard(symbol, modifiers)

    def update(self, delta):
        self.world.update(delta)
