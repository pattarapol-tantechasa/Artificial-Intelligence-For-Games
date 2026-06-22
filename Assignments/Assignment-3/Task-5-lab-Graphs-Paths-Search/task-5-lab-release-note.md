# Task 5 - Lab - Graphs, Paths & Search

- Assignment: 3
- Task 5, Lab: Graphs, Paths and Search
- Name: Pattarapol Tantechasa
- Student ID: 103883220
- Email: [103883220@student.swin.edu.au](mailto:103883220@student.swin.edu.au)

## Release Note

- Explored and compared four pathfinding algorithms (DFS, BFS, Dijkstra, A*) on a grid-based world using pyglet.
- Fixed critical bug: `min_edge_cost` corrected from `10.0` to `1.0` in `box_world.py` to ensure A* heuristic is admissible and finds optimal paths.
- Enabled diagonal movement edges (8-directional) in `reset_navgraph()`.
- Added two new terrain types, **Forest** (dark green) and **Hill** (orange), with custom traversal costs.
- Created two custom maps: `maze.txt` (10×10 maze) and `map3.txt` (forest and hill terrain).
- Implemented an animated agent (`agent.py`), a red circle that walks the found path node by node at 60fps.
- Lab notes and observations documented in `Lab5_Notes.md` and `Lab5_Extensions_Notes.md`.

## How to Run

- `cd` into `Task-5-lab-Grabps-Paths-Search/05 - Lab - Graphs, Paths and Search` folder.
- Activate conda environment: `conda activate ai-for-game`
- Run with a map file:
  - `python main.py map1.txt`
  - `python main.py map2.txt`
  - `python main.py map3.txt`
  - `python main.py maze.txt`
- Press **SPACE** to run a search, **N/M** to cycle algorithms, **7** for forest brush, **8** for hill brush.
