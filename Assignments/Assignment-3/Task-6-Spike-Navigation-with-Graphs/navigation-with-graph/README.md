# Box World Navigation Visualiser

A sandbox tool to visualise how Graph Searching algorithms navigate 2D grid worlds.

### Authorship
- **Original Author**: Created for COS30002 AI for Games by Clinton Woodward (cwoodward@swin.edu.au).
- **Updated and Maintained by**: Enrique Ketterer (ekettererortiz@swin.edu.au).
- **Extended by**: Pattarapol Tantechasa (103883220@student.swin.edu.au) — Task 5 Lab submission.

## Objective
To understand Depth First Search (DFS), Breadth First Search (BFS), Dijkstra’s, and A* Search algorithms applied to a simple "box" based world.

## Features
- Interactive grid where tiles can be changed (clear, mud, water, wall, forest, hill).
- Configurable start and target positions.
- Multiple search algorithms:
  - Breadth First Search (BFS)
  - Depth First Search (DFS)
  - Dijkstra's Algorithm
  - A* (AStar) Search
- Step-by-step limits for clear instructional visualisation.
- Navigation graph, search tree, and final path overlaid visually.
- Diagonal movement edges enabled (8-directional movement).
- Animated agent that walks the found path node by node.
- Fully compatible with Pyglet 2.0+ library updates.

## Parameters/Flags
Run the tool by passing the map file path directly via the CLI:
`python main.py [map_filename]`

Available maps: `map1.txt`, `map2.txt`, `map3.txt` (custom — forest and hill terrain), `maze.txt` (custom — 10×10 maze).

## Usage Examples
```
python main.py map1.txt
python main.py map2.txt
python main.py map3.txt
python main.py maze.txt
```

### Controls
The world's boxes can be changed by selecting the box "kind" and left-clicking onto a box.

**Tile Brushes:**
- **1**: "clear" (white)
- **2**: "mud" (grey-brownish)
- **3**: "water" (blue)
- **4**: "wall" (black)
- **7**: "forest" (dark green) — moderate terrain cost
- **8**: "hill" (orange) — high terrain cost, elevation-based

**Node Placement:**
- **5**: "start"
- **6**: "target"

*(Note: Walls are not included in the navigation graph as they have no edges. You can allocate a start or target to a wall box, but this will stop any search from being successful!)*

**Execution & Limits:**
- **SPACE**: force a replan (execute search)
- **N / M**: Cycle (backward/forward) through the search methods and replan.
- **UP / DOWN**: Increase or decrease the search step depth limit by one.
- **0**: Remove the search step limit (A full search will be performed).

**Visibility Toggles:**
- **E**: toggle edges on/off for the current navigation graph (thin blue lines)
- **L**: toggle box (node) index values on/off (useful for understanding search and path details).
- **C**: toggle box "centre" markers on/off
- **T**: toggle tree on/off for the current search if available
- **P**: toggle path on/off for the current search if there is a successful route.

## Installation
Requires Python 3.x and Pyglet 2.0+.
```
pip install pyglet
```
Or with conda:
```
conda activate ai-for-game
python main.py map1.txt
```
