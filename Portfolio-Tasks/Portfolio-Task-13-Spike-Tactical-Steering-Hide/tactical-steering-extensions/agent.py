"""Autonomous Agent Steering Logic.

This module defines the Agent class, which implements various steering 
behaviours such as Seek, Flee, Arrive, and placeholders for Pursuit, 
Wander, and Path Following. It handles the physics integration (force -> 
acceleration -> velocity -> position) and updates the graphical representation.

Created by
    Clinton Woodward (2019)
    James Bonner (2024)
    contact: jbonner@swin.edu.au

Comments and code refactored by Enrique Ketterer <ekettererortiz@swin.edu.au>
- S1 2026

For class use only. Do not publicly share or post this code without permission.
"""

import pyglet
from vector2d import Vector2D, Point2D
from graphics import COLOUR_NAMES, window, ArrowLine
from math import sin, cos, radians
from random import random, randrange, uniform
from path import Path

# Mapping of keyboard keys to steering modes
AGENT_MODES = {
    pyglet.window.key._1: 'seek',
    pyglet.window.key._2: 'arrive_slow',
    pyglet.window.key._3: 'arrive_normal',
    pyglet.window.key._4: 'arrive_fast',
    pyglet.window.key._5: 'flee',
    pyglet.window.key._6: 'pursuit',
    pyglet.window.key._7: 'follow_path',
    pyglet.window.key._8: 'wander',
}

