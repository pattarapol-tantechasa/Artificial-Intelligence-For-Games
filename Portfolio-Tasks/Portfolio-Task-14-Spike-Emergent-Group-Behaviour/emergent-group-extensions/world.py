"""World Environment — Emergent Group Behaviour (Extensions).

Ext 1 — Non-overlapping: rigid-body collision resolution between all agents.
Ext 2 — Predator avoidance: tracks predator agents; prey flee from them.
Ext 3 — Wall avoidance: rectangular wall obstacle in the centre of the world.
Ext 4 — Factional behaviour: prey / predator / scavenger factions coexist.
"""

import pyglet
from vector2d import Vector2D
from matrix33 import Matrix33
from graphics import COLOUR_NAMES, window
from agent import Agent


# ------------------------------------------------------------------ #
# Wall segment
# ------------------------------------------------------------------ #

class Wall:
    """A static line-segment wall that agents avoid via feeler raycasting."""
    def __init__(self, x1, y1, x2, y2):
        self.p1 = Vector2D(x1, y1)
        self.p2 = Vector2D(x2, y2)
        self.line = pyglet.shapes.Line(
            x1, y1, x2, y2, 3,
            color=COLOUR_NAMES['WHITE'],
            batch=window.get_batch("main")
        )


# ------------------------------------------------------------------ #
# World
# ------------------------------------------------------------------ #

