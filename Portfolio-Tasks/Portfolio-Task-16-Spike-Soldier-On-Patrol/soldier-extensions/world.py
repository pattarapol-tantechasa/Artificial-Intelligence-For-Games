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
import pyglet
from graphics import COLOUR_NAMES, window
from agent import Agent, AGENT_MODES
from enemy import Enemy
from healing_station import HealingStation

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
        self.enemies = []
        self.projectiles = []
        self.hunter = None
        self.healing_station = HealingStation(self)

    def update(self, delta):
        """Advances the simulation by one tick."""
        if not self.paused:
            for agent in self.agents:
                agent.update(delta)
            for enemy in self.enemies:
                enemy.update(delta)
            for proj in self.projectiles:
                proj.update(delta)
            self.projectiles = [p for p in self.projectiles if p.active]
            self.enemies = [e for e in self.enemies if e.alive]
        self._update_hud()

    def spawn_enemy(self):
        self.enemies.append(Enemy(self))

    def _update_hud(self):
        lines = []
        for i, agent in enumerate(self.agents):
            state = agent.current_state
            state_name = type(state).__name__ if state else '-'
            extra = state.status() if state else ''
            lines.append(f'S{i+1}: {state_name} {extra}  [{int(agent.health)}hp]')
        lines.append(f'Enemies: {len(self.enemies)}')
        lines.append('[E] Spawn Enemy   [P] Pause')
        window.labels['mode'].text = '\n'.join(lines)

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
        elif symbol == pyglet.window.key.E:
            self.spawn_enemy()