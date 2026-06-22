# Task 7: Goal Oriented Behavior & SGI

Two scripts demonstrating Simple Goal Insistence (SGI) decision-making in AI — one showing it working correctly, one showing it fail.


### `gob_simple.py` — Working SGI 

**Run:**
```bash
python gob_simple.py
```

**What it does:**
Agent has 2 goals: Eat (4) and Sleep (3). It picks the most urgent goal and performs the best action to satisfy it.

**Expected output:**
- Iteration 1: Eat=4 (most urgent) → "get raw food" → Eat=1
- Iteration 2: Sleep=3 (most urgent) → "sleep in bed" → Sleep=0
- Iteration 3: Eat=1 (most urgent) → "get raw food" → Eat=0
- **Done!** Both goals satisfied.

**Why it works:** Actions are effective and have no side effects. SGI's greedy approach finds the optimal solution.

---

### `gob_sgi_fail.py` — SGI Failure Case 

**Run:**
```bash
python gob_sgi_fail.py
```

**What it does:**
Agent has 2 goals: Eat (10) and Sleep (10). But every action has negative side effects:
- `drink coffee` reduces Sleep by 3 but increases Eat by 2
- `eat heavy meal` reduces Eat by 3 but increases Sleep by 2

**Expected output:**
Agent oscillates between the two actions for 20 iterations:
- Satisfies Eat → increases Sleep
- Satisfies Sleep → increases Eat
- Never reaches a stable solution
- **Stops with:** "STUCK IN LOOP! Agent oscillates between actions."

**Why SGI fails:** It's too greedy and short-sighted. It only looks at the most pressing goal without considering that solving it will create a new problem. Gets trapped in an endless cycle.


