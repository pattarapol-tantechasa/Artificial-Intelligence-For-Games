# RandomSearchAI — explores the game-state graph via a random walk.
# Pushes candidate GameNodes onto a stack; returns the first move that leads to a win,
# or falls back to any valid move if no winning path is found.
import random
from agents.agent import Agent
from agents.game_node import GameNode, print_path

WIN_SET = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
)


class RandomSearchAI(Agent):
    def get_move(self, board, events=None):
        current_state = list(board.board)
        player = self._whose_turn(current_state)

        empty_cells = [i for i in range(9) if current_state[i] == ' ']
        if not empty_cells:
            return None

        stack = []
        states_visited = 0
        # Seed the stack with all valid moves from the current position
        for cell in empty_cells:
            next_state = list(current_state)
            next_state[cell] = player
            stack.append(GameNode(next_state, cell, parent=None))

        random.shuffle(stack)

        while stack:
            node = stack.pop()
            states_visited += 1
            winner = self._check_winner(node.board_state)

            if winner == player:
                # Walk back to the first move from the original state
                root = node
                while root.parent is not None:
                    root = root.parent
                print_path(node, agent_name='RandomSearchAI')
                print(f'[RandomSearchAI] picks cell {root.move} (found winning path, visited {states_visited} states)')
                return root.move

            # Expand: pick a random empty cell from this node's state
            next_empties = [i for i in range(9) if node.board_state[i] == ' ']
            if next_empties:
                next_player = self._whose_turn(node.board_state)
                cell = random.choice(next_empties)
                next_state = list(node.board_state)
                next_state[cell] = next_player
                stack.append(GameNode(next_state, cell, parent=node))

        # Fallback: return any valid move
        move = random.choice(empty_cells)
        print(f'[RandomSearchAI] picks cell {move} (fallback, visited {states_visited} states)')
        return move

    def _whose_turn(self, board_state):
        xs = board_state.count('x')
        os = board_state.count('o')
        return 'x' if xs <= os else 'o'

    def _check_winner(self, board_state):
        for a, b, c in WIN_SET:
            if board_state[a] == board_state[b] == board_state[c] != ' ':
                return board_state[a]
        if ' ' not in board_state:
            return 'tie'
        return None
