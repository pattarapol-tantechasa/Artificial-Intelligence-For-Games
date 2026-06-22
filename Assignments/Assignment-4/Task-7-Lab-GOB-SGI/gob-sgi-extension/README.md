# GOB-SGI Extensions

Two extensions demonstrating advanced Goal Oriented Behaviour concepts.

## Extension 1: Object-Oriented Refactoring

**File:** `gob_oo.py`

Refactors the dictionary-based GOB code from gob_simple.py into an object-oriented design.

**Run:**
```bash
python gob_oo.py
```

**Output:** Same as gob_simple.py but using reusable classes (Goal, Action, Agent, World).

**Key Benefit:** The OO structure enables multiple independent agents, which is essential for Extension 2.

---

## Extension 2: Combat Simulation

**File:** `combat_simulation.py`

Two AI-controlled NPCs (Hero and Villain) fight in turn-based combat using SGI to choose actions.

**Run:**
```bash
python combat_simulation.py
```

**Output:** Turn-by-turn battle log showing each agent's goals, chosen action, and HP status.

### How It Works
- Hero vs Villain fight until one dies
- Each agent has Attack and Survive goals
- SGI chooses best action each turn (attack, heal, special)
- Survive goal increases when damaged (reactive healing)
- Attack goal increases over time (keeps combat engaging)

### Key Insights
- Shows SGI's reactive, goal-driven decision-making
- Demonstrates emergent behavior (no hardcoded rules)
- Reveals SGI's weakness: no lookahead or planning
- Perfect for understanding AI for games

---

## Learning Outcomes

After running both extensions, you understand:

1. **Object-Oriented Design for Game AI**
   - Why classes are better than global state for multiple agents
   - How to extend Agent class for specialization
   - Trade-offs: boilerplate vs. reusability

2. **SGI in a Game Context**
   - How goals drive decision-making
   - Dynamic goal updates based on game state
   - Emergent combat behavior from simple rules

3. **SGI Limitations**
   - No long-term planning or strategy
   - Goal oscillation can create predictable patterns
   - Better systems (Behavior Trees, Utility-Based AI) needed for complexity

---

## Files Structure
```
gob-sgi-extension/
  gob_oo.py                    # Extension 1: OO refactoring
  combat_simulation.py         # Extension 2: Combat simulation
  README.md                    # This file
```

## Verification

Test both extensions:
```bash
python gob_oo.py           # Should output 3 iterations, Done!
python combat_simulation.py # Should output 10-15 turn battle, winner announced
```

Both should run without errors and demonstrate the core SGI algorithm working in different contexts.
