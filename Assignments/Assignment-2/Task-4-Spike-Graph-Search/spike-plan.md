# Spike Plan 

## Title: 
Task 4: Spike - Graphs, Search & Rules

## Context: 

Extending the Task 3 Tic Tac Toe (pygame + OOP) to represent game states as a graph and implement three progressively smarter AI agents that search that graph. The existing Board/Game/Renderer/Agent architecture is kept intact. New files are added, old agents are preserved as baselines.

## Knowledge/Skill Gap: 

- I'm not familiar working with Tree and Graph based search.
- I don't know how to apply those data structure knowledge like BFS & DFS to the real game.
- I'm still very new to PyGame and concept of how to write code for game to refresh every frame.
  
## Goals/Deliverables: 

1. Get the current state of the board.
2. Randomly attempt a move, push the resulting board state onto a list.
3. If the move results in a victory, return the list.
4. Otherwise, take the last board state and repeat.

## Start-End Period:
- Start : 20 March 2026
- End : 27 March 2026

## Planning Notes:

- Update the [old Tic Tac Toe diagram](../Task-3-lab-Tic-Tac-Toe/tic-tac-toe-diagram.png) to reflect this spike task.
- Implement a class to represent each game state as a graph node -> `GameNode`
  - Holds a reference to the parent node for path tracing
- Implement AI agents that search the graph to find a winning move
  - `RandomSearchAI` -> randomly walks the graph until a winning state is found
  - `EfficientSearchAI` -> `RandomSearchAI` with deduplication; does not revisit already visited game states
  - `MinimaxAI` -> optimal search; always forces a tie or win

