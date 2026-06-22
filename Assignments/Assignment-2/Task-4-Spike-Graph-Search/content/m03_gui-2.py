"""
COS30002 - Module 3 Pygame Companion: Uninformed Search Visualiser
Requires Python 3.12+ and Pygame (uv add pygame)

Proves the geometric difference between Breadth-First and Depth-First search.
Highlights the severe UI and engine constraints of Matrix data structures.
"""

import pygame
import sys
from collections import deque

# --- CORE ARCHITECTURE ---
type Point = tuple[int, int]

TILE = 20
COLS, ROWS = 40, 30
SIDEBAR_WIDTH = 350
WIDTH, HEIGHT = (COLS * TILE) + SIDEBAR_WIDTH, ROWS * TILE

# Colors
BG_COLOR = (25, 25, 25)
GRID_COLOR = (40, 40, 40)
WALL_COLOR = (120, 120, 120)
START_COLOR = (50, 200, 50)
GOAL_COLOR = (200, 50, 50)
VISITED_COLOR = (40, 80, 40)
PATH_COLOR = (255, 200, 50)
UI_BG = (15, 15, 15)
UI_TEXT = (220, 220, 220)

def get_neighbours(current: Point, grid_w: int, grid_h: int, walls: set[Point]) -> list[Point]:
    """Computes valid orthogonal neighbours dynamically (Implicit Adjacency List)."""
    neighbours = []
    # Up, Right, Down, Left
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        nx, ny = current[0] + dx, current[1] + dy
        if 0 <= nx < grid_w and 0 <= ny < grid_h and (nx, ny) not in walls:
            neighbours.append((nx, ny))
    return neighbours

# --- GENERATORS (Asynchronous Loop Steppers) ---

def bfs_stepper(start: Point, goal: Point, grid_w: int, grid_h: int, walls: set[Point]):
    queue = deque([[start]])
    visited = {start}
    steps = 0

    while queue:
        path = queue.popleft()
        current = path[-1]
        steps += 1

        if current == goal:
            yield path, visited, True, steps
            return

        for neighbor in get_neighbours(current, grid_w, grid_h, walls):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

        yield path, visited, False, steps

def dfs_stepper(start: Point, goal: Point, grid_w: int, grid_h: int, walls: set[Point]):
    stack = [[start]] 
    visited = {start}
    steps = 0

    while stack:
        path = stack.pop()
        current = path[-1]
        steps += 1

        if current == goal:
            yield path, visited, True, steps
            return

        # DFS pop takes the last appended item. We iterate normally.
        # This biases the search to plunge down the last checked direction.
        for neighbor in get_neighbours(current, grid_w, grid_h, walls):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(path + [neighbor])

        yield path, visited, False, steps

# --- UI & RENDERING ---

def render_sidebar(screen, font, small_font, state_dict):
    """Draws the right-hand UI panel containing logs and legends."""
    sidebar_rect = pygame.Rect(COLS * TILE, 0, SIDEBAR_WIDTH, HEIGHT)
    pygame.draw.rect(screen, UI_BG, sidebar_rect)
    pygame.draw.line(screen, (80, 80, 80), (COLS * TILE, 0), (COLS * TILE, HEIGHT), 2)

    y_offset = 20
    def draw_text(text, color, font_to_use, x=COLS * TILE + 20, y=None):
        nonlocal y_offset
        if y is None: y = y_offset
        surface = font_to_use.render(text, True, color)
        screen.blit(surface, (x, y))
        y_offset += surface.get_height() + 10

    draw_text("AI SEARCH VISUALISER", (200, 200, 255), font)
    y_offset += 10
    
    # Legend
    draw_text("CONTROLS", UI_TEXT, font)
    draw_text("[L-Click] Draw Wall", UI_TEXT, small_font)
    draw_text("[R-Click] Erase Wall", UI_TEXT, small_font)
    draw_text("[B] Run Breadth-First (BFS)", UI_TEXT, small_font)
    draw_text("[D] Run Depth-First (DFS)", UI_TEXT, small_font)
    draw_text("[C] Clear Grid / Reset", UI_TEXT, small_font)
    draw_text("[G] Toggle Gridlines", UI_TEXT, small_font)
    draw_text("[V] Toggle Data View", UI_TEXT, small_font)
    draw_text("[F] Toggle Sync/Async", UI_TEXT, small_font)
    
    y_offset += 20
    draw_text("SYSTEM LOGS", UI_TEXT, font)
    draw_text(f"View Mode:  {state_dict['view_mode']}", (255, 200, 100), small_font)
    
    sync_text = "Synchronous (Blocking)" if state_dict.get('sync_mode') else "Asynchronous"
    sync_color = (255, 100, 100) if state_dict.get('sync_mode') else (100, 255, 100)
    draw_text(f"Execution:  {sync_text}", sync_color, small_font)

    draw_text(f"Algorithm:  {state_dict['algo']}", UI_TEXT, small_font)
    draw_text(f"Status:     {state_dict['status']}", UI_TEXT, small_font)
    draw_text(f"Total Jumps:{state_dict['steps']}", (255, 100, 100), font)
    
    if state_dict['path_len'] > 0:
        draw_text(f"Path Length:{state_dict['path_len']}", (100, 255, 100), small_font)

