''' Agent that walks along a found path node by node.

Created for COS30002 AI for Games, Lab,
Task 5 Extension - Animated Path Agent
'''
from math import hypot
from graphics import COLOUR_NAMES, window
import pyglet

class Agent:
    SPEED = 150  # pixels per second

    def __init__(self):
        self.path = []      # list of Box objects to walk through
        self.path_idx = 0   # index of current target in path
        self.x = 0.0
        self.y = 0.0
        self.active = False
        self.circle = pyglet.shapes.Circle(
            0, 0, radius=8,
            color=COLOUR_NAMES['RED'],
            batch=window.get_batch("path")
        )
        self.circle.visible = False

    def set_path(self, boxes, path_indices):
        ''' Start walking a new path. boxes is the BoxWorld box list,
        path_indices is the list of node indices from the search result. '''
        if len(path_indices) < 2:
            self.active = False
            self.circle.visible = False
            return
        self.path = [boxes[i] for i in path_indices]
        self.path_idx = 0
        start = self.path[0].center()
        self.x = float(start.x)
        self.y = float(start.y)
        self.circle.x = self.x
        self.circle.y = self.y
        self.circle.visible = True
        self.active = True

    def update(self, dt):
        ''' Move toward the next node in the path each frame. '''
        if not self.active:
            return
        if self.path_idx >= len(self.path) - 1:
            self.active = False
            return

        target = self.path[self.path_idx + 1].center()
        tx, ty = float(target.x), float(target.y)

        dx = tx - self.x
        dy = ty - self.y
        dist = hypot(dx, dy)

        move = self.SPEED * dt
        if dist <= move:
            # reached the next node — snap to it and advance
            self.x = tx
            self.y = ty
            self.path_idx += 1
        else:
            # move toward it
            self.x += (dx / dist) * move
            self.y += (dy / dist) * move

        self.circle.x = self.x
        self.circle.y = self.y
