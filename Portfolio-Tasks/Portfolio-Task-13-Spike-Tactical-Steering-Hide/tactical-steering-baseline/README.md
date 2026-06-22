# Task 13: Tactical Steering — Hide!

A simulation of tactical steering behaviour using Python and Pyglet. A **prey** agent analyses the environment to find hiding spots behind circular obstacles and steers to the safest one, while a **hunter** wanders the environment unpredictably.

## How to Run

```bash
cd Portfolio-Tasks/Portfolio-Task-13-Spike-Tactical-Steering-Hide/tactical-steering-baseline
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

## Simulation Overview

| Agent | Colour | Description |
|-------|--------|-------------|
| Hunter | Red triangle | Wanders randomly through the environment |
| Prey | Green triangle | Evaluates all obstacles and steers to the best hiding spot |

| Object | Colour | Description |
|--------|--------|-------------|
| Obstacles | Dark green circles | Static objects the prey can hide behind |
| Hide spot markers | White **x** | Calculated hiding position behind each obstacle |
| Best hide spot | Yellow **x** | The optimal spot the prey is currently targeting |

## How the Hiding Works

1. For each obstacle, the simulation draws an imaginary line from the hunter through the obstacle centre.
2. That line is extended beyond the obstacle by its radius plus a small buffer — this is the **hide spot**.
3. All hide spots are recalculated every frame as the hunter moves.
4. The prey selects the **closest hide spot** to itself and steers to it using the Arrive behaviour.

## Attribution

- Original code by Clinton Woodward and James Bonner
- Refactored by Enrique Ketterer <ekettererortiz@swin.edu.au> — S1 2026
