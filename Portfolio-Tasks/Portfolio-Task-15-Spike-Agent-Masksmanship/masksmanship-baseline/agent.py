import pyglet
import math
import random
from vector2d import Vector2D
from graphics import COLOUR_NAMES, window

MAX_SPREAD_RADIANS = math.radians(30)  # max spread at 0% accuracy
WAYPOINT_REACH_DIST = 20.0             # pixels — counts as "reached"


class TargetAgent:

    def __init__(self, world, waypoints):
        self.world = world
        self.waypoints = waypoints
        self.waypoint_idx = 0

        self.pos = waypoints[0].copy()
        self.vel = Vector2D()
        self.heading = Vector2D(1, 0)
        self.mass = 1.0
        self.max_speed = 120.0
        self.max_force = 500.0

        self.hit_flash = 0.0  # seconds remaining for red flash on hit

        self.shape = pyglet.shapes.Triangle(
            self.pos.x + 12, self.pos.y,
            self.pos.x - 12, self.pos.y + 8,
            self.pos.x - 12, self.pos.y - 8,
            color=COLOUR_NAMES['AQUA'],
            batch=window.get_batch("main")
        )

    @property
    def current_waypoint(self):
        return self.waypoints[self.waypoint_idx]

    def update(self, dt):
        # Hit flash visual feedback
        if self.hit_flash > 0:
            self.hit_flash -= dt
            self.shape.color = COLOUR_NAMES['RED']
        else:
            self.shape.color = COLOUR_NAMES['AQUA']

        # Advance to next waypoint when close enough
        if self.pos.distance(self.current_waypoint) < WAYPOINT_REACH_DIST:
            self.waypoint_idx = (self.waypoint_idx + 1) % len(self.waypoints)

        # Seek force toward current waypoint
        desired = (self.current_waypoint - self.pos)
        desired.normalise()
        desired *= self.max_speed
        force = desired - self.vel

        # Physics integration — same pattern as Task 14, already working
        force.truncate(self.max_force)
        accel = force / self.mass
        self.vel += accel * dt
        self.vel.truncate(self.max_speed)
        self.pos += self.vel * dt

        if self.vel.lengthSq() > 0.001:
            self.heading = self.vel.get_normalised()

        # Sync visual
        self.shape.x = self.pos.x
        self.shape.y = self.pos.y
        self.shape.rotation = -self.heading.angle_degrees()

    def register_hit(self):
        self.hit_flash = 0.3


class AttackerAgent:

    def __init__(self, world, pos):
        self.world = world
        self.pos = pos.copy()
        self.fire_cooldown = 0.0

        self.shape = pyglet.shapes.Circle(
            self.pos.x, self.pos.y, 16,
            color=COLOUR_NAMES['BLUE'],
            batch=window.get_batch("main")
        )

        # Debug visuals — visible when [I] is pressed
        # Red line: attacker → predicted interception point
        self._aim_line = pyglet.shapes.Line(
            self.pos.x, self.pos.y,
            self.pos.x, self.pos.y,
            1, color=COLOUR_NAMES['RED'],
            batch=window.get_batch("info")
        )
        # Green circle: predicted interception point
        self._crosshair = pyglet.shapes.Circle(
            self.pos.x, self.pos.y, 8,
            color=COLOUR_NAMES['GREEN'],
            batch=window.get_batch("info")
        )

    def update(self, dt, target, weapon):
        self.fire_cooldown -= dt
        if self.fire_cooldown <= 0:
            self.fire(target, weapon)
            self.fire_cooldown = 1.0 / weapon.fire_rate

    def calculate_interception(self, target, projectile_speed):
        """Return the predicted world position to aim at so the projectile meets the target."""
        rel_pos = target.pos - self.pos
        tv = target.vel

        a = tv.dot(tv) - projectile_speed ** 2
        b = 2 * rel_pos.dot(tv)
        c = rel_pos.dot(rel_pos)

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return target.pos.copy()

        sqrt_disc = math.sqrt(discriminant)
        t1 = (-b - sqrt_disc) / (2 * a) if abs(a) > 1e-6 else float('inf')
        t2 = (-b + sqrt_disc) / (2 * a) if abs(a) > 1e-6 else float('inf')

        # Pick the smallest positive t
        t = None
        for candidate in sorted([t1, t2]):
            if candidate > 0:
                t = candidate
                break

        if t is None:
            return target.pos.copy()

        return target.pos + target.vel * t

    def _apply_inaccuracy(self, direction, accuracy):
        """Return a copy of direction rotated by a random angle scaled by (1 - accuracy)."""
        spread = (1.0 - accuracy) * MAX_SPREAD_RADIANS
        angle = random.uniform(-spread, spread)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        new_x = direction.x * cos_a - direction.y * sin_a
        new_y = direction.x * sin_a + direction.y * cos_a
        return Vector2D(new_x, new_y)

    def fire(self, target, weapon):
        from projectile import Projectile

        aim_point = self.calculate_interception(target, weapon.projectile_speed)

        direction = (aim_point - self.pos)
        direction.normalise()
        direction = self._apply_inaccuracy(direction, weapon.accuracy)

        vel = direction * weapon.projectile_speed
        self.world.projectiles.append(Projectile(self.pos, vel))

        # Update debug visuals
        self._aim_line.x2 = aim_point.x
        self._aim_line.y2 = aim_point.y
        self._crosshair.x = aim_point.x
        self._crosshair.y = aim_point.y
