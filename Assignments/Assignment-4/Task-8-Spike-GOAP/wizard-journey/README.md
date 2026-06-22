# Wizard Potion Shop - GOAP System

A complete Goal-Oriented Action Planning (GOAP) implementation in Python demonstrating A* graph search over world states.

## What This Program Does

This is an **AI planning system** where an agent (a wizard) automatically plans a sequence of actions to achieve a goal (buy a potion and return home). The planner finds the cheapest path through possible actions, adapting its strategy when conditions change.

**In simple terms:** The agent asks "How do I reach my goal?" and the planner answers with a step-by-step plan. If the world changes (like a quest becoming unavailable), it automatically finds a new plan.


## Project Structure

```
wizard-journey/
├── main.py              # Runs the planner and shows results
├── world_state.py       # Stores world information (energy, gold, location, etc.)
├── action.py            # Defines what an action is
├── actions.py           # All 11 actions the agent can do
├── planner.py           # The A* algorithm that finds plans
├── simulation.py        # Shows step-by-step execution
└── README.md            # This file
```

**File Purposes:**

| File | Does What |
|------|-----------|
| `main.py` | Entry point - decides scenario and runs everything |
| `world_state.py` | Represents current game world (wizard's energy, gold, location, etc.) |
| `action.py` | Basic action template with cost and effects |
| `actions.py` | Defines 11 specific actions (Rest, Hunt, Travel, Buy, etc.) |
| `planner.py` | A* search algorithm that finds optimal plan |
| `simulation.py` | Shows each action executing and state changing |

---

## Quick Start

```bash
python main.py
```

---

## System Requirements

- **Python**: 3.6 or higher
- **Operating System**: Windows, macOS, or Linux
- **Dependencies**: None (uses only Python standard library)

## Setup Instructions

### Step 1: Verify Python Installation

Check that Python is installed:

```bash
python --version
```

Should output: `Python 3.6.0` or higher

### Step 2: Navigate to Project Directory

```bash
cd wizard-journey
```

### Step 3: Run the System

```bash
python main.py
```

### Step 4: Verify Output

You should see:
1. Initial world state printed
2. Plan found message (7 steps)
3. Step-by-step execution showing state changes
4. Final message: "GOAL ACHIEVED!"

---

## How to Run

### Scenario 1: Quest Available (Default)

**File:** `main.py` line 18

```python
QUEST_ALREADY_COMPLETE = False  # This is the default
```

**Run:**
```bash
python main.py
```

**Expected Output:**
```
Plan found! (7 steps)
Cost: 210
```

**Strategy:** Agent completes quest to earn gold, then buys potion

---

### Scenario 2: Quest Unavailable (Alternative)

**File:** `main.py` line 18 - Change to:

```python
QUEST_ALREADY_COMPLETE = True
```

**Run:**
```bash
python main.py
```

**Expected Output:**
```
Plan found! (16 steps)
Cost: 320
```

**Strategy:** Agent hunts monsters and sells ingredients for gold

---


