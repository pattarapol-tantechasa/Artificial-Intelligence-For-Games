# Autonomous Agent Steering - Lab 12: Wander and Path Following

A simulation of autonomous agent steering behaviours using Python and Pyglet. Extends Lab 11 (Seek, Arrive, Flee) with two new behaviours: **Path Following** and **Smooth Wander**.

## How to Run

```bash
cd Portfolio-Tasks/Portfolio-Task-12-Lab-Wander-Paths/steering-2-wander-paths
python main.py
```

## Dependencies

- Python 3.13+
- Pyglet 2.1.14+

Install dependencies with:
```bash
uv add pyglet
```

## Controls

| Key | Action |
|-----|--------|
| `1` | Seek — agent chases the red target |
| `2` | Arrive Slow |
| `3` | Arrive Normal |
| `4` | Arrive Fast |
| `5` | Flee — agent runs away from target (within panic distance) |
| `6` | Pursuit (not implemented) |
| `7` | Follow Path — agent navigates the pink waypoint path |
| `8` | Wander — agent moves smoothly and randomly |
| `R` | Reset / regenerate a new random path |
| `P` | Pause / Resume simulation |
| `I` | Toggle debug visuals (force vectors, path, wander target) |
| Left click | Move the target |

## Features

- **Seek / Flee / Arrive** — foundational steering behaviours from Lab 11
- **Path Following** — agent seeks through a randomly generated looped set of waypoints, arriving smoothly at the final point of an open path
- **Smooth Wander** — uses a projected jitter circle to produce organic, non-erratic random movement
- **Force and speed limiting** — prevents erratic snapping during high-force situations
- **Toroidal world** — agents wrap around screen edges
- **Real-time debug overlay** — colour-coded vectors: Blue = steering force, Aqua = velocity, Grey = net change, Green dot = wander target, Pink lines = path

## Attribution

- Original code by Clinton Woodward and James Bonner
- Refactored by Enrique Ketterer <ekettererortiz@swin.edu.au> — S1 2026