class World(object):
    """Simulation container for all extension behaviours."""

    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.paused = False

        # All agents (prey + predators + scavengers)
        self.agents = []

        # Predator agents referenced separately for flee/seek logic
        self.predators = []

        # ---- Flocking weights (shared by prey + scavenger) ----
        self.w_cohesion      = 1.0
        self.w_separation    = 2.0
        self.w_alignment     = 1.5
        self.w_wander        = 1.0
        self.w_flee_predator = 2.5   # Ext 2
        self.w_wall          = 0.8   # Ext 3

        # ---- Neighbourhood radii ----
        self.neighbour_radius = 100.0
        self.sep_radius       = 35.0

        # ---- Ext 3: Wall obstacle — rectangle in centre of window ----
        self.walls = self._build_walls(cx, cy)

        # ---- UI labels ----
        self._init_labels()

    # ------------------------------------------------------------------ #
    # Ext 3: Wall construction
    # ------------------------------------------------------------------ #

    def _build_walls(self, cx, cy):
        """A single horizontal wall across the centre of the world."""
        mid_x = cx // 2
        mid_y = cy // 2
        half_len = 280
        return [
            Wall(mid_x - half_len, mid_y, mid_x + half_len, mid_y),
        ]

    # ------------------------------------------------------------------ #
    # UI
    # ------------------------------------------------------------------ #

    def _init_labels(self):
        x = 10
        y_start = self.cy - 30
        step = 22
        font = 14

        entries = [
            ('lbl_cohesion',   self._cohesion_text()),
            ('lbl_separation', self._separation_text()),
            ('lbl_alignment',  self._alignment_text()),
            ('lbl_wander',     self._wander_text()),
            ('lbl_nbr',        self._nbr_text()),
            ('lbl_sep',        self._sep_text()),
            ('lbl_flee',       self._flee_text()),
            ('lbl_wall',       self._wall_text()),
            ('lbl_hint',       '[P] Pause/Resume  |  [I] Toggle neighbour rings'),
        ]

        for i, (key, text) in enumerate(entries):
            window.labels[key] = pyglet.text.Label(
                text, font_size=font,
                x=x, y=y_start - i * step,
                color=COLOUR_NAMES['WHITE']
            )

    def _update_labels(self):
        window.labels['lbl_cohesion'].text   = self._cohesion_text()
        window.labels['lbl_separation'].text = self._separation_text()
        window.labels['lbl_alignment'].text  = self._alignment_text()
        window.labels['lbl_wander'].text     = self._wander_text()
        window.labels['lbl_nbr'].text        = self._nbr_text()
        window.labels['lbl_sep'].text        = self._sep_text()
        window.labels['lbl_flee'].text       = self._flee_text()
        window.labels['lbl_wall'].text       = self._wall_text()

    def _cohesion_text(self):   return f'[Q/A] Cohesion:         {self.w_cohesion:.2f}'
    def _separation_text(self): return f'[W/S] Separation:       {self.w_separation:.2f}'
    def _alignment_text(self):  return f'[E/D] Alignment:        {self.w_alignment:.2f}'
    def _wander_text(self):     return f'[R/F] Wander:           {self.w_wander:.2f}'
    def _nbr_text(self):        return f'[T/G] Neighbour Radius: {self.neighbour_radius:.0f}'
    def _sep_text(self):        return f'[Y/H] Sep Radius:       {self.sep_radius:.0f}'
    def _flee_text(self):       return f'[U/J] Flee Predator:    {self.w_flee_predator:.2f}'
    def _wall_text(self):       return f'[O/L] Wall Avoidance:   {self.w_wall:.2f}'

    # ------------------------------------------------------------------ #
    # Simulation loop
    # ------------------------------------------------------------------ #

    def update(self, delta):
        if not self.paused:
            for agent in self.agents:
                agent.update(delta)
            self._resolve_overlaps()        # Ext 1
            self._resolve_wall_penetration()  # Ext 3 hard correction

    # ------------------------------------------------------------------ #
    # Ext 1: Non-overlapping collision resolution
    # ------------------------------------------------------------------ #

    def _resolve_overlaps(self):
        """Push apart agents whose circles physically overlap."""
        agents = self.agents
        for i in range(len(agents)):
            for j in range(i + 1, len(agents)):
                a, b = agents[i], agents[j]
                min_dist = a.agent_radius + b.agent_radius
                diff = b.pos - a.pos
                dist = diff.length()
                if 0.001 < dist < min_dist:
                    overlap = (min_dist - dist) * 0.5
                    push = diff.get_normalised() * overlap
                    a.pos -= push
                    b.pos += push

    # ------------------------------------------------------------------ #
    # Ext 3: Hard wall penetration correction
    # ------------------------------------------------------------------ #

    def _resolve_wall_penetration(self):
        """Physically eject agents that penetrate within MIN_CLEARANCE of any wall segment."""
        MIN_CLEARANCE = 10.0
        for agent in self.agents:
            for wall in self.walls:
                seg = wall.p2 - wall.p1
                seg_len_sq = seg.dot(seg)
                if seg_len_sq < 0.001:
                    continue
                # Closest point on the wall segment to the agent
                t = max(0.0, min(1.0, (agent.pos - wall.p1).dot(seg) / seg_len_sq))
                closest = wall.p1 + seg * t
                diff = agent.pos - closest
                dist = diff.length()
                if 0.001 < dist < MIN_CLEARANCE:
                    normal = diff.get_normalised()
                    # Push position out
                    agent.pos = closest + normal * MIN_CLEARANCE
                    # Remove the velocity component heading into the wall
                    # so the agent deflects along the wall surface instead of
                    # continuing to push through it
                    dot = agent.vel.dot(normal)
                    if dot < 0:
                        agent.vel -= normal * dot

    # ------------------------------------------------------------------ #
    # Spatial utilities
    # ------------------------------------------------------------------ #

    def wrap_around(self, pos):
        if pos.x > self.cx:   pos.x -= self.cx
        elif pos.x < 0:       pos.x += self.cx
        if pos.y > self.cy:   pos.y -= self.cy
        elif pos.y < 0:       pos.y += self.cy

    def transform_points(self, points, pos, forward, side, scale):
        world_pts = [pt.copy() for pt in points]
        mat = Matrix33()
        mat.scale_update(scale.x, scale.y)
        mat.rotate_by_vectors_update(forward, side)
        mat.translate_update(pos.x, pos.y)
        mat.transform_vector2d_list(world_pts)
        return world_pts

    def transform_point(self, point, pos, forward, side):
        world_pt = point.copy()
        mat = Matrix33()
        mat.rotate_by_vectors_update(forward, side)
        mat.translate_update(pos.x, pos.y)
        mat.transform_vector2d(world_pt)
        return world_pt

    # ------------------------------------------------------------------ #
    # Input
    # ------------------------------------------------------------------ #

    def input_mouse(self, x, y, button, modifiers):
        pass

    def input_keyboard(self, symbol, modifiers):
        k = pyglet.window.key
        W_STEP = 0.1
        R_STEP = 5.0

        if symbol == k.P:
            self.paused = not self.paused
            return

        actions = {
            k.Q: ('w_cohesion',       W_STEP),
            k.A: ('w_cohesion',      -W_STEP),
            k.W: ('w_separation',     W_STEP),
            k.S: ('w_separation',    -W_STEP),
            k.E: ('w_alignment',      W_STEP),
            k.D: ('w_alignment',     -W_STEP),
            k.R: ('w_wander',         W_STEP),
            k.F: ('w_wander',        -W_STEP),
            k.T: ('neighbour_radius', R_STEP),
            k.G: ('neighbour_radius', -R_STEP),
            k.Y: ('sep_radius',       R_STEP),
            k.H: ('sep_radius',      -R_STEP),
            k.U: ('w_flee_predator',  W_STEP),
            k.J: ('w_flee_predator', -W_STEP),
            k.O: ('w_wall',           W_STEP),
            k.L: ('w_wall',          -W_STEP),
        }

        if symbol in actions:
            attr, delta = actions[symbol]
            setattr(self, attr, max(0.0, getattr(self, attr) + delta))
            self._update_labels()
