# PlanetWars

A turn-based space strategy simulation where AI bots compete to conquer planets by launching fleets.

## How to Run

From the `planetwars/` directory, run `main.py` with the following flags:

```
python main.py --gui -p <Bot1> <Bot2> -m <map>
```

| Flag | Description |
|------|-------------|
| `--gui` | Run with graphical window |
| `-p <Bot1> <Bot2>` | Bot names (no `.py` extension) from the `bots/` folder |
| `-m <map>` | Map name (no extension) from the `maps/` folder |

### GUI Controls

| Key | Action |
|-----|--------|
| `N` | Step one frame forward |
| `P` | Pause / Unpause |
| `+` / `-` | Increase / Decrease frame rate |
| `[` / `]` | Cycle player views |
| `A` | Return to full map view |
| `L` | Cycle planet label types |

## Custom Bots

### Rando (`bots/Rando.py`)

Runs Rando against OneMove on map001:

```
python main.py --gui -p Rando OneMove -m map001
```

Rando attacks randomly each turn. It picks a random source planet it owns and a random target it does not own, then launches 75% of the source planet's ships if it has more than 10.

### BestWorst (`bots/BestWorst.py`)

Runs BestWorst against Rando on map001:

```
python main.py --gui -p BestWorst Rando -m map001
```

BestWorst uses targeted logic instead of random selection:

- **Source**: always picks the planet it owns with the **most** ships (`max` by `ships`), maximising fleet size.
- **Target**: always picks the planet it does not own with the **fewest** ships (`min` by `ships`), choosing the easiest planet to capture.

This makes BestWorst consistently stronger than Rando because it commits large forces against weak targets rather than wasting ships on random, potentially heavily defended planets.

## Extensions

### Defender (`bots/Defender.py`)

```
python main.py --gui -p Defender BestWorst -m map001
```

Adds a defence phase before attacking. Each tick it scans visible enemy fleets — if one is heading to a planet we own and outnumbers it, the bot sends reinforcements from the safest friendly planet with the most spare ships. If no threats are detected, it falls back to BestWorst attack logic.

### Closest (`bots/Closest.py`)

```
python main.py --gui -p Closest BestWorst -m map001
```

Targets the nearest planet rather than the weakest. Uses `distance_to()` (squared distance) as the selection key. Fleets arrive faster, reducing transit time and exposure compared to BestWorst.

### Scout (`bots/Scout.py`)

```
python main.py --gui -p Scout BestWorst -m map001
```

Uses `vision_age` to detect planets with stale information (not currently visible). Before committing a real attack, it sends a single probe ship to the closest unscouted planet to reveal its true ship count. Once all visible planets have fresh data, it attacks the weakest target using BestWorst logic.
