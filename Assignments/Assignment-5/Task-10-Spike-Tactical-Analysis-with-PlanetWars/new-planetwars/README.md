# PlanetWars — COS30002 AI for Games

Deceptive PlanetWars simulation for the COS30002 unit at Swinburne University of Technology.

## Dependencies

- Python 3.13+
- pyglet >= 2.1.14

Install with conda:
```bash
conda install pyglet
```

Or with pip:
```bash
pip install "pyglet>=2.1.14"
```

## Quick Start

```bash
# Run a headless game between two bots on a specific map
python main.py -p TacticalBot NaiveBot -m map001

# Run with the graphical interface
python main.py -p TacticalBot NaiveBot -m map001 --gui

# Run the batch experiment (TacticalBot vs NaiveBot across 10 maps, 10 runs each)
python batch_runner.py
```

## Switching Bots

Pass any two bot names (matching filenames in `bots/`) via `-p`:

| Match-up | Command |
|---|---|
| TacticalBot vs NaiveBot | `python main.py -p TacticalBot NaiveBot -m map001 --gui` |
| TacticalBot vs OneMove | `python main.py -p TacticalBot OneMove -m map001 --gui` |
| NaiveBot vs NaiveBot | `python main.py -p NaiveBot NaiveBot -m map001 --gui` |

Available bots in `bots/`:

| Bot | Description |
|---|---|
| `TacticalBot` | Tactical bot — scores targets by growth and proximity, keeps a garrison, sends minimum ships to win |
| `NaiveBot` | Naive baseline — attacks random targets from all planets, sends half its ships |
| `OneMove` | Sends all ships from the first planet to the first target every tick |
| `OneSlowMove` | Like OneMove but waits to accumulate ships first |
| `Blanko` | Does nothing — useful as a punching bag |

When TacticalBot is playing with `--gui`, **yellow lines** show which planet it is currently targeting from each of its planets.

## Batch Runner

`batch_runner.py` runs headless experiments and outputs a win/loss table:

```bash
python batch_runner.py
```

Edit the top of `batch_runner.py` to change:
- `BOT_A` / `BOT_B` — which bots to pit against each other
- `MAPS` — which maps to test on
- `RUNS_PER_MAP` — how many games per map (default: 10)

Results are saved as a CSV to the `replays/` directory.

## CLI Parameters

| Flag | Description |
|------|-------------|
| `-h`, `--help` | Show help message and exit. |
| `-p [PLAYERS...]`, `--players [PLAYERS...]` | Space-separated bot names (no `.py` extension) from `bots/`. |
| `-m MAP`, `--map MAP` | Filename (no extension) of a map in `maps/`. |
| `-r REPLAY`, `--replay REPLAY` | Filename (no extension) of a replay in `replays/`. |
| `--gui` | Launch the graphical window (pyglet). |
| `--logscript LOGSCRIPT` | Name of a log output script from `logscripts/`. |
| `--save-replay [NAME]` | Save a replay file. Optional name; defaults to auto-generated. |
| `--max-ticks N` | Maximum number of game ticks (default: 10 000). |

## GUI Controls

| Key | Action |
|-----|--------|
| `N` | Step the game forward by one frame. |
| `P` | Toggle pause/un-pause. |
| `-` / `+` | Decrease / increase frame rate. |
| `[` / `]` | Cycle through player views. |
| `A` | Return to the all-player view. |
| `L` | Cycle displayed planet property (ID, ships, vision_age, owner). |
| `Esc` | Quit the application. |

## Project Structure

| Path | Description |
|------|-------------|
| `main.py` | Entry point — CLI parsing and game bootstrap. |
| `planet_wars.py` | Core game engine (simulation loop, combat, fog-of-war). |
| `entities.py` | `Entity`, `Planet`, and `Fleet` classes. |
| `players.py` | `Player` class (façade) and bot controller loader. |
| `planet_wars_draw.py` | Pyglet rendering (window, shapes, batches). |
| `bots/` | Bot controllers (`TacticalBot.py`, `NaiveBot.py`, etc.). **Class name MUST match filename.** |
| `batch_runner.py` | Headless batch experiment runner — outputs win/loss stats table and CSV. |
| `maps/*.json` | Planet map definitions. |
| `replays/*.json` | Recorded game replays. |
| `logscripts/` | Optional log output scripts. |
| `map_generator.py` | Utility for procedurally generating new maps. |

## Authors

- Michael Jensen (2011)
- Clinton Woodward (2012)
- James Bonner (2023/4)
- Comments and code refactored by Enrique Ketterer — S1 2026
