"""Stationary enemy target for the Soldier on Patrol simulation."""

import pyglet
from graphics import COLOUR_NAMES, window
from vector2d import Vector2D
from random import randrange


class Enemy:
    RADIUS = 15
    MAX_HEALTH = 100

    def __init__(self, world):
        self.world = world
        self.alive = True
        self.health = self.MAX_HEALTH
        self.pos = Vector2D(
            randrange(100, world.cx - 100),
            randrange(100, world.cy - 100)
        )
        self.shape = pyglet.shapes.Circle(
            self.pos.x, self.pos.y, self.RADIUS,
            color=COLOUR_NAMES['RED'],
            batch=window.get_batch("main")
        )
        self.health_bar_bg = pyglet.shapes.Rectangle(
            self.pos.x - 20, self.pos.y + 22, 40, 6,
            color=COLOUR_NAMES['GREY'],
            batch=window.get_batch("main")
        )
        self.health_bar = pyglet.shapes.Rectangle(
            self.pos.x - 20, self.pos.y + 22, 40, 6,
            color=COLOUR_NAMES['GREEN'],
            batch=window.get_batch("main")
        )

    def take_damage(self, amount):
        if not self.alive:
            return
        self.health -= amount
        ratio = max(0, self.health / self.MAX_HEALTH)
        self.health_bar.width = int(40 * ratio)
        if self.health <= 0:
            self._die()

    def _die(self):
        self.alive = False
        self.shape.visible = False
        self.health_bar.visible = False
        self.health_bar_bg.visible = False
