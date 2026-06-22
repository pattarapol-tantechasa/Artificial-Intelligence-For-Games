import random
import box_world
''' Agent that walks along a found path node by node.

Created for COS30002 AI for Games, Lab,
Task 5 Extension - Animated Path Agent
'''
from math import hypot
from graphics import COLOUR_NAMES, window
import pyglet

class Agent:
    SPEED = 150  # pixels per second
    SEARCH_ASTAR = 4
    SEARCH_NO_LIMIT = 0
    AGENT_COLOR = COLOUR_NAMES['RED']  # default colour, subclasses can override

    def __init__(self):
        self.path = []      # list of Box objects to walk through
        self.path_idx = 0   # index of current target in path
        self.x = 0.0
        self.y = 0.0
        self.active = False
        self.circle = pyglet.shapes.Circle(
            0, 0, radius=8,
            color=self.AGENT_COLOR,
            batch=window.get_batch("path")
        )
        self.circle.visible = False
        self.start_marker = pyglet.shapes.Arc(
            0, 0, 12, segments=30,
            color=self.AGENT_COLOR,
            batch=window.get_batch("path"),
            thickness=3
        )
        self.target_marker = pyglet.shapes.Arc(
            0, 0, 12, segments=30,
            color=self.AGENT_COLOR,
            batch=window.get_batch("path"),
            thickness=3
        )
        self.start_marker.visible = False
        self.target_marker.visible = False
        self.render_path = []

        self.start_idx = 0
        self.target_idx = 10
        self.world = None

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
        # clear old path lines and draw new ones
        for line in self.render_path:
            try:
                line.delete()
            except:
                pass
        self.render_path = []
        for i in range(len(self.path) - 1):
            a = self.path[i].center()
            b = self.path[i + 1].center()
            self.render_path.append(
                pyglet.shapes.Line(
                    a.x, a.y, b.x, b.y,
                    width=2,
                    color=self.AGENT_COLOR,
                    batch=window.get_batch("path")
                )
            )

    def update(self, dt):
        ''' Move toward the next node in the path each frame. '''
        if not self.active:
            return
        if self.path_idx >= len(self.path) - 1:
            # Should randomly pick new target that is : not wall, not current target and current target become new start
            newTarget = random.randint(0, len(self.world.boxes) - 1)
            while newTarget == self.target_idx or newTarget == self.start_idx or self.world.boxes[newTarget].type == "WALL":
                newTarget = random.randint(0, len(self.world.boxes) - 1)
            self.start_idx = self.target_idx
            self.target_idx = newTarget
            # Should call plan path here
            self.plan_path(self.world)
            

            # self.active = False
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

    def current_tile_idx(self):
        if self.world is None:
            return None
        box = self.world.get_box_by_pos(self.x, self.y)
        return box.index if box else None

class GroundAgent(Agent):
    def __init__(self):
        super().__init__()

    def plan_path(self, world):
        self.world = world
        result = world.plan_path(self.SEARCH_ASTAR, self.SEARCH_NO_LIMIT, world.graph, self.start_idx, self.target_idx)
        if result and result.path:
            self.set_path(world.boxes, result.path)
            self.start_marker.x = world.boxes[self.start_idx].center().x
            self.start_marker.y = world.boxes[self.start_idx].center().y
            self.start_marker.visible = True
            self.target_marker.x = world.boxes[self.target_idx].center().x
            self.target_marker.y = world.boxes[self.target_idx].center().y
            self.target_marker.visible = True

class FlyingAgent(Agent):
    AGENT_COLOR = COLOUR_NAMES['BLUE']

    def __init__(self):
        super().__init__()

    def plan_path(self, world):
        self.world = world
        result = world.plan_path(self.SEARCH_ASTAR, self.SEARCH_NO_LIMIT, world.sky_graph, self.start_idx, self.target_idx)
        if result and result.path:
            self.set_path(world.boxes, result.path)
            self.start_marker.x = world.boxes[self.start_idx].center().x
            self.start_marker.y = world.boxes[self.start_idx].center().y
            self.start_marker.visible = True
            self.target_marker.x = world.boxes[self.target_idx].center().x
            self.target_marker.y = world.boxes[self.target_idx].center().y
            self.target_marker.visible = True