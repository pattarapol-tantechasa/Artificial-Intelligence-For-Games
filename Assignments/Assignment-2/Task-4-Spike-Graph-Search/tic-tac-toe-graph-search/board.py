# Stores game state and rules. No pygame — pure logic only.
class Board:
    # All possible winning combinations (rows, columns, diagonals)
    WIN_SET = ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6))

    def __init__(self):
        self.board = [' '] * 9  # 9 cells, all empty

    def get_cell(self, index):
        return self.board[index]

    def get_cell_from_click(self, x, y, cell_size):
        # Convert pixel position to board index (0-8)
        col = x // cell_size
        row = y // cell_size
        return row * 3 + col

    def is_valid_move(self, index):
        # A move is valid only if the cell is empty
        return self.board[index] == ' '

    def set_cell(self, index, player):
        self.board[index] = player

    def reset(self):
        self.board = [' '] * 9

    def check_for_winner(self):
        # Check all winning combos first, then tie, then return None if still going
        for combo in self.WIN_SET:
            a, b, c = combo
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                return self.board[a]  # 'x' or 'o'

        if ' ' not in self.board:
            return 'tie'

        return None
