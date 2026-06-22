# Task 14: Emergent Group Behaviour — Extensions

Extends the baseline flocking simulation with four additional features: rigid body non-overlapping constraints, a predator agent that prey actively flee from, wall avoidance using feeler raycasting, and factional behaviours where three distinct agent types interact with unique cross-faction dynamics.

## How to Run

```bash
cd Portfolio-Tasks/Portfolio-Task-14-Spike-Emergent-Group-Behaviour/emergent-group-extensions
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
| `U` / `J` | Increase / Decrease **Flee Predator** weight (prey only) |
| `O` / `L` | Increase / Decrease **Wall Avoidance** weight |

All current parameter values are displayed on-screen in the top-left corner and update in real time.

## Simulation Overview

| Agent | Colour | Faction | Behaviour |
|-------|--------|---------|-----------|
| Prey | Cyan triangles | PREY | Flock with other cyan; flee from predators |
| Predators | Red triangles (larger) | PREDATOR | Chase the nearest prey every frame |
| Scavengers | Yellow triangles | SCAVENGER | Flock with other yellow; trail predators from a distance |

| Element | Description |
|---------|-------------|
| White horizontal line | Static wall obstacle in the centre — all agents avoid it via feeler raycasting |
| Grey rings (debug) | Each agent's neighbour detection radius — press `I` to show |

## Extensions Explained

### Extension 1 — Non-Overlapping Agents
After each update tick, every agent pair is checked. If two agents overlap (distance < sum of their radii), they are physically pushed apart by equal amounts. This is a rigid body constraint applied on top of the steering system, ensuring agents never visually stack regardless of weight settings.

### Extension 2 — Predator Avoidance
Three red predator agents independently chase the nearest cyan prey each frame using a seek behaviour. Cyan prey have an additional `flee_predator()` steering force that activates when a predator enters a 160px panic radius. The weight of this flee response is adjustable at runtime with `U` / `J`.

### Extension 3 — Wall Avoidance
Each agent projects three feelers forward every frame: one straight ahead (120px), and two angled 35° left and right (78px). If any feeler intersects the wall segment, the agent applies a velocity-space steering force perpendicular to the wall — the closer the detected intersection, the stronger the force. A secondary hard correction ejects agents and redirects their velocity if they penetrate within 10px of the wall.

### Extension 4 — Factional Behaviours
Each agent carries a `faction` tag (PREY / PREDATOR / SCAVENGER). The neighbourhood detection filters by faction, so cohesion, separation, and alignment only operate within each group. Cross-faction interactions are separate:
- Prey flee from predators
- Predators seek the nearest prey
- Scavengers follow the average predator position from 130px behind

## Distinct Emergent Modes (with extensions active)

| Mode | Settings |
|------|----------|
| **Tight panicking school** | High cohesion + high flee predator — flock clusters then explodes when red approaches |
| **Scattered survival** | Low cohesion, high flee — prey stay spread out to avoid mass capture |
| **Wall circulation** | Moderate cohesion + alignment, wall weight 1.5+ — flock circulates around the wall |
| **Predator dominance** | Low flee weight — prey ignore predators and flock normally regardless |

## Attribution

- Original steering codebase by Clinton Woodward and James Bonner
- Refactored by Enrique Ketterer <ekettererortiz@swin.edu.au> — S1 2026
