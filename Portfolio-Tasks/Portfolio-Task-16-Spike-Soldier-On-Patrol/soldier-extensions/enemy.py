"""Enemy that shoots back at soldiers (Extension 1)."""

import pyglet
from graphics import COLOUR_NAMES, window
from vector2d import Vector2D
from random import randrange, uniform

ENEMY_SHOOT_RATE = 2.0
ENEMY_DAMAGE     = 10
ENEMY_DETECTION  = 250.0


class Enemy:
    RADIUS     = 15
    BAR_W      = 40
    BAR_H      = 6
    BAR_OFFSET = 22
    MAX_HEALTH = 100

    def __init__(self, world):
        self.world = world
        self.alive = True
        self.health = self.MAX_HEALTH
        self.pos = Vector2D(
            randrange(100, world.cx - 100),
            randrange(100, world.cy - 100)
        )
        # Stagger initial cooldown so enemies don't all fire at once
        self.shoot_cooldown = uniform(0, ENEMY_SHOOT_RATE)

        self.shape = pyglet.shapes.Circle(
            self.pos.x, self.pos.y, self.RADIUS,
            color=COLOUR_NAMES['RED'],
            batch=window.get_batch("main")
        )
        self.health_bar_bg = pyglet.shapes.Rectangle(
            self.pos.x - self.BAR_W // 2, self.pos.y + self.BAR_OFFSET,
            self.BAR_W, self.BAR_H,
            color=COLOUR_NAMES['GREY'],
            batch=window.get_batch("main")
        )
        self.health_bar = pyglet.shapes.Rectangle(
            self.pos.x - self.BAR_W // 2, self.pos.y + self.BAR_OFFSET,
            self.BAR_W, self.BAR_H,
            color=COLOUR_NAMES['GREEN'],
            batch=window.get_batch("main")
        )

    def update(self, delta):
        if not self.alive:
            return
        self.shoot_cooldown -= delta
        if self.shoot_cooldown <= 0:
            target = self._nearest_soldier()
            if target:
                self._shoot_at(target)
            self.shoot_cooldown = ENEMY_SHOOT_RATE

    def _nearest_soldier(self):
        nearest, min_dist = None, float('inf')
        for agent in self.world.agents:
            if agent.alive:
                d = self.pos.distance(agent.pos)
                if d < ENEMY_DETECTION and d < min_dist:
                    min_dist, nearest = d, agent
        return nearest

    def _shoot_at(self, target):
        from projectile import Projectile
        self.world.projectiles.append(
            Projectile(self.pos.copy(), target, damage=ENEMY_DAMAGE)
        )

    def take_damage(self, amount):
        if not self.alive:
            return
        self.health -= amount
        ratio = max(0, self.health / self.MAX_HEALTH)
        self.health_bar.width = int(self.BAR_W * ratio)
        if self.health <= 0:
            self._die()

    def _die(self):
        self.alive = False
        self.shape.visible = False
        self.health_bar.visible = False
        self.health_bar_bg.visible = False
