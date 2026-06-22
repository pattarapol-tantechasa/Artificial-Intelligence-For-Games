import pyglet
import math
import random
from vector2d import Vector2D
from graphics import COLOUR_NAMES, window

MAX_SPREAD_RADIANS = math.radians(30)  # max spread at 0% accuracy
WAYPOINT_REACH_DIST = 20.0             # pixels — counts as "reached"
PROXIMITY_OFFSET = 30.0                # px below predicted body — grenade aims at "feet"

# Target agent states
PATROL     = 'PATROL'
EVADE      = 'EVADE'
SEEK_COVER = 'SEEK_COVER'

# Evasion thresholds
THREAT_SPEED_MAX      = 200.0   # px/s — only evade projectiles slower than this
THREAT_DETECT_RADIUS  = 200.0   # px — detection range for incoming threats
COVER_SEEK_THRESHOLD  = 220.0   # px — prefer cover over raw flee if obstacle within this range
COVER_PADDING         = 30.0    # px — how far behind obstacle to hide
OBSTACLE_AVOID_RADIUS = 55.0    # px — push-away buffer beyond obstacle radius
ARRIVE_SLOWING_RADIUS = 80.0    # px — start decelerating when this close to cover point


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
        self.state = PATROL

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

        # --- State machine ---
        threat = self._detect_threat()

        if threat is not None:
            cover = self._find_nearest_cover()
            if cover is not None and self.pos.distance(cover.pos) < COVER_SEEK_THRESHOLD:
                # Close enough to an obstacle — hide behind it
                self.state = SEEK_COVER
                cover_pos = self._calculate_cover_pos(cover)
                force = self._arrive(cover_pos)
            else:
                # No reachable cover — flee from the incoming projectile
                self.state = EVADE
                force = self._flee(threat)
        else:
            # No threat — resume waypoint patrol
            self.state = PATROL
            if self.pos.distance(self.current_waypoint) < WAYPOINT_REACH_DIST:
                self.waypoint_idx = (self.waypoint_idx + 1) % len(self.waypoints)
            desired = (self.current_waypoint - self.pos)
            desired.normalise()
            desired *= self.max_speed
            force = desired - self.vel

        # Obstacle avoidance added to all states
        force += self._avoid_obstacles()

        # Physics integration
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

    # ------------------------------------------------------------------ #
    # Evasion helpers
    # ------------------------------------------------------------------ #

    def _detect_threat(self):
        """Return the closest slow projectile within detection range, or None."""
        from projectile import ExplosiveProjectile
        closest = None
        closest_dist = THREAT_DETECT_RADIUS
        for proj in self.world.projectiles:
            if not proj.active:
                continue
            if isinstance(proj, ExplosiveProjectile):
                continue  # explosions can't be dodged
            if proj.vel.length() > THREAT_SPEED_MAX:
                continue  # too fast to evade
            dist = self.pos.distance(proj.pos)
            if dist < closest_dist:
                closest_dist = dist
                closest = proj
        return closest

    def _find_nearest_cover(self):
        """Return the closest obstacle, or None if none exist."""
        if not self.world.obstacles:
            return None
        return min(self.world.obstacles, key=lambda o: self.pos.distance(o.pos))

    def _calculate_cover_pos(self, obstacle):
        """Return the point directly behind the obstacle from the attacker's perspective."""
        direction = (obstacle.pos - self.world.attacker.pos)
        direction.normalise()
        return obstacle.pos + direction * (obstacle.radius + COVER_PADDING)

    def _flee(self, threat):
        """Steer directly away from the threat's current position."""
        desired = (self.pos - threat.pos)
        desired.normalise()
        desired *= self.max_speed
        return desired - self.vel

    def _arrive(self, target_pos):
        """Seek with smooth deceleration as the target position is approached."""
        to_target = target_pos - self.pos
        dist = to_target.length()
        if dist < 1.0:
            return Vector2D()
        speed = self.max_speed if dist > ARRIVE_SLOWING_RADIUS else self.max_speed * (dist / ARRIVE_SLOWING_RADIUS)
        desired = to_target * (speed / dist)
        return desired - self.vel

    def _avoid_obstacles(self):
        """Gentle push force away from any obstacle that is too close."""
        steer = Vector2D()
        for obs in self.world.obstacles:
            dist = self.pos.distance(obs.pos)
            min_dist = obs.radius + OBSTACLE_AVOID_RADIUS
            if 0.001 < dist < min_dist:
                away = self.pos - obs.pos
                away.normalise()
                steer += away * ((min_dist - dist) / min_dist) * self.max_force
        return steer

    def register_hit(self):
        self.hit_flash = 0.3


