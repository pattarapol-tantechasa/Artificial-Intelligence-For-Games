"""Boid Agent with Emergent Group Steering Behaviours.

Implements cohesion, separation, alignment, and wandering, combined via a
weighted-sum approach to produce emergent flocking behaviour.
"""

import pyglet
from vector2d import Vector2D, Point2D
from graphics import COLOUR_NAMES, window
from math import sin, cos, radians
from random import random, randrange, uniform


class Agent(object):
    """A boid agent that flocks with its neighbours."""

    def __init__(self, world=None, scale=30.0, mass=1.0,
                 color='AQUA', max_speed=None, max_force=None,
                 vehicle_size=1.0, wander_jitter=15.0):
        self.world = world

        # Physics state
        angle = radians(random() * 360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(angle), cos(angle))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)
        self.mass = mass

        self.force = Vector2D()
        self.accel = Vector2D()
        self.max_speed = max_speed if max_speed is not None else 20.0 * scale
        self.max_force = max_force if max_force is not None else 100.0 * scale

        # Visual triangle
        self.color = color
        s = vehicle_size
        self.vehicle = pyglet.shapes.Triangle(
            self.pos.x + 10 * s, self.pos.y,
            self.pos.x - 10 * s, self.pos.y + 6 * s,
            self.pos.x - 10 * s, self.pos.y - 6 * s,
            color=COLOUR_NAMES[self.color],
            batch=window.get_batch("main")
        )

        # Debug: neighbourhood radius ring (shown in info batch when [I] is pressed)
        self.info_nbr_circle = pyglet.shapes.Arc(
            self.pos.x, self.pos.y,
            world.neighbour_radius,
            color=COLOUR_NAMES['GREY'],
            batch=window.get_batch("info")
        )

        # Wander state
        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 2.0 * scale
        self.wander_radius = 1.5 * scale
        self.wander_jitter = wander_jitter

    # ------------------------------------------------------------------ #
    # Core loop
    # ------------------------------------------------------------------ #

    def calculate(self, delta):
        """Weighted-sum of all active steering forces."""
        neighbours = self.get_neighbours()

        force = (
            self.wander(delta)          * self.world.w_wander     +
            self.cohesion(neighbours)   * self.world.w_cohesion   +
            self.separation(neighbours) * self.world.w_separation +
            self.alignment(neighbours)  * self.world.w_alignment
        )
        self.force = force
        return force

    def update(self, delta):
        """Physics integration and visual update."""
        force = self.calculate(delta)
        force.truncate(self.max_force)

        self.accel = force / self.mass
        self.vel += self.accel * delta
        self.vel.truncate(self.max_speed)
        self.pos += self.vel * delta

        if self.vel.lengthSq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()

        self.world.wrap_around(self.pos)

        self.vehicle.x = self.pos.x
        self.vehicle.y = self.pos.y
        self.vehicle.rotation = -self.heading.angle_degrees()

        self.info_nbr_circle.x = self.pos.x
        self.info_nbr_circle.y = self.pos.y
        self.info_nbr_circle.radius = self.world.neighbour_radius

    def speed(self):
        return self.vel.length()

    # ------------------------------------------------------------------ #
    # Neighbourhood
    # ------------------------------------------------------------------ #

    def get_neighbours(self):
        """Return agents within neighbour_radius."""
        neighbours = []
        r = self.world.neighbour_radius
        for agent in self.world.agents:
            if agent is self:
                continue
            if self.pos.distance(agent.pos) < r:
                neighbours.append(agent)
        return neighbours

    # ------------------------------------------------------------------ #
    # Group steering behaviours
    # ------------------------------------------------------------------ #

    def cohesion(self, neighbours):
        """Steer toward the average position of neighbours."""
        if not neighbours:
            return Vector2D()
        avg = Vector2D()
        for n in neighbours:
            avg += n.pos
        avg /= len(neighbours)
        return self.seek(avg)

    def separation(self, neighbours):
        """Steer away from neighbours that are too close."""
        steer = Vector2D()
        sep_r = self.world.sep_radius
        for n in neighbours:
            dist = self.pos.distance(n.pos)
            if 0.001 < dist < sep_r:
                away = self.pos - n.pos
                away.normalise()
                steer += away * (sep_r / dist)
        return steer

    def alignment(self, neighbours):
        """Match the average heading of neighbours."""
        if not neighbours:
            return Vector2D()
        avg_heading = Vector2D()
        for n in neighbours:
            avg_heading += n.heading
        avg_heading /= len(neighbours)
        avg_heading.normalise()
        desired = avg_heading * self.max_speed
        return desired - self.vel

    # ------------------------------------------------------------------ #
    # Primitive steering behaviours
    # ------------------------------------------------------------------ #

    def seek(self, target_pos):
        """Steer directly toward a target."""
        desired = (target_pos - self.pos).normalise() * self.max_speed
        return desired - self.vel

    def wander(self, delta):
        """Random wandering using a projected jitter circle."""
        jitter = self.wander_jitter * delta
        self.wander_target += Vector2D(uniform(-1, 1) * jitter,
                                       uniform(-1, 1) * jitter)
        self.wander_target.normalise()
        self.wander_target *= self.wander_radius
        target_local = self.wander_target + Vector2D(self.wander_dist, 0)
        world_target = self.world.transform_point(
            target_local, self.pos, self.heading, self.side)
        return self.seek(world_target)
