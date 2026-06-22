"""World Environment for Steering Simulation.

This module defines the World class, which manages the simulation space, 
the target object, and the collection of agents. It handles spatial 
constraints (like toroidal wrap-around) and routes input events to 
relevant simulation entities.

Created by
    Clinton Woodward (2019)
    James Bonner (2024)
    contact: jbonner@swin.edu.au

Comments and code refactored by Enrique Ketterer <ekettererortiz@swin.edu.au>
- S1 2026

For class use only. Do not publicly share or post this code without permission.
"""

from vector2d import Vector2D
from matrix33 import Matrix33
from random import randrange
import pyglet
from graphics import COLOUR_NAMES, window
from agent import Agent, AGENT_MODES


def _ray_intersects_circle(start, end, center, radius):
    """Returns True if the line segment start→end passes through a circle."""
    d = end - start
    f = start - center
    a = d.dot(d)
    b = 2.0 * f.dot(d)
    c = f.dot(f) - radius * radius
    discriminant = b * b - 4.0 * a * c
    if discriminant < 0:
        return False
    sq = discriminant ** 0.5
    t1 = (-b - sq) / (2.0 * a)
    t2 = (-b + sq) / (2.0 * a)
    return (0.0 <= t1 <= 1.0) or (0.0 <= t2 <= 1.0)


def _has_line_of_sight(hunter_pos, prey_pos, obstacles):
    """Returns True if no obstacle blocks the ray from hunter to prey."""
    for obs in obstacles:
        if _ray_intersects_circle(hunter_pos, prey_pos, obs.pos, obs.radius):
            return False
    return True


class Obstacle:
    """A static circular obstacle agents can hide behind."""
    def __init__(self, x, y, radius):
        self.pos = Vector2D(x, y)
        self.radius = radius
        self.shape = pyglet.shapes.Circle(
            x, y, radius,
            color=COLOUR_NAMES['DARK_GREEN'],
            batch=window.get_batch("main")
        )