def draw_data_view(screen, font, small_font, walls, view_mode):
    """
    Renders the raw data structures to prove O(V^2) memory scaling.
    We physically cannot render a 1.44 million item matrix without crashing Pygame,
    so we render a localized 10x10 slice to prove the point.
    """
    screen.fill(BG_COLOR, pygame.Rect(0, 0, COLS * TILE, HEIGHT))
    
    y = 20
    if view_mode == "LIST":
        title = font.render("ADJACENCY LIST (First 20 Nodes)", True, UI_TEXT)
        screen.blit(title, (20, y))
        y += 40
        count = 0
        for r in range(ROWS):
            for c in range(COLS):
                if (c, r) in walls: continue
                if count > 20: break
                
                neighbours = get_neighbours((c, r), COLS, ROWS, walls)
                text = small_font.render(f"Node ({c:02d}, {r:02d}) -> {neighbours}", True, (150, 200, 150))
                screen.blit(text, (20, y))
                y += 25
                count += 1
                
    elif view_mode == "MATRIX":
        title = font.render("ADJACENCY MATRIX (10x10 Slice of 1200x1200)", True, UI_TEXT)
        warning = small_font.render("WARNING: Full 1.44M entry matrix withheld to prevent engine crash.", True, (255, 100, 100))
        screen.blit(title, (20, y))
        screen.blit(warning, (20, y + 30))
        y += 70
        
        # Render a 10x10 cross-section of the matrix
        for i in range(10):
            row_str = f"({i:02d},00) | "
            for j in range(10):
                # Is node J a neighbour of node I?
                node_i = (i, 0)
                node_j = (j, 0) # Just checking a single row's relationships for the slice
                val = "1" if node_j in get_neighbours(node_i, COLS, ROWS, walls) else "0"
                row_str += f" {val} "
            
            text = small_font.render(row_str, True, (150, 150, 200))
            screen.blit(text, (20, y))
            y += 25


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("COS30002: AI Search Engine")
    
    font = pygame.font.SysFont("consolas", 20, bold=True)
    small_font = pygame.font.SysFont("consolas", 14)

    start = (5, 15)
    goal = (35, 15)
    walls = set()

    # Engine State
    search_generator = None
    current_path = []
    visited_set = set()
    show_grid = True
    
    view_modes = ["MAP", "LIST", "MATRIX"]
    current_view_idx = 0

    state_dict = {
        "view_mode": view_modes[current_view_idx],
        "algo": "None",
        "status": "Awaiting Input",
        "steps": 0,
        "path_len": 0,
        "sync_mode": False
    }

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Input handling for map drawing
            if state_dict["view_mode"] == "MAP":
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    if x < COLS * TILE:
                        col, row = x // TILE, y // TILE
                        if (col, row) != start and (col, row) != goal:
                            walls.add((col, row))
                if pygame.mouse.get_pressed()[2]: 
                    x, y = pygame.mouse.get_pos()
                    if x < COLS * TILE:
                        walls.discard((x // TILE, y // TILE))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and state_dict["view_mode"] == "MAP":
                    search_generator = bfs_stepper(start, goal, COLS, ROWS, walls)
                    state_dict.update({"algo": "BFS", "status": "Computing...", "steps": 0, "path_len": 0})
                    current_path, visited_set = [], set()
                elif event.key == pygame.K_d and state_dict["view_mode"] == "MAP":
                    search_generator = dfs_stepper(start, goal, COLS, ROWS, walls)
                    state_dict.update({"algo": "DFS", "status": "Computing...", "steps": 0, "path_len": 0})
                    current_path, visited_set = [], set()
                elif event.key == pygame.K_c:
                    search_generator = None
                    current_path, visited_set, walls = [], set(), set()
                    state_dict.update({"algo": "None", "status": "Cleared", "steps": 0, "path_len": 0})
                elif event.key == pygame.K_g:
                    show_grid = not show_grid
                elif event.key == pygame.K_v:
                    current_view_idx = (current_view_idx + 1) % len(view_modes)
                    state_dict["view_mode"] = view_modes[current_view_idx]
                elif event.key == pygame.K_f:
                    state_dict["sync_mode"] = not state_dict["sync_mode"]

        # Generator Tick (Engine Logic Loop)
        if search_generator and state_dict["status"] == "Computing...":
            if state_dict["sync_mode"]:
                # SYNCHRONOUS BLOCKING MODE: Exhaust the generator entirely in one frame.
                # This locks the main thread. On a larger grid, this triggers OS "Not Responding".
                try:
                    while True:
                        current_path, visited_set, finished, steps = next(search_generator)
                        state_dict["steps"] = steps
                        if finished:
                            state_dict["status"] = "Path Found!"
                            state_dict["path_len"] = len(current_path)
                            break
                except StopIteration:
                    state_dict["status"] = "No Path Exists"
            else:
                # ASYNCHRONOUS YIELD MODE: Time-slicing compute over multiple frames.
                try:
                    # Process 10 nodes per frame to speed up visualisation
                    for _ in range(10):
                        current_path, visited_set, finished, steps = next(search_generator)
                        state_dict["steps"] = steps
                        if finished:
                            state_dict["status"] = "Path Found!"
                            state_dict["path_len"] = len(current_path)
                            break
                except StopIteration:
                    state_dict["status"] = "No Path Exists"

        # --- RENDER PIPELINE ---
        screen.fill(BG_COLOR)

        if state_dict["view_mode"] == "MAP":
            # Gridlines
            if show_grid:
                for x in range(0, COLS * TILE, TILE):
                    pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
                for y in range(0, HEIGHT, TILE):
                    pygame.draw.line(screen, GRID_COLOR, (0, y), (COLS * TILE, y))

            # Visited / Frontier
            for v in visited_set:
                pygame.draw.rect(screen, VISITED_COLOR, (v[0]*TILE, v[1]*TILE, TILE, TILE))

            # Final Path
            for p in current_path:
                color = (255, 255, 0) if state_dict["status"] == "Path Found!" else PATH_COLOR
                pygame.draw.rect(screen, color, (p[0]*TILE, p[1]*TILE, TILE, TILE))

            # Walls
            for w in walls:
                pygame.draw.rect(screen, WALL_COLOR, (w[0]*TILE, w[1]*TILE, TILE, TILE))

            # Start and Goal
            pygame.draw.rect(screen, START_COLOR, (start[0]*TILE, start[1]*TILE, TILE, TILE))
            pygame.draw.rect(screen, GOAL_COLOR, (goal[0]*TILE, goal[1]*TILE, TILE, TILE))
            
            # Labels
            s_text = font.render("S", True, (0,0,0))
            g_text = font.render("G", True, (0,0,0))
            screen.blit(s_text, (start[0]*TILE + 5, start[1]*TILE + 1))
            screen.blit(g_text, (goal[0]*TILE + 5, goal[1]*TILE + 1))
            
        else:
            # Data Struct Views
            draw_data_view(screen, font, small_font, walls, state_dict["view_mode"])

        render_sidebar(screen, font, small_font, state_dict)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()