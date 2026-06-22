"""Simple straight-line projectile for the Soldier on Patrol simulation."""

import pyglet
from graphics import COLOUR_NAMES, window
from vector2d import Vector2D

PROJECTILE_SPEED = 300.0
HIT_RADIUS       = 15.0
DAMAGE           = 25


class Projectile:
    def __init__(self, start_pos, target, damage=DAMAGE):
        self.pos = start_pos
        self.target = target
        self.active = True
        self.damage = damage

        direction = (target.pos - start_pos).normalise()
        self.vel = Vector2D(direction.x * PROJECTILE_SPEED, direction.y * PROJECTILE_SPEED)

        self.shape = pyglet.shapes.Circle(
            self.pos.x, self.pos.y, 4,
            color=COLOUR_NAMES['YELLOW'],
            batch=window.get_batch("main")
        )

    def update(self, delta):
        if not self.active:
            return

        self.pos.x += self.vel.x * delta
        self.pos.y += self.vel.y * delta
        self.shape.x = self.pos.x
        self.shape.y = self.pos.y

        # Hit check — also deactivate if target already dead
        if not self.target.alive or self.pos.distance(self.target.pos) < HIT_RADIUS:
            if self.target.alive:
                self.target.take_damage(self.damage)
            self._deactivate()

        # Deactivate if off screen
        world = self.target.world
        if not (0 < self.pos.x < world.cx and 0 < self.pos.y < world.cy):
            self._deactivate()

    def _deactivate(self):
        self.active = False
        self.shape.visible = False
