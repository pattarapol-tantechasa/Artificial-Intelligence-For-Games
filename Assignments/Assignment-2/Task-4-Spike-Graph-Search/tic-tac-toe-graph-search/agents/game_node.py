# Represents a single node in the game state graph.
# Each node holds a snapshot of the board, the move that produced it, and a pointer to its parent.

class GameNode:
    def __init__(self, board_state, move, parent=None):
        self.board_state = list(board_state)  # copy — critical, avoids shared mutable state
        self.move = move        # int cell index (0-8) that produced this state
        self.parent = parent    # GameNode | None

def board_state_key(board_state):
    """Return a hashable key for a board state — used by EfficientSearchAI's visited set."""
    return tuple(board_state)

def render_board(board_state):
    """Return a 5-line ASCII string of a 3x3 board state."""
    def cell(i):
        return board_state[i] if board_state[i] != ' ' else '.'
    rows = [' | '.join(cell(r * 3 + c) for c in range(3)) for r in range(3)]
    sep = '---------'
    return f'{rows[0]}\n{sep}\n{rows[1]}\n{sep}\n{rows[2]}'


def print_path(winning_node, agent_name='AI'):
    """Trace the parent chain from winning_node to root and print each board state."""
    path = []
    node = winning_node
    while node is not None:
        path.append(node)
        node = node.parent
    path.reverse()  # root-first order

    print(f'\n[{agent_name}] Winning path ({len(path)} step(s) deep):')
    for depth, n in enumerate(path):
        print(f'  Depth {depth} — move: {n.move}')
        for line in render_board(n.board_state).splitlines():
            print(f'    {line}')
    print()
