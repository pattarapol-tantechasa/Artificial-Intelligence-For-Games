# EfficientSearchAI — same random graph walk as RandomSearchAI but with a visited-state set
# to skip duplicate board positions and backtrack when all children are exhausted.
import random
from agents.agent import Agent
from agents.game_node import GameNode, board_state_key, print_path

WIN_SET = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
)


class EfficientSearchAI(Agent):
    def get_move(self, board, events=None):
        current_state = list(board.board)
        player = self._whose_turn(current_state)

        empty_cells = [i for i in range(9) if current_state[i] == ' ']
        if not empty_cells:
            return None

        visited = set()
        visited.add(board_state_key(current_state))

        stack = []
        for cell in empty_cells:
            next_state = list(current_state)
            next_state[cell] = player
            key = board_state_key(next_state)
            if key not in visited:
                visited.add(key)
                stack.append(GameNode(next_state, cell, parent=None))

        random.shuffle(stack)

        while stack:
            node = stack.pop()
            winner = self._check_winner(node.board_state)

            if winner == player:
                root = node
                while root.parent is not None:
                    root = root.parent
                print_path(node, agent_name='EfficientSearchAI')
                print(f'[EfficientSearchAI] picks cell {root.move} (found winning path, visited {len(visited)} states)')
                return root.move

            # Expand only unvisited children
            next_empties = [i for i in range(9) if node.board_state[i] == ' ']
            next_player = self._whose_turn(node.board_state)
            children_added = 0
            for cell in next_empties:
                next_state = list(node.board_state)
                next_state[cell] = next_player
                key = board_state_key(next_state)
                if key not in visited:
                    visited.add(key)
                    stack.append(GameNode(next_state, cell, parent=node))
                    children_added += 1

        # Fallback: return any valid move
        move = random.choice(empty_cells)
        print(f'[EfficientSearchAI] picks cell {move} (fallback, exhausted {len(visited)} states)')
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
