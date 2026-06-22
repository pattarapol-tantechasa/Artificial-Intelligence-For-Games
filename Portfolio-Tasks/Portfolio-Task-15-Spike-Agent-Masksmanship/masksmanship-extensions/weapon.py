import math


class WeaponProfile:
    def __init__(self, name, projectile_speed, accuracy, fire_rate,
                 effective_range=None, pellets_per_shot=1, spread_angle_maximum=0.0,
                 blast_radius=None):
        self.name = name
        self.projectile_speed = projectile_speed    # pixels per second
        self.accuracy = accuracy                    # 1.0 = perfect, lower = more spread
        self.fire_rate = fire_rate                  # shots per second
        self.effective_range = effective_range      # None = no range limit
        self.pellets_per_shot = pellets_per_shot    # projectiles spawned per shot
        self.spread_angle_maximum = spread_angle_maximum  # radians, per-pellet cone spread
        self.blast_radius = blast_radius            # None = direct hit, number = AoE explosion


RIFLE        = WeaponProfile('Rifle',        600, 0.98, 2.0)
ROCKET       = WeaponProfile('Rocket',       150, 0.97, 0.5)
HANDGUN      = WeaponProfile('Handgun',      500, 0.75, 3.0)
HAND_GRENADE = WeaponProfile('Hand Grenade', 120, 0.70, 0.3, blast_radius=80)
SHOTGUN      = WeaponProfile('Shotgun',      400, 1.0,  0.7,
                             effective_range=150,
                             pellets_per_shot=8,
                             spread_angle_maximum=math.radians(20))

WEAPONS = [RIFLE, ROCKET, HANDGUN, HAND_GRENADE, SHOTGUN]
