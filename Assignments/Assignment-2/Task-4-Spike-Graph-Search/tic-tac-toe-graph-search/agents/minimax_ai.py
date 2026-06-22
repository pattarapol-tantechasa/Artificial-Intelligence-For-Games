# MinimaxAI — exhaustive game-tree search using the minimax algorithm.
# Scores every possible outcome (+1 AI wins, -1 opponent wins, 0 tie) and always
# picks the move that maximises the AI's score. Never loses.
from agents.agent import Agent
from agents.game_node import GameNode

WIN_SET = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
)


class MinimaxAI(Agent):
    def get_move(self, board, events=None):
        current_state = list(board.board)
        ai_player = self._whose_turn(current_state)

        best_score = -2
        best_move = None

        for cell in range(9):
            if current_state[cell] != ' ':
                continue
            next_state = list(current_state)
            next_state[cell] = ai_player
            _ = GameNode(next_state, cell)  # graph node created per candidate
            score = self.minimax(next_state, is_maximising=False, ai_player=ai_player)
            if score > best_score:
                best_score = score
                best_move = cell

        print(f'[MinimaxAI]  picks cell {best_move} (score={best_score})')
        return best_move

    def minimax(self, board_state, is_maximising, ai_player):
        opponent = 'o' if ai_player == 'x' else 'x'
        winner = self._check_winner(board_state)

        if winner == ai_player:
            return 1
        if winner == opponent:
            return -1
        if winner == 'tie':
            return 0

        empty_cells = [i for i in range(9) if board_state[i] == ' ']

        if is_maximising:
            best = -2
            for cell in empty_cells:
                next_state = list(board_state)
                next_state[cell] = ai_player
                score = self.minimax(next_state, False, ai_player)
                best = max(best, score)
            return best
        else:
            best = 2
            for cell in empty_cells:
                next_state = list(board_state)
                next_state[cell] = opponent
                score = self.minimax(next_state, True, ai_player)
                best = min(best, score)
            return best

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
