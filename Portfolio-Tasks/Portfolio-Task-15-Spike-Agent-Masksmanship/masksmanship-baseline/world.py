import pyglet
from vector2d import Vector2D
from matrix33 import Matrix33
from graphics import COLOUR_NAMES, window
from weapon import WEAPONS


class World:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.paused = False

        self.attacker = None
        self.target = None
        self.projectiles = []

        self.weapon_idx = 0

        self._init_labels()

    @property
    def active_weapon(self):
        return WEAPONS[self.weapon_idx]

    # ------------------------------------------------------------------ #
    # UI
    # ------------------------------------------------------------------ #

    def _init_labels(self):
        x = 10
        y_start = self.cy - 30
        font = 16
        step = 24
        entries = [
            ('lbl_weapon', self._weapon_text()),
            ('lbl_hint',   '[1] Rifle  [2] Rocket  [3] Handgun  [4] Hand Grenade  |  [P] Pause  |  [I] Debug'),
        ]
        for i, (key, text) in enumerate(entries):
            window.labels[key] = pyglet.text.Label(
                text, font_size=font,
                x=x, y=y_start - i * step,
                color=COLOUR_NAMES['WHITE']
            )

    def _weapon_text(self):
        w = self.active_weapon
        return f'Weapon: {w.name}  |  Speed: {w.projectile_speed} px/s  |  Accuracy: {w.accuracy:.0%}  |  Rate: {w.fire_rate}/s'

    def _update_labels(self):
        window.labels['lbl_weapon'].text = self._weapon_text()

    # ------------------------------------------------------------------ #
    # Simulation loop
    # ------------------------------------------------------------------ #

    def update(self, delta):
        if self.paused:
            return

        self.target.update(delta)
        self.attacker.update(delta, self.target, self.active_weapon)

        for proj in self.projectiles:
            proj.update(delta)
            if proj.active and proj.check_hit(self.target):
                self.target.register_hit()
            # Deactivate if off screen
            if (proj.pos.x < 0 or proj.pos.x > self.cx or
                    proj.pos.y < 0 or proj.pos.y > self.cy):
                proj.deactivate()

        self.projectiles = [p for p in self.projectiles if p.active]

    # ------------------------------------------------------------------ #
    # Spatial utilities (kept for wander/transforms if needed)
    # ------------------------------------------------------------------ #

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

        if symbol == k.P:
            self.paused = not self.paused
            return

        weapon_keys = {k._1: 0, k._2: 1, k._3: 2, k._4: 3}
        if symbol in weapon_keys:
            self.weapon_idx = weapon_keys[symbol]
            self._update_labels()
