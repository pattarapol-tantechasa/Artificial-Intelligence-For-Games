# Smart AI — prioritises winning, then blocking, then falls back to random.
import random
from agents.agent import Agent

WIN_SET = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
)

class SmartAI(Agent):
    def get_move(self, board, events=None):
        # Step 1: take the win if available
        winning_move = self._find_winning_move(board, 'o')
        if winning_move is not None:
            print(f'[SmartAI]   picks cell {winning_move} to WIN')
            return winning_move

        # Step 2: block opponent from winning
        blocking_move = self._find_winning_move(board, 'x')
        if blocking_move is not None:
            print(f'[SmartAI]   picks cell {blocking_move} to BLOCK opponent')
            return blocking_move

        # Step 3: no strategic move, pick randomly
        empty_cells = [i for i in range(9) if board.get_cell(i) == ' ']
        index = random.choice(empty_cells)
        print(f'[SmartAI]   picks cell {index} (no win/block available, random fallback)')
        return index

    def _find_winning_move(self, board, player):
        # Returns the empty cell index that completes a winning combo, or None
        for combo in WIN_SET:
            a, b, c = combo
            cells = [board.get_cell(a), board.get_cell(b), board.get_cell(c)]
            if cells.count(player) == 2 and cells.count(' ') == 1:
                return combo[cells.index(' ')]
        return None