class AttackerAgent:

    def __init__(self, world, pos):
        self.world = world
        self.pos = pos.copy()
        self.fire_cooldown = 0.0

        # Movement state (used when closing range for shotgun)
        self.vel = Vector2D()
        self.heading = Vector2D(1, 0)
        self.mass = 1.0
        self.max_speed = 180.0
        self.max_force = 800.0

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
        if weapon.effective_range is not None:
            # Shotgun mode: close the distance first, then fire
            dist = self.pos.distance(target.pos)
            if dist > weapon.effective_range:
                self._move_toward(target, dt)
            else:
                self._brake(dt)
                self.fire_cooldown -= dt
                if self.fire_cooldown <= 0:
                    self._fire_shotgun(target, weapon)
                    self.fire_cooldown = 1.0 / weapon.fire_rate
        elif weapon.blast_radius is not None:
            # Explosive mode: aim near target's feet and detonate on arrival
            self.fire_cooldown -= dt
            if self.fire_cooldown <= 0:
                self._fire_explosive(target, weapon)
                self.fire_cooldown = 1.0 / weapon.fire_rate
        else:
            # Standard mode: stay still and fire on cooldown
            self.fire_cooldown -= dt
            if self.fire_cooldown <= 0:
                self.fire(target, weapon)
                self.fire_cooldown = 1.0 / weapon.fire_rate

        # Sync shape and aim line start to current position
        self.shape.x = self.pos.x
        self.shape.y = self.pos.y
        self._aim_line.x = self.pos.x
        self._aim_line.y = self.pos.y

    def _move_toward(self, target, dt):
        """Seek toward the target to close the distance."""
        desired = (target.pos - self.pos)
        desired.normalise()
        desired *= self.max_speed
        force = desired - self.vel
        force.truncate(self.max_force)
        self.vel += (force / self.mass) * dt
        self.vel.truncate(self.max_speed)
        self.pos += self.vel * dt
        if self.vel.lengthSq() > 0.001:
            self.heading = self.vel.get_normalised()

    def _brake(self, dt):
        """Quickly decelerate to a stop once in firing range."""
        self.vel *= max(0.0, 1.0 - 12.0 * dt)
        self.pos += self.vel * dt

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

    def _fire_shotgun(self, target, weapon):
        """Fire multiple pellets in a spread cone — each pellet gets its own random angle."""
        from projectile import Projectile

        aim_point = self.calculate_interception(target, weapon.projectile_speed)
        base_dir = (aim_point - self.pos)
        base_dir.normalise()

        for _ in range(weapon.pellets_per_shot):
            angle = random.uniform(-weapon.spread_angle_maximum, weapon.spread_angle_maximum)
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            px = base_dir.x * cos_a - base_dir.y * sin_a
            py = base_dir.x * sin_a + base_dir.y * cos_a
            self.world.projectiles.append(Projectile(self.pos, Vector2D(px, py) * weapon.projectile_speed))

        # Update debug visuals
        self._aim_line.x2 = aim_point.x
        self._aim_line.y2 = aim_point.y
        self._crosshair.x = aim_point.x
        self._crosshair.y = aim_point.y

    def _fire_explosive(self, target, weapon):
        """Fire an explosive projectile aimed at the target's proximity (feet offset).

        Rather than aiming at the target's body, we aim slightly below the predicted
        position so the projectile detonates near the ground at their feet. The blast
        radius then catches the target even without a direct body hit.
        """
        from projectile import ExplosiveProjectile

        predicted = self.calculate_interception(target, weapon.projectile_speed)
        # Shift aim point downward — proximity/feet targeting
        aim_point = predicted + Vector2D(0, -PROXIMITY_OFFSET)

        direction = (aim_point - self.pos)
        direction.normalise()
        vel = direction * weapon.projectile_speed

        self.world.projectiles.append(
            ExplosiveProjectile(self.pos, vel, aim_point, self.world, weapon.blast_radius)
        )

        # Update debug visuals — crosshair shows the proximity aim point, not the body
        self._aim_line.x2 = aim_point.x
        self._aim_line.y2 = aim_point.y
        self._crosshair.x = aim_point.x
        self._crosshair.y = aim_point.y
