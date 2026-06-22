"""Asymmetric Maps batch experiment for Task 10 Spike.

Tests TacticalBot vs NaiveBot on the hand-crafted asymmetric map (asym001)
in both player-position orders to measure positional bias.

Run A: TacticalBot as Player 1 (advantaged left side) vs NaiveBot as Player 2
Run B: NaiveBot as Player 1 (advantaged left side) vs TacticalBot as Player 2

Compare results against the symmetric baseline from batch_runner.py.

Usage:
    python asymmetric_batch.py
"""

import json
import pathlib
import uuid
import collections
import csv
import datetime

from planet_wars import PlanetWarsGame

# ---- Configuration ----
RUNS_PER_CONDITION = 20   # games per condition (A and B)
MAX_TICKS          = 5000

ASYM_MAP           = "asym001"
TACTICAL           = "TacticalBot"
NAIVE              = "NaiveBot"

# Symmetric baseline from batch_runner.py (100 games, map001-map010)
SYMMETRIC_TACTICAL_WINS = 97
SYMMETRIC_NAIVE_WINS    = 3
SYMMETRIC_TOTAL         = 100


def get_winner(game):
    """Return winner player name, or 'Draw'."""
    planet_counts = collections.defaultdict(int)
    ship_counts   = collections.defaultdict(int)

    for planet in game.planets.values():
        from entities import NEUTRAL_ID
        if planet.owner != NEUTRAL_ID:
            planet_counts[planet.owner] += 1
            ship_counts[planet.owner]   += planet.ships

    for fleet in game.fleets.values():
        ship_counts[fleet.owner] += fleet.ships

    if not planet_counts:
        return "Draw"

    winner_id = max(planet_counts, key=lambda pid: (planet_counts[pid], ship_counts[pid]))
    return game.players[winner_id].name


def run_game(map_name, bot_p1, bot_p2):
    """Run a single headless game. bot_p1 gets the Player 1 (left/advantaged) starting slot."""
    map_path = pathlib.PurePath("maps") / (map_name + ".json")
    with open(map_path) as f:
        gamestate = json.load(f)

    gamestate["players"] = [
        {"ID": str(uuid.uuid1()), "name": bot_p1},
        {"ID": str(uuid.uuid1()), "name": bot_p2},
    ]
    gamestate["max_ticks"] = MAX_TICKS

    game = PlanetWarsGame(gamestate)
    game.paused = False

    while game.is_alive() and game.tick < game.max_ticks:
        game.update()

    return get_winner(game)


def run_condition(label, bot_p1, bot_p2, runs):
    """Run one experimental condition and return counts."""
    counts = {TACTICAL: 0, NAIVE: 0, "Draw": 0}
    for _ in range(runs):
        winner = run_game(ASYM_MAP, bot_p1, bot_p2)
        if winner in counts:
            counts[winner] += 1
        else:
            counts["Draw"] += 1
    return counts


def run_all():
    print(f"\nAsymmetric Maps Experiment  |  map: {ASYM_MAP}  |  {RUNS_PER_CONDITION} runs per condition\n")
    print(f"{'Condition':<38} {'Runs':>5} {'Tactical Wins':>14} {'Naive Wins':>11} {'Draw':>5} {'Tactical Win%':>14}")
    print("-" * 95)

    # Symmetric baseline (pre-computed, not re-run)
    sym_pct = SYMMETRIC_TACTICAL_WINS / SYMMETRIC_TOTAL * 100
    print(f"{'Symmetric baseline (map001-010)':<38} {SYMMETRIC_TOTAL:>5} {SYMMETRIC_TACTICAL_WINS:>14} {SYMMETRIC_NAIVE_WINS:>11} {'0':>5} {sym_pct:>13.1f}%")

    # Run A: TacticalBot on advantaged (P1) side
    print(f"\nRunning Run A: {TACTICAL} as P1 (advantaged side)...")
    counts_a = run_condition(
        f"{TACTICAL}(P1) vs {NAIVE}(P2)",
        bot_p1=TACTICAL, bot_p2=NAIVE,
        runs=RUNS_PER_CONDITION,
    )
    pct_a = counts_a[TACTICAL] / RUNS_PER_CONDITION * 100
    print(f"{'Asym — TacticalBot P1 (advantaged)':<38} {RUNS_PER_CONDITION:>5} {counts_a[TACTICAL]:>14} {counts_a[NAIVE]:>11} {counts_a['Draw']:>5} {pct_a:>13.1f}%")

    # Run B: TacticalBot on disadvantaged (P2) side
    print(f"\nRunning Run B: {TACTICAL} as P2 (disadvantaged side)...")
    counts_b = run_condition(
        f"{NAIVE}(P1) vs {TACTICAL}(P2)",
        bot_p1=NAIVE, bot_p2=TACTICAL,
        runs=RUNS_PER_CONDITION,
    )
    pct_b = counts_b[TACTICAL] / RUNS_PER_CONDITION * 100
    print(f"{'Asym — TacticalBot P2 (disadvantaged)':<38} {RUNS_PER_CONDITION:>5} {counts_b[TACTICAL]:>14} {counts_b[NAIVE]:>11} {counts_b['Draw']:>5} {pct_b:>13.1f}%")

    print("-" * 95)
    print()
    print("Interpretation:")
    print(f"  Symmetric baseline:         {sym_pct:.1f}% TacticalBot win rate")
    print(f"  Asym with positional bonus: {pct_a:.1f}% TacticalBot win rate  (TacticalBot on advantaged P1 side)")
    print(f"  Asym with positional drag:  {pct_b:.1f}% TacticalBot win rate  (TacticalBot on disadvantaged P2 side)")
    delta_a = pct_a - sym_pct
    delta_b = pct_b - sym_pct
    print(f"\n  Positional advantage added:   {delta_a:+.1f}%")
    print(f"  Positional disadvantage drag: {delta_b:+.1f}%")
    print(f"  Total positional swing:       {pct_a - pct_b:.1f}% difference between P1 and P2 sides")

    # Save CSV
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path  = pathlib.Path("replays") / f"results_asymmetric_{timestamp}.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Condition", "Runs", "TacticalBot Wins", "NaiveBot Wins", "Draws", "TacticalBot Win%"])
        writer.writerow(["Symmetric baseline (map001-010)", SYMMETRIC_TOTAL,
                         SYMMETRIC_TACTICAL_WINS, SYMMETRIC_NAIVE_WINS, 0, f"{sym_pct:.1f}%"])
        writer.writerow([f"Asym — TacticalBot P1 (advantaged)", RUNS_PER_CONDITION,
                         counts_a[TACTICAL], counts_a[NAIVE], counts_a["Draw"], f"{pct_a:.1f}%"])
        writer.writerow([f"Asym — TacticalBot P2 (disadvantaged)", RUNS_PER_CONDITION,
                         counts_b[TACTICAL], counts_b[NAIVE], counts_b["Draw"], f"{pct_b:.1f}%"])

    print(f"\nResults saved to {csv_path}")

    return counts_a, counts_b, pct_a, pct_b, sym_pct


if __name__ == "__main__":
    run_all()
