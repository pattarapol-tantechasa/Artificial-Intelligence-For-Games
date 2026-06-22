from world import World, Obstacle
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

        # Obstacles placed between attacker and target path — used as cover
        self.world.obstacles = [
            Obstacle(cx * 0.40, cy * 0.35, 40),
            Obstacle(cx * 0.52, cy * 0.65, 40),
            Obstacle(cx * 0.62, cy * 0.48, 35),
        ]

    def input_mouse(self, x, y, button, modifiers):
        self.world.input_mouse(x, y, button, modifiers)

    def input_keyboard(self, symbol, modifiers):
        self.world.input_keyboard(symbol, modifiers)

    def update(self, delta):
        self.world.update(delta)
