import pyglet
from vector2d import Vector2D
from graphics import COLOUR_NAMES, window

HIT_RADIUS = 15.0


class Projectile:
    def __init__(self, pos, vel, color='YELLOW'):
        self.pos = pos.copy()
        self.vel = vel.copy()
        self.active = True
        self.shape = pyglet.shapes.Circle(
            self.pos.x, self.pos.y, 4,
            color=COLOUR_NAMES[color],
            batch=window.get_batch("main")
        )

    def update(self, dt):
        self.pos += self.vel * dt
        self.shape.x = self.pos.x
        self.shape.y = self.pos.y

    def check_hit(self, target):
        if self.pos.distance(target.pos) < HIT_RADIUS:
            self.deactivate()
            return True
        return False

    def deactivate(self):
        self.active = False
        self.shape.visible = False
