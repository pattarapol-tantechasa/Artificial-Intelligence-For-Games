"""Boid Agent — Emergent Group Behaviour (Extensions).

Adds on top of the baseline:
  Ext 1 — Non-overlapping: rigid body collision handled in world.py
  Ext 2 — Predator avoidance: prey flee from predator agents
  Ext 3 — Wall avoidance: feeler raycasting steers agents away from walls
  Ext 4 — Factional behaviour: prey, predator fish, and scavenger factions
           each with unique steering configurations and cross-faction dynamics
"""

import pyglet
from vector2d import Vector2D, Point2D
from graphics import COLOUR_NAMES, window
from math import sin, cos, radians, degrees
from random import random, randrange, uniform

# Faction constants
PREY      = 0
PREDATOR  = 1
SCAVENGER = 2


class Agent(object):
    """A boid agent supporting faction-based steering and wall avoidance."""

    def __init__(self, world=None, scale=30.0, mass=1.0,
                 color='AQUA', max_speed=None, max_force=None,
                 vehicle_size=1.0, wander_jitter=15.0,
                 faction=PREY, agent_radius=10.0):
        self.world = world
        self.faction = faction
        self.agent_radius = agent_radius

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

        # Debug: neighbourhood radius ring (info batch)
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
        """Faction-specific weighted-sum steering."""
        if self.faction == PREDATOR:
            force = self._calculate_predator(delta)
        elif self.faction == SCAVENGER:
            force = self._calculate_scavenger(delta)
        else:
            force = self._calculate_prey(delta)
        self.force = force
        return force

    def _calculate_prey(self, delta):
        neighbours = self.get_neighbours()
        return (
            self.wander(delta)          * self.world.w_wander        +
            self.cohesion(neighbours)   * self.world.w_cohesion      +
            self.separation(neighbours) * self.world.w_separation    +
            self.alignment(neighbours)  * self.world.w_alignment     +
            self.flee_predator()        * self.world.w_flee_predator +
            self.wall_avoidance()       * self.world.w_wall
        )

    def _calculate_predator(self, delta):
        # Predators seek nearest prey and avoid walls
        return (
            self.wander(delta)    * 0.3             +
            self.seek_nearest_prey() * 2.0          +
            self.wall_avoidance() * self.world.w_wall
        )

    def _calculate_scavenger(self, delta):
        # Scavengers flock among themselves and loosely trail predators
        neighbours = self.get_neighbours()
        return (
            self.wander(delta)          * self.world.w_wander     +
            self.cohesion(neighbours)   * self.world.w_cohesion   +
            self.separation(neighbours) * self.world.w_separation +
            self.alignment(neighbours)  * self.world.w_alignment  +
            self.follow_predators()     * 1.5                     +
            self.wall_avoidance()       * self.world.w_wall
        )

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
    # Neighbourhood (faction-filtered)
    # ------------------------------------------------------------------ #

    def get_neighbours(self):
        """Return same-faction agents within neighbour_radius."""
        neighbours = []
        r = self.world.neighbour_radius
        for agent in self.world.agents:
            if agent is self or agent.faction != self.faction:
                continue
            if self.pos.distance(agent.pos) < r:
                neighbours.append(agent)
        return neighbours

    # ------------------------------------------------------------------ #
    # Group steering behaviours (unchanged from baseline)
    # ------------------------------------------------------------------ #

    def cohesion(self, neighbours):
        if not neighbours:
            return Vector2D()
        avg = Vector2D()
        for n in neighbours:
            avg += n.pos
        avg /= len(neighbours)
        return self.seek(avg)

    def separation(self, neighbours):
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
    # Ext 2: Predator avoidance
    # ------------------------------------------------------------------ #

    def flee_predator(self):
        """Flee from predator agents within panic radius."""
        if not self.world.predators:
            return Vector2D()
        PANIC_RADIUS = 160.0
        steer = Vector2D()
        for pred in self.world.predators:
            dist = self.pos.distance(pred.pos)
            if dist < PANIC_RADIUS:
                away = self.pos - pred.pos
                away.normalise()
                steer += away * (PANIC_RADIUS / max(dist, 0.001))
        return steer

    def seek_nearest_prey(self):
        """Predator steers toward the nearest prey agent."""
        prey_agents = [a for a in self.world.agents if a.faction == PREY]
        if not prey_agents:
            return Vector2D()
        nearest = min(prey_agents, key=lambda a: self.pos.distance(a.pos))
        return self.seek(nearest.pos)

    # ------------------------------------------------------------------ #
    # Ext 4: Factional — scavenger behaviour
    # ------------------------------------------------------------------ #

    def follow_predators(self):
        """Scavenger trails the predator group from a comfortable distance."""
        if not self.world.predators:
            return Vector2D()
        avg = Vector2D()
        for pred in self.world.predators:
            avg += pred.pos
        avg /= len(self.world.predators)
        dist = self.pos.distance(avg)
        FOLLOW_DIST = 130.0
        if dist < FOLLOW_DIST:
            return Vector2D()
        return self.seek(avg)

    # ------------------------------------------------------------------ #
    # Ext 3: Wall avoidance via feeler raycasting
    # ------------------------------------------------------------------ #

    def wall_avoidance(self):
        """Three forward feelers detect the nearest wall and steer away using
        velocity-space forces (same scale as seek/flee so they properly compete
        with cohesion and other behaviours)."""
        if not self.world.walls:
            return Vector2D()
        FEELER_LEN = 120.0
        SIDE_LEN   = FEELER_LEN * 0.65
        SIDE_ANGLE = radians(35)

        feelers = [
            self._feeler_endpoint(0,            FEELER_LEN),
            self._feeler_endpoint( SIDE_ANGLE,  SIDE_LEN),
            self._feeler_endpoint(-SIDE_ANGLE,  SIDE_LEN),
        ]

        # Find the single closest wall intersection across all feelers
        closest_dist   = float('inf')
        closest_normal = None

        for feeler_end in feelers:
            for wall in self.world.walls:
                hit, hit_pt, normal = self._ray_segment_intersect(feeler_end, wall)
                if hit:
                    dist = self.pos.distance(hit_pt)
                    if dist < closest_dist:
                        closest_dist   = dist
                        closest_normal = normal

        if closest_normal is None:
            return Vector2D()

        # Desired velocity = full speed perpendicular away from wall.
        # This matches the velocity-space scale of seek/flee so the weight
        # in the weighted-sum can be compared fairly.
        desired = closest_normal * self.max_speed
        # Scale up as the agent gets closer (closer hit → stronger turn)
        scale = FEELER_LEN / max(closest_dist, 1.0)
        return (desired - self.vel) * scale

    def _feeler_endpoint(self, angle_offset, length):
        """Return world-space endpoint of a feeler rotated by angle_offset from heading."""
        hx = self.heading.x * cos(angle_offset) - self.heading.y * sin(angle_offset)
        hy = self.heading.x * sin(angle_offset) + self.heading.y * cos(angle_offset)
        return self.pos + Vector2D(hx, hy) * length

    def _ray_segment_intersect(self, feeler_end, wall):
        """
        Test if the ray (self.pos -> feeler_end) hits the wall segment.
        Returns (hit, hit_point, outward_normal).
        """
        r = feeler_end - self.pos
        s = wall.p2 - wall.p1

        denom = r.x * s.y - r.y * s.x
        if abs(denom) < 0.0001:
            return False, None, None

        w = wall.p1 - self.pos
        t = (w.x * s.y - w.y * s.x) / denom
        u = (w.x * r.y - w.y * r.x) / denom

        if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
            hit_pt = self.pos + r * t
            normal = Vector2D(-s.y, s.x)
            normal.normalise()
            # Ensure normal points toward the agent
            if normal.dot(self.pos - wall.p1) < 0:
                normal = Vector2D(s.y, -s.x)
                normal.normalise()
            return True, hit_pt, normal
        return False, None, None

    # ------------------------------------------------------------------ #
    # Primitive steering
    # ------------------------------------------------------------------ #

    def seek(self, target_pos):
        desired = (target_pos - self.pos).normalise() * self.max_speed
        return desired - self.vel

    def wander(self, delta):
        jitter = self.wander_jitter * delta
        self.wander_target += Vector2D(uniform(-1, 1) * jitter,
                                       uniform(-1, 1) * jitter)
        self.wander_target.normalise()
        self.wander_target *= self.wander_radius
        target_local = self.wander_target + Vector2D(self.wander_dist, 0)
        world_target = self.world.transform_point(
            target_local, self.pos, self.heading, self.side)
        return self.seek(world_target)
