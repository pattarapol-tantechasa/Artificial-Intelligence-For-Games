# Steering 1 - Seek, Arrive, Flee

COS30002 AI for Games — Portfolio Task 11

## Dependencies

- Python 3.x
- pyglet

Install pyglet via pip:

```bash
pip install pyglet
```

If you are using a conda environment:

```bash
conda activate ai-for-game
pip install pyglet
```

## How to Run

Navigate to the `steering-1` folder and run:

```bash
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| `1` | Seek — move toward target at full speed |
| `2` | Arrive Slow — decelerate gradually and stop at target |
| `3` | Arrive Normal — medium deceleration to target |
| `4` | Arrive Fast — fast deceleration to target |
| `5` | Flee — move away from target (only when within panic distance) |
| `6` | Pursuit — predict and intercept a moving target |
| `A` | Spawn a new agent at a random position |
| `P` | Pause / unpause the simulation |
| Left click | Move the target (red star) to cursor position |

## Features Implemented

### Seek
Agent computes a desired velocity pointing directly at the target at full speed, then steers toward it. The agent never slows down, so it will overshoot and orbit the target.
```python
desired_vel = (target_pos - self.pos).normalise() * self.max_speed
return desired_vel - self.vel
```

### Arrive
Same direction as seek, but desired speed scales down with distance — the agent brakes smoothly and stops at the target. Three deceleration rates are available (keys 2/3/4).
```python
speed = dist / decel_rate          # slower as distance shrinks
speed = min(speed, self.max_speed)
desired_vel = to_target * (speed / dist)
```
Deceleration rates: `slow=0.9`, `normal=0.5`, `fast=0.2`

### Flee
Agent moves away from the target but only reacts when within a panic distance of 200px. Outside that range it ignores the target entirely.
```python
if (hunter_pos - self.pos).length() > panic_distance:
    return Vector2D()  # too far away, do nothing
desired_vel = (self.pos - hunter_pos).normalise() * self.max_speed
```

### Spawn Agents
Press `A` to add a new agent at a random position. All agents respond to the same mode key presses simultaneously.
```python
self.agents.append(Agent(self))
```

### Physical Properties
Agent physics were tuned to produce realistic movement:
- `mass = 2.0` — heavier agent, slower to accelerate
- `max_speed = 500.0` — capped top speed (down from 2500)
- `friction = 0.95` — velocity bleeds off each tick, agent coasts to a stop naturally
```python
self.vel += acceleration * delta
self.vel *= self.friction           # apply friction each frame
self.vel.truncate(self.max_speed)
```

---

## Extensions

### Extension 1: Pursuit
The pursuer (blue agent) predicts where the prey (green agent) will be in the future and seeks that predicted position — rather than chasing where the prey currently is. This produces a realistic intercept path instead of just following behind.

The look-ahead time scales with distance: far away = predict further ahead.
```python
look_ahead_time = dist / (self.max_speed + evader.speed())
future_pos = evader.pos + evader.vel * look_ahead_time
return self.seek(future_pos)
```

On startup, the **green agent** (prey) seeks the click target and the **blue agent** (pursuer) intercepts it. Press `6` to switch all agents to pursuit mode.

### Extension 2: Non-Uniform Acceleration Limits
Instead of a single uniform force cap, acceleration is decomposed into **forward**, **side (lateral)**, and **reverse** components — each with its own limit. This makes movement feel like a vehicle: easy to accelerate forward, harder to turn, very sluggish in reverse.

```python
fwd_amount = acceleration.dot(self.heading)   # project onto heading axis
fwd_vec    = self.heading * fwd_amount        # forward/reverse part
side_vec   = acceleration - fwd_vec           # lateral (turning) part
# clamp each independently
# forward: 500  |  side: 250  |  reverse: 100
```

The result: agents take wide arcs when turning and overshoot significantly when reversing, compared to the snappy uniform behaviour in the baseline.
