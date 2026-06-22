# Task 14: Emergent Group Behaviour — Baseline

A simulation of emergent flocking behaviour using Python and Pyglet. Twenty-five autonomous boid agents combine **cohesion**, **separation**, **alignment**, and **wandering** steering forces via a weighted-sum approach to produce natural group movement patterns such as flocking and schooling.

## How to Run

```bash
cd Portfolio-Tasks/Portfolio-Task-14-Spike-Emergent-Group-Behaviour/emergent-group-baseline
python main.py
```

## Dependencies

- Python 3.13+
- Pyglet 2.1.14+

Install dependencies with:
```bash
pip install pyglet
```

## Controls

### Simulation

| Key | Action |
|-----|--------|
| `P` | Pause / Resume simulation |
| `I` | Toggle debug view (neighbourhood radius rings) |

### Real-Time Parameter Tuning

| Key | Action |
|-----|--------|
| `Q` / `A` | Increase / Decrease **Cohesion** weight |
| `W` / `S` | Increase / Decrease **Separation** weight |
| `E` / `D` | Increase / Decrease **Alignment** weight |
| `R` / `F` | Increase / Decrease **Wander** weight |
| `T` / `G` | Increase / Decrease **Neighbour Radius** |
| `Y` / `H` | Increase / Decrease **Separation Radius** |

All current parameter values are displayed on-screen in the top-left corner and update in real time.

## Simulation Overview

| Element | Colour | Description |
|---------|--------|-------------|
| Boid agents | Cyan triangles | Autonomous agents running the flocking simulation |
| Neighbourhood rings | Grey circles (debug) | Each agent's neighbour detection radius — press `I` to show |

## How the Flocking Works

Each agent runs four steering behaviours every frame, combined into one resultant force using a **weighted-sum**:

```
total_force = (cohesion   × w_cohesion)
            + (separation × w_separation)
            + (alignment  × w_alignment)
            + (wander     × w_wander)
```

| Behaviour | Description |
|-----------|-------------|
| **Cohesion** | Steers toward the average position of nearby neighbours — keeps the group together |
| **Separation** | Steers away from neighbours that are too close — prevents crowding |
| **Alignment** | Matches the average heading of nearby neighbours — synchronises direction |
| **Wandering** | Adds unpredictable organic movement using a projected jitter circle |

Neighbourhood is determined by `neighbour_radius`. Separation is only applied when another agent is within the smaller `sep_radius`.

## Distinct Emergent Modes

By adjusting the weights you can produce qualitatively different behaviours:

| Mode | Settings |
|------|----------|
| **Tight school** | High cohesion + high alignment, low wander |
| **Loose swarm** | Low cohesion, high wander, moderate separation |
| **Scattered drift** | Zero cohesion + zero alignment, high wander |
| **Repulsion field** | Very high separation, low cohesion — agents spread to fill space |

## Attribution

- Original steering codebase by Clinton Woodward and James Bonner
- Refactored by Enrique Ketterer <ekettererortiz@swin.edu.au> — S1 2026
