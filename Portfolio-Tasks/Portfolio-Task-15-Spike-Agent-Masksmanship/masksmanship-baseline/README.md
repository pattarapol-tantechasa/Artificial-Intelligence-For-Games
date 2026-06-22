# Task 15 — Agent Marksmanship (Baseline)

A 2D simulation demonstrating intelligent agent targeting. A static attacker fires projectiles at a moving target using predictive interception — calculating where the target *will be*, not where it currently is.

## Dependencies

- Python 3.10+
- Pyglet

Install Pyglet if not already installed:

```
pip install pyglet
```

## How to Run

From the `masksmanship-baseline/` directory:

```
python main.py
```

## Weapon Profiles

Switch weapons using number keys **1–4**. The active weapon name, speed, accuracy, and fire rate are shown in the top-left corner.

| Key | Weapon | Speed | Accuracy | Fire Rate |
|-----|--------|-------|----------|-----------|
| `1` | Rifle | 600 px/s | 98% | 2 shots/s |
| `2` | Rocket | 150 px/s | 97% | 0.5 shots/s |
| `3` | Handgun | 500 px/s | 75% | 3 shots/s |
| `4` | Hand Grenade | 120 px/s | 70% | 0.3 shots/s |

## Controls

| Key | Action |
|-----|--------|
| `1` – `4` | Switch weapon |
| `P` | Pause / Resume |
| `I` | Toggle debug view (aim line + interception crosshair) |

## What to Observe

- The **blue circle** is the static attacker
- The **cyan triangle** is the target patrolling between two waypoints
- **Yellow dots** are projectiles
- The target **flashes red** when hit
- Press `[I]` to reveal the **red aim line** and **green crosshair** marking the predicted interception point
- Switch to Rocket `[2]` with debug on — the green crosshair sits well ahead of the target, showing the AI is leading the shot
- Switch to Handgun `[3]` or Grenade `[4]` to observe shot spread from weapon inaccuracy