class Agent(object):
    """A vehicle agent with steering behaviours."""

    # Deceleration rates for the Arrive behaviour
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        ### STUDENT TODO: ADD 'normal' and 'fast' speeds here (e.g., 0.6, 0.3)
        'normal': 0.6,
        'fast': 0.3,
    }

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='seek',
                 color='ORANGE', max_speed=None, max_force=None, vehicle_size=1.0,
                 wander_jitter=15.0):
        # Reference to the simulation world
        self.world = world
        self.mode = mode

        # Physics state: position, velocity, and orientation
        angle = radians(random() * 360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(angle), cos(angle))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)
        self.mass = mass

        # Forces and limits
        self.force = Vector2D()
        self.accel = Vector2D()
        self.max_speed = max_speed if max_speed is not None else 20.0 * scale
        self.max_force = max_force if max_force is not None else 100.0 * scale

        # ---- Graphical Representation ----
        self.color = color
        s = vehicle_size
        self.vehicle_shape = [
            Point2D(-10 * s,  6 * s),
            Point2D( 10 * s,  0),
            Point2D(-10 * s, -6 * s)
        ]

        # Main vehicle primitive
        self.vehicle = pyglet.shapes.Triangle(
            self.pos.x + self.vehicle_shape[1].x, self.pos.y + self.vehicle_shape[1].y,
            self.pos.x + self.vehicle_shape[0].x, self.pos.y + self.vehicle_shape[0].y,
            self.pos.x + self.vehicle_shape[2].x, self.pos.y + self.vehicle_shape[2].y,
            color=COLOUR_NAMES[self.color],
            batch=window.get_batch("main")
        )

        # ---- Debug/Info Visuals ----
        # Wander logic visuals (placeholders)
        self.info_wander_circle = pyglet.shapes.Circle(0, 0, 0, color=COLOUR_NAMES['WHITE'], batch=window.get_batch("info"))
        self.info_wander_target = pyglet.shapes.Circle(0, 0, 0, color=COLOUR_NAMES['GREEN'], batch=window.get_batch("info"))
        
        # Vectors: Blue = Steering Force, Aqua = Velocity, Grey = Desired Change
        self.info_force_vector = ArrowLine(Vector2D(0,0), Vector2D(0,0), colour=COLOUR_NAMES['BLUE'], batch=window.get_batch("info"))
        self.info_vel_vector = ArrowLine(Vector2D(0,0), Vector2D(0,0), colour=COLOUR_NAMES['AQUA'], batch=window.get_batch("info"))
        self.info_net_vectors = [
            ArrowLine(Vector2D(0,0), Vector2D(0,0), colour=COLOUR_NAMES['GREY'], batch=window.get_batch("info")),
            ArrowLine(Vector2D(0,0), Vector2D(0,0), colour=COLOUR_NAMES['GREY'], batch=window.get_batch("info")),
        ]

        ### STUDENT TODO: Initialise path and wander details here
        self.path = Path()
        self.randomise_path()
        self.waypoint_threshold = 20.0

        # Wander-specific state
        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 2.0 * scale
        self.wander_radius = 1.5 * scale
        self.wander_jitter = wander_jitter

    def calculate(self, delta):
        """Calculates the accumulated steering force based on the current mode."""
        mode = self.mode

        if mode == 'wander':
            force = self.wander(delta)
        elif mode == 'chase':
            force = self.pursuit(self.world.prey)
        elif mode == 'hide':
            force = self.hide()
        else:
            force = Vector2D()

        # Obstacle avoidance blended on top for all modes
        force += self.obstacle_avoidance()

        self.force = force
        return force

    def update(self, delta):
        """Updates the agent's physics and graphical representation."""
        # 1. Calculate steering force
        force = self.calculate(delta)
        force.truncate(self.max_force)

        # 2. Integrate physics: F = ma -> a = F/m
        self.accel = force / self.mass
        
        # 3. Update velocity and clamp to max speed
        self.vel += self.accel * delta
        self.vel.truncate(self.max_speed)
        
        # 4. Update position
        self.pos += self.vel * delta
        
        # 5. Update orientation if moving
        if self.vel.lengthSq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
            
        # 6. Handle world boundaries (wrap-around)
        self.world.wrap_around(self.pos)
        
        # 7. Update graphical vehicle position and rotation
        # Note: Pyglet shapes rotation is in degrees, clockwise.
        self.vehicle.x = self.pos.x
        self.vehicle.y = self.pos.y
        self.vehicle.rotation = -self.heading.angle_degrees()

        # 8. Update debug vector visuals
        s = 0.5 # Scale factor for vector drawing
        self.info_force_vector.position = self.pos
        self.info_force_vector.end_pos = self.pos + self.force * s
        
        self.info_vel_vector.position = self.pos
        self.info_vel_vector.end_pos = self.pos + self.vel * s
        
        # Net change vectors (showing how force modifies velocity)
        self.info_net_vectors[0].position = self.pos + self.vel * s
        self.info_net_vectors[0].end_pos = self.pos + (self.force + self.vel) * s
        self.info_net_vectors[1].position = self.pos
        self.info_net_vectors[1].end_pos = self.pos + (self.force + self.vel) * s

    def speed(self):
        return self.vel.length()

    # ---- Steering Behaviour Implementations ----

    def seek(self, target_pos):
        """Calculates a force to move the agent towards a target."""
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def flee(self, hunter_pos):
        ''' move away from hunter position '''
        panic_distance = 200.0
        to_hunter = hunter_pos - self.pos
        if to_hunter.length() > panic_distance:
            return Vector2D()
        desired_vel = (self.pos - hunter_pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def arrive(self, target_pos, speed):
        """Steers the agent to arrive at a target with zero velocity."""
        decel_rate = self.DECELERATION_SPEEDS.get(speed, 0.6)
        to_target = target_pos - self.pos
        dist = to_target.length()
        
        if dist > 0.1:
            # Required speed to decelerate over the remaining distance
            req_speed = dist / decel_rate
            req_speed = min(req_speed, self.max_speed)
            desired_vel = to_target * (req_speed / dist)
            return (desired_vel - self.vel)
        return Vector2D(0, 0)

    def obstacle_avoidance(self):
        """Pushes the agent away from any obstacle it gets too close to."""
        DANGER_BUFFER = 30.0
        REPULSION_STRENGTH = 15.0
        steer = Vector2D()
        for obs in self.world.obstacles:
            to_agent = self.pos - obs.pos
            dist = to_agent.length()
            danger_radius = obs.radius + DANGER_BUFFER
            if 0.001 < dist < danger_radius:
                overlap = danger_radius - dist
                steer += to_agent.normalise() * (overlap * REPULSION_STRENGTH)
                # Hard correction: physically push agent outside the obstacle if overlapping
                if dist < obs.radius:
                    self.pos = obs.pos + to_agent.normalise() * (obs.radius + 1)
        return steer

    def pursuit(self, evader):
        """Predicts the evader's future position and seeks towards it."""
        to_evader = evader.pos - self.pos
        look_ahead = to_evader.length() / (self.max_speed + evader.speed())
        future_pos = evader.pos + evader.vel * look_ahead
        return self.seek(future_pos)

    def path_exposure(self, target_spot):
        """Estimates how much danger the prey faces while travelling to a hide spot.

        Projects each hunter onto the prey→spot segment and accumulates exposure
        for any hunter whose closest point on that path is within a threat radius.
        """
        THREAT_RADIUS = 150.0
        exposure = 0.0
        to_target = target_spot - self.pos
        seg_len_sq = to_target.dot(to_target)
        if seg_len_sq < 0.001:
            return 0.0
        for hunter in self.world.hunters:
            to_hunter = hunter.pos - self.pos
            # Scalar projection of hunter onto the prey→spot segment, clamped to [0,1]
            t = max(0.0, min(1.0, to_hunter.dot(to_target) / seg_len_sq))
            closest = self.pos + to_target * t
            dist = hunter.pos.distance(closest)
            if dist < THREAT_RADIUS:
                exposure += (THREAT_RADIUS - dist)
        return exposure

    def hide(self):
        """Steers prey to the best hiding spot (closest spot behind an obstacle)."""
        spot = self.world.best_hide_spot
        if spot is None:
            return Vector2D()
        return self.arrive(spot, 'normal')

    def wander(self, delta):
        """ Random wandering using a projected jitter circle. """
        # Add a small random jitter to the target's position
        jitter = self.wander_jitter * delta
        self.wander_target += Vector2D(uniform(-1,1) * jitter, uniform(-1,1) * jitter)

        # Re-project the target back onto the unit circle and scale by radius
        self.wander_target.normalise()
        self.wander_target *= self.wander_radius

        # Project the target into world space in front of the agent
        target_local = self.wander_target + Vector2D(self.wander_dist, 0)
        world_target = self.world.transform_point(target_local, self.pos, self.heading, self.side)

        # Update debug visuals (if enabled)
        self.info_wander_target.x, self.info_wander_target.y = world_target.x, world_target.y
        
        return self.seek(world_target)

    def follow_path(self):
        """Moves the agent along a predefined set of waypoints."""
        if self.path.is_finished():
            return self.arrive(self.path.current_pt(), 'fast')
        else:
            if self.pos.distance(self.path.current_pt()) < self.waypoint_threshold:
                self.path.inc_current_pt()
            return self.seek(self.path.current_pt())

    def randomise_path(self):
        cx = self.world.cx
        cy = self.world.cy
        margin = min(cx, cy) * (1/6)
        self.path.create_random_path(5, margin, margin, cx - margin, cy - margin, looped=True)