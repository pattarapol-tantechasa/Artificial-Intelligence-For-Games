class WeaponProfile:
    def __init__(self, name, projectile_speed, accuracy, fire_rate):
        self.name = name
        self.projectile_speed = projectile_speed  # pixels per second
        self.accuracy = accuracy                  # 1.0 = perfect, lower = more spread
        self.fire_rate = fire_rate                # shots per second


RIFLE        = WeaponProfile('Rifle',        600, 0.98, 2.0)
ROCKET       = WeaponProfile('Rocket',       150, 0.97, 0.5)
HANDGUN      = WeaponProfile('Handgun',      500, 0.75, 3.0)
HAND_GRENADE = WeaponProfile('Hand Grenade', 120, 0.70, 0.3)

WEAPONS = [RIFLE, ROCKET, HANDGUN, HAND_GRENADE]
