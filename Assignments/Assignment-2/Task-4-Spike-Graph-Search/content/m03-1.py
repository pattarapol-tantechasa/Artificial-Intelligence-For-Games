"""
COS30002 - Module 3 Companion: Applied Uninformed Search
Requires Python 3.12+

Teaches the fundamental memory/computation trade-offs between BFS and DFS.
These are "blind" searches—they have no heuristic to guide them to the goal.
"""
from collections import deque
from typing import Optional

# Python 3.12 type aliases
type Node = str
type Graph = dict[Node, list[Node]]

def breadth_first_search(graph: Graph, start: Node, goal: Node) -> tuple[list[Node], int]:
    """
    Explores the graph layer by layer radially.
    Crucially, it uses collections.deque. In Python, popping from the start of a 
    standard list is O(N) because memory must shift. deque.popleft() is O(1).
    
    Returns: (Path to goal, Number of nodes evaluated)
    """
    queue = deque([[start]])
    visited = {start} 
    nodes_evaluated = 0

    while queue:
        path = queue.popleft()
        node = path[-1]
        nodes_evaluated += 1

        if node == goal:
            return path, nodes_evaluated

        for adjacent in graph.get(node, []):
            if adjacent not in visited:
                visited.add(adjacent)
                new_path = list(path)
                new_path.append(adjacent)
                queue.append(new_path)
                
    return [], nodes_evaluated

def depth_first_search(graph: Graph, start: Node, goal: Node, path: Optional[list[Node]] = None, visited: Optional[set[Node]] = None) -> tuple[list[Node], int]:
    """
    Dives down a single branch until it hits a dead end, then backtracks.
    Implemented recursively. Tracks evaluation count via a mutable list trick or global, 
    but rewritten here iteratively for accurate comparative benchmarking against BFS.
    """
    stack = [[start]]
    visited = {start}
    nodes_evaluated = 0

    while stack:
        path = stack.pop()
        node = path[-1]
        nodes_evaluated += 1

        if node == goal:
            return path, nodes_evaluated

        # Reverse to maintain standard left-to-right tree evaluation visually
        for adjacent in reversed(graph.get(node, [])):
            if adjacent not in visited:
                visited.add(adjacent)
                new_path = list(path)
                new_path.append(adjacent)
                stack.append(new_path)
                
    return [], nodes_evaluated

if __name__ == "__main__":
    # Standard navigation graph representation using an Adjacency List
    nav_graph: Graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': ['G'],
        'G': []
    }

    print("--- Graph Search Foundations ---\n")
    
    bfs_path, bfs_steps = breadth_first_search(nav_graph, 'A', 'G')
    print(f"BFS Path to G: {bfs_path} | Nodes Evaluated: {bfs_steps}")
    
    dfs_path, dfs_steps = depth_first_search(nav_graph, 'A', 'G')
    print(f"DFS Path to G: {dfs_path} | Nodes Evaluated: {dfs_steps}")
    
    print("\nNote: In this specific open tree, DFS stumbles upon the goal faster.")
