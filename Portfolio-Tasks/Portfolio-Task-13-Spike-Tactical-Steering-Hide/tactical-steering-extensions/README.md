# Task 13: Tactical Steering — Hide! (Extensions)

A simulation of tactical steering behaviour using Python and Pyglet. Extends the baseline with obstacle avoidance, multiple hunters, hunter line-of-sight and chase, and danger-aware hiding decisions.

## How to Run

```bash
cd Portfolio-Tasks/Portfolio-Task-13-Spike-Tactical-Steering-Hide/tactical-steering-extensions
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
| `P` | Pause / Resume simulation |
| `I` | Toggle debug visuals (force and velocity vectors) |

## Agents and Objects

| Agent | Colour | Description |
|-------|--------|-------------|
| Hunters | Red / Orange / Pink triangles | Wander independently; switch to active pursuit when prey is in line of sight |
| Prey | Green triangle | Evaluates all hiding spots and steers to the safest one |

| Object | Colour | Description |
|--------|--------|-------------|
| Obstacles | Dark green circles | Static objects the prey can hide behind; all agents avoid them |
| Hide spot markers | White **x** | Calculated hiding position behind each obstacle |
| Best hide spot | Yellow **x** | The spot the prey is currently targeting |
| Chase line | Orange line | Drawn from a hunter to the prey when it has line of sight |
| Score | Top-left label | Counts how many times the prey has been caught |

## Extensions Over Baseline

### Extension 1 — Obstacle Avoidance
All agents apply a proximity-based repulsion force when they get too close to an obstacle edge. A hard position correction also prevents any agent from fully overlapping a circle. Agents curve around obstacles naturally instead of clipping through them.

### Extension 2 — Multiple Hunters
Three hunters (red, orange, pink) wander independently. Each checks its own line of sight to the prey every frame. The prey's hiding logic identifies the **nearest hunter** as the primary threat when calculating which obstacle to hide behind.

### Extension 3 — Danger-Aware Path Scoring
The prey no longer picks the closest hiding spot blindly. Each candidate spot is scored by:

```
score = distance_to_spot + exposure * 2.0
```

`exposure` measures how close any hunter is to the straight-line travel path from the prey to that spot. If a hunter sits on the route to a nearby spot, the prey picks a farther spot with a safer approach path instead.

### Extension 4 — Hunter Chase, Eat, and Respawn
Each hunter performs a ray-cast against all obstacles every frame. If no obstacle blocks the line from the hunter to the prey, the hunter switches from **wander** to **pursuit** mode — predicting the prey's future position and steering toward it. When a hunter closes within catch range, the prey is "eaten", teleported to a random position, and the score increments.

## Attribution

- Original code by Clinton Woodward and James Bonner
- Refactored by Enrique Ketterer <ekettererortiz@swin.edu.au> — S1 2026
