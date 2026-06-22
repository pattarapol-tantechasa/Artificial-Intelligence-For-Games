"""Healing Station — a functional environmental region (Extension 2).

Soldiers with low health navigate here to recover. Positioned in the
bottom-left corner so it's away from the centre where enemies tend to spawn.
"""

import pyglet
from graphics import COLOUR_NAMES, window
from vector2d import Vector2D


class HealingStation:
    RADIUS = 35

    def __init__(self, world):
        self.pos = Vector2D(world.cx * 0.12, world.cy * 0.12)

        self.zone = pyglet.shapes.Circle(
            self.pos.x, self.pos.y, self.RADIUS,
            color=(0, 200, 80, 120),
            batch=window.get_batch("main")
        )
        self.label = pyglet.text.Label(
            'HEAL',
            x=self.pos.x, y=self.pos.y,
            anchor_x='center', anchor_y='center',
            color=COLOUR_NAMES['GREEN'],
            font_size=11,
            batch=window.get_batch("main")
        )
