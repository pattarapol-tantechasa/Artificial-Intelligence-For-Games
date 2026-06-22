"""World Environment for Emergent Group Behaviour Simulation.

Manages the flock of agents, flocking parameters, and keyboard-driven
real-time weight adjustment with on-screen UI labels.
"""

import pyglet
from vector2d import Vector2D
from matrix33 import Matrix33
from graphics import COLOUR_NAMES, window
from agent import Agent


class World(object):
    """Simulation container for the emergent group behaviour spike."""

    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.paused = False

        # All boid agents
        self.agents = []

        # ---- Flocking weights (adjustable at runtime) ----
        self.w_cohesion   = 1.0
        self.w_separation = 2.0
        self.w_alignment  = 1.5
        self.w_wander     = 1.0

        # ---- Neighbourhood radii ----
        self.neighbour_radius = 100.0   # range for cohesion + alignment
        self.sep_radius       = 35.0    # range for separation push

        # ---- UI labels ----
        self._init_labels()

    # ------------------------------------------------------------------ #
    # UI
    # ------------------------------------------------------------------ #

    def _init_labels(self):
        """Add parameter display labels to the window."""
        x = 10
        y_start = self.cy - 30
        step = 20
        font = 16
        step = 24

        entries = [
            ('lbl_cohesion',   self._cohesion_text()),
            ('lbl_separation', self._separation_text()),
            ('lbl_alignment',  self._alignment_text()),
            ('lbl_wander',     self._wander_text()),
            ('lbl_nbr',        self._nbr_text()),
            ('lbl_sep',        self._sep_text()),
            ('lbl_hint',       '[P] Pause/Resume  |  [I] Toggle neighbour radius'),
        ]

        for i, (key, text) in enumerate(entries):
            window.labels[key] = pyglet.text.Label(
                text,
                font_size=font,
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

    def _cohesion_text(self):
        return f'[Q/A] Cohesion:        {self.w_cohesion:.2f}'

    def _separation_text(self):
        return f'[W/S] Separation:      {self.w_separation:.2f}'

    def _alignment_text(self):
        return f'[E/D] Alignment:       {self.w_alignment:.2f}'

    def _wander_text(self):
        return f'[R/F] Wander:          {self.w_wander:.2f}'

    def _nbr_text(self):
        return f'[T/G] Neighbour Radius: {self.neighbour_radius:.0f}'

    def _sep_text(self):
        return f'[Y/H] Separation Radius:{self.sep_radius:.0f}'

    # ------------------------------------------------------------------ #
    # Simulation loop
    # ------------------------------------------------------------------ #

    def update(self, delta):
        if not self.paused:
            for agent in self.agents:
                agent.update(delta)

    # ------------------------------------------------------------------ #
    # Spatial utilities
    # ------------------------------------------------------------------ #

    def wrap_around(self, pos):
        """Toroidal world wrap."""
        if pos.x > self.cx:
            pos.x -= self.cx
        elif pos.x < 0:
            pos.x += self.cx
        if pos.y > self.cy:
            pos.y -= self.cy
        elif pos.y < 0:
            pos.y += self.cy

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
        }

        if symbol in actions:
            attr, delta = actions[symbol]
            current = getattr(self, attr)
            setattr(self, attr, max(0.0, current + delta))
            self._update_labels()
