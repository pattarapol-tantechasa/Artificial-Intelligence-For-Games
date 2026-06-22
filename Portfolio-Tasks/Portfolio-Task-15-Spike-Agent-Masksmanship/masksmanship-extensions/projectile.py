import pyglet
from vector2d import Vector2D
from graphics import COLOUR_NAMES, window

HIT_RADIUS = 15.0


class Projectile:
    def __init__(self, pos, vel, color='YELLOW'):
        self.pos = pos.copy()
        self.vel = vel.copy()
        self.active = True
        self.shape = pyglet.shapes.Circle(
            self.pos.x, self.pos.y, 4,
            color=COLOUR_NAMES[color],
            batch=window.get_batch("main")
        )

    def update(self, dt):
        self.pos += self.vel * dt
        self.shape.x = self.pos.x
        self.shape.y = self.pos.y

    def check_hit(self, target):
        if self.pos.distance(target.pos) < HIT_RADIUS:
            self.deactivate()
            return True
        return False

    def deactivate(self):
        self.active = False
        self.shape.visible = False


class ExplosiveProjectile(Projectile):
    """Travels to a proximity aim point then detonates with an area-of-effect blast."""

    DETONATE_DIST = 25.0   # px — how close to aim point triggers detonation
    BLAST_FLASH_TIME = 0.5  # seconds the blast ring is visible

    def __init__(self, pos, vel, aim_point, world, blast_radius=80):
        super().__init__(pos, vel, color='ORANGE')
        self.aim_point = aim_point.copy()
        self.world = world
        self.blast_radius = blast_radius
        self.detonated = False
        self._blast_flash = 0.0

        # Visual ring that appears at detonation
        self._blast_ring = pyglet.shapes.Arc(
            pos.x, pos.y, blast_radius,
            color=COLOUR_NAMES['ORANGE'],
            batch=window.get_batch("main")
        )
        self._blast_ring.visible = False

    def update(self, dt):
        if self.detonated:
            self._blast_flash -= dt
            if self._blast_flash <= 0:
                self._blast_ring.visible = False
                self.active = False
            return

        # Normal movement
        super().update(dt)

        # Detonate when close enough to the aim point
        if self.pos.distance(self.aim_point) < self.DETONATE_DIST:
            self._detonate()

    def _detonate(self):
        self.detonated = True
        self.shape.visible = False

        # Show blast ring at detonation position
        self._blast_ring.x = self.pos.x
        self._blast_ring.y = self.pos.y
        self._blast_ring.visible = True
        self._blast_flash = self.BLAST_FLASH_TIME

        # Register hit on anything within blast radius
        if self.world.target and self.pos.distance(self.world.target.pos) <= self.blast_radius:
            self.world.target.register_hit()

    def check_hit(self, target):
        return False  # hits are handled inside _detonate()

    def deactivate(self):
        self.active = False
        self.shape.visible = False
        self._blast_ring.visible = False
