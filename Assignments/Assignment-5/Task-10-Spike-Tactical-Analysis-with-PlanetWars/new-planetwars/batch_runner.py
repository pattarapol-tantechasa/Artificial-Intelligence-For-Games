"""Batch runner for headless PlanetWars experiments.

Runs multiple games between two bots across a set of maps and reports
win/loss/draw statistics. Results are printed as a table and saved to
a CSV file for use in the Spike Report.

Usage:
    python batch_runner.py

Adjust BOT_A, BOT_B, MAPS, and RUNS_PER_MAP below to configure the experiment.
"""

import json
import pathlib
import uuid
import collections
import csv
import datetime

from planet_wars import PlanetWarsGame

# ---- Experiment configuration ----
BOT_A        = "TacticalBot"
BOT_B        = "NaiveBot"
MAPS         = [f"map{str(i).zfill(3)}" for i in range(1, 11)]  # map001 to map010
RUNS_PER_MAP = 10     # games per map (higher = more statistically significant)
MAX_TICKS    = 5000   # tick cap per game to prevent infinite loops


def get_winner(game):
    """Determine the winner after a game ends.

    Returns the player name string, or 'Draw' if no clear winner.
    """
    # Count planets owned by each non-neutral player
    planet_counts = collections.defaultdict(int)
    ship_counts   = collections.defaultdict(int)

    for planet in game.planets.values():
        from entities import NEUTRAL_ID
        if planet.owner != NEUTRAL_ID:
            planet_counts[planet.owner] += 1
            ship_counts[planet.owner]   += planet.ships

    # Also count fleet ships
    for fleet in game.fleets.values():
        ship_counts[fleet.owner] += fleet.ships

    if not planet_counts:
        return "Draw"

    # Player with the most planets wins; break ties by total ships
    winner_id = max(planet_counts, key=lambda pid: (planet_counts[pid], ship_counts[pid]))

    # Map player ID back to name
    return game.players[winner_id].name


def run_game(map_name, bot_a, bot_b):
    """Run a single headless game and return the winner's name."""
    map_path = pathlib.PurePath("maps") / (map_name + ".json")
    with open(map_path) as f:
        gamestate = json.load(f)

    gamestate["players"] = [
        {"ID": str(uuid.uuid1()), "name": bot_a},
        {"ID": str(uuid.uuid1()), "name": bot_b},
    ]
    gamestate["max_ticks"] = MAX_TICKS

    game = PlanetWarsGame(gamestate)
    game.paused = False

    while game.is_alive() and game.tick < game.max_ticks:
        game.update()

    return get_winner(game)


def run_all():
    """Run all configured experiments and print + save results."""
    # results[map_name] = {BOT_A: wins, BOT_B: wins, 'Draw': count}
    results = {}

    total_a, total_b, total_draw = 0, 0, 0

    print(f"\nRunning {BOT_A} vs {BOT_B}  |  {RUNS_PER_MAP} runs per map\n")
    print(f"{'Map':<10} {'Runs':>5} {BOT_A:>14} {BOT_B:>14} {'Draw':>6} {BOT_A+' Win%':>12}")
    print("-" * 65)

    for map_name in MAPS:
        counts = {BOT_A: 0, BOT_B: 0, "Draw": 0}

        for run in range(RUNS_PER_MAP):
            winner = run_game(map_name, BOT_A, BOT_B)
            if winner in counts:
                counts[winner] += 1
            else:
                counts["Draw"] += 1

        results[map_name] = counts
        total_a    += counts[BOT_A]
        total_b    += counts[BOT_B]
        total_draw += counts["Draw"]

        win_pct = counts[BOT_A] / RUNS_PER_MAP * 100
        print(f"{map_name:<10} {RUNS_PER_MAP:>5} {counts[BOT_A]:>14} {counts[BOT_B]:>14} {counts['Draw']:>6} {win_pct:>11.1f}%")

    # Totals row
    print("-" * 65)
    total_runs = len(MAPS) * RUNS_PER_MAP
    overall_pct = total_a / total_runs * 100
    print(f"{'TOTAL':<10} {total_runs:>5} {total_a:>14} {total_b:>14} {total_draw:>6} {overall_pct:>11.1f}%")
    print()

    # Save to CSV
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path  = pathlib.Path("replays") / f"results_{BOT_A}_vs_{BOT_B}_{timestamp}.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Map", "Runs", f"{BOT_A} Wins", f"{BOT_B} Wins", "Draws", f"{BOT_A} Win%"])
        for map_name, counts in results.items():
            win_pct = counts[BOT_A] / RUNS_PER_MAP * 100
            writer.writerow([map_name, RUNS_PER_MAP, counts[BOT_A], counts[BOT_B], counts["Draw"], f"{win_pct:.1f}%"])
        win_pct = total_a / total_runs * 100
        writer.writerow(["TOTAL", total_runs, total_a, total_b, total_draw, f"{win_pct:.1f}%"])

    print(f"Results saved to {csv_path}")


if __name__ == "__main__":
    run_all()