class World(object):
    """The simulation container holding agents and environmental state."""

    def __init__(self, cx, cy):
        # Dimensions of the world
        self.cx = cx
        self.cy = cy

        # State flags
        self.paused = True
        self.show_info = True

        # Simulation entities
        self.agents = []
        self.hunters = []
        self.prey = None

        # Static obstacles spread across the window
        self.obstacles = [
            Obstacle(200, 400, 50),
            Obstacle(500, 250, 60),
            Obstacle(750, 500, 45),
            Obstacle(350, 550, 55),
            Obstacle(650, 150, 50),
        ]

        # Calculated each frame: one hide spot per obstacle
        self.hide_spots = []
        self.best_hide_spot = None

        # Score counter
        self.score = 0
        self.score_label = pyglet.text.Label(
            'Caught: 0',
            font_size=16,
            x=10, y=cy - 30,
            color=COLOUR_NAMES['WHITE'],
            batch=window.get_batch("main")
        )

        # One orange chase line per hunter (3 hunters)
        self.chase_lines = []
        for _ in range(3):
            line = pyglet.shapes.Line(0, 0, 1, 1,
                color=COLOUR_NAMES['ORANGE'],
                batch=window.get_batch("main"))
            line.visible = False
            self.chase_lines.append(line)

        # "x" marker visuals — two crossing lines per obstacle
        M = 8  # half-size of the x marker in pixels
        self._marker_half = M
        self.hide_markers = []
        for _ in self.obstacles:
            l1 = pyglet.shapes.Line(0, 0, 1, 1,
                                    color=COLOUR_NAMES['WHITE'],
                                    batch=window.get_batch("main"))
            l2 = pyglet.shapes.Line(0, 0, 1, 1,
                                    color=COLOUR_NAMES['WHITE'],
                                    batch=window.get_batch("main"))
            self.hide_markers.append((l1, l2))

    def _calculate_hide_spots(self):
        """Recalculates all hide spots relative to the nearest hunter."""
        BUFFER = 20.0
        M = self._marker_half

        if not self.hunters or self.prey is None:
            return

        # Use the nearest hunter as the primary threat
        nearest = min(self.hunters, key=lambda h: h.pos.distance(self.prey.pos))

        spots = []
        for obs in self.obstacles:
            to_obs = obs.pos - nearest.pos
            if to_obs.length() < 0.001:
                spots.append(obs.pos.copy())
                continue
            to_obs.normalise()
            spot = obs.pos + to_obs * (obs.radius + BUFFER)
            spots.append(spot)

        self.hide_spots = spots

        # Best = lowest danger-aware score (distance + exposure penalty)
        EXPOSURE_WEIGHT = 2.0
        best_idx = -1
        if spots:
            def score(i):
                dist = self.prey.pos.distance(spots[i])
                exposure = self.prey.path_exposure(spots[i])
                return dist + exposure * EXPOSURE_WEIGHT

            best_idx = min(range(len(spots)), key=score)
            self.best_hide_spot = spots[best_idx]

        # Update x marker line positions and colours
        for i, (spot, (l1, l2)) in enumerate(zip(spots, self.hide_markers)):
            color = COLOUR_NAMES['YELLOW'] if i == best_idx else COLOUR_NAMES['WHITE']
            l1.x,  l1.y  = spot.x - M, spot.y - M
            l1.x2, l1.y2 = spot.x + M, spot.y + M
            l1.color = color
            l2.x,  l2.y  = spot.x - M, spot.y + M
            l2.x2, l2.y2 = spot.x + M, spot.y - M
            l2.color = color

    def _update_hunter_state(self):
        """Switches each hunter between wander and chase based on line-of-sight to prey."""
        if not self.hunters or self.prey is None:
            return
        for i, hunter in enumerate(self.hunters):
            can_see = _has_line_of_sight(hunter.pos, self.prey.pos, self.obstacles)
            hunter.mode = 'chase' if can_see else 'wander'
            line = self.chase_lines[i]
            if can_see:
                line.x,  line.y  = hunter.pos.x, hunter.pos.y
                line.x2, line.y2 = self.prey.pos.x, self.prey.pos.y
                line.visible = True
            else:
                line.visible = False

    def _check_catch(self):
        """Respawns prey if any hunter catches it."""
        CATCH_RADIUS = 25.0
        if not self.hunters or self.prey is None:
            return
        for hunter in self.hunters:
            if hunter.pos.distance(self.prey.pos) < CATCH_RADIUS:
                self.score += 1
                self.score_label.text = f'Caught: {self.score}'
                self.prey.pos.x = randrange(self.cx)
                self.prey.pos.y = randrange(self.cy)
                self.prey.vel.x = 0.0
                self.prey.vel.y = 0.0
                break

    def update(self, delta):
        """Advances the simulation by one tick."""
        if not self.paused:
            self._update_hunter_state()
            self._calculate_hide_spots()
            self._check_catch()
            for agent in self.agents:
                agent.update(delta)

    def wrap_around(self, pos):
        """Treats the world as a toroidal (wrap-around) space.
        
        Updates the x and y coordinates of the provided position object.
        """
        if pos.x > self.cx:
            pos.x -= self.cx
        elif pos.x < 0:
            pos.x += self.cx
            
        if pos.y > self.cy:
            pos.y -= self.cy
        elif pos.y < 0:
            pos.y += self.cy

    def transform_points(self, points, pos, forward, side, scale):
        """Transforms a list of local space points into world space.
        
        Useful for rendering complex shapes that rotate and scale with an agent.
        """
        # Create copies of points to avoid mutating the original definitions
        world_pts = [pt.copy() for pt in points]
        
        # Construct transformation matrix
        mat = Matrix33()
        mat.scale_update(scale.x, scale.y)
        mat.rotate_by_vectors_update(forward, side)
        mat.translate_update(pos.x, pos.y)
        
        # Apply transformation
        mat.transform_vector2d_list(world_pts)
        return world_pts

    def transform_point(self, point, pos, forward, side):
        """Transforms a single local space point into world space."""
        world_pt = point.copy()
        mat = Matrix33()
        mat.rotate_by_vectors_update(forward, side)
        mat.translate_update(pos.x, pos.y)
        mat.transform_vector2d(world_pt)
        return world_pt
    
    def input_mouse(self, x, y, button, modifiers):
        pass

    def input_keyboard(self, symbol, modifiers):
        """Handles keyboard events."""
        if symbol == pyglet.window.key.P:
            self.paused = not self.paused
        elif symbol == pyglet.window.key.I:
            self.show_info = not self.show_info