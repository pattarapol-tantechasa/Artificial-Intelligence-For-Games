# Task 16 Spike: Soldier on Patrol (Baseline)

A layered Finite State Machine (FSM) simulation where a soldier agent autonomously patrols a waypoint path and switches to an attack mode when enemies are detected — built with Python and Pyglet.

## How to Run

```bash
cd Portfolio-Tasks/Portfolio-Task-16-Spike-Soldier-On-Patrol/soldier-baseline
conda activate ai-for-game
python main.py
```

## Dependencies

- Python 3.x
- Pyglet 2.1.14+
- Conda environment: `ai-for-game`

## Controls

| Key | Action |
|-----|--------|
| `E` | Spawn a stationary enemy at a random position |
| `P` | Pause / Resume simulation |
| `I` | Toggle debug visuals (force/velocity vectors) |

## FSM Architecture

The soldier brain is split into two layers:

**High-level states (what the agent is doing):**
- `PatrolState` — soldier follows a looped waypoint path, shown in orange
- `AttackState` — soldier stops and fires at the nearest enemy, shown in red

**Transition rules:**
- `Patrol → Attack`: a live enemy enters detection range (200 px)
- `Attack → Patrol`: no live enemies remain within detection range

**Low-level behaviours (how the agent does it):**
- Patrol uses `follow_path()` and `seek()` steering to move between waypoints
- Attack uses a 1.5-second shoot cooldown timer to fire yellow projectiles

## Project Structure

```
soldier-baseline/
├── main.py         # Entry point
├── game.py         # Game controller
├── world.py        # World state, enemy/projectile lists, key bindings
├── agent.py        # Soldier agent with FSM wiring
├── states.py       # FSM state classes (PatrolState, AttackState)
├── enemy.py        # Stationary enemy with health and health bar
├── projectile.py   # Straight-line bullet with hit detection
└── graphics.py     # Window and rendering utilities
```
