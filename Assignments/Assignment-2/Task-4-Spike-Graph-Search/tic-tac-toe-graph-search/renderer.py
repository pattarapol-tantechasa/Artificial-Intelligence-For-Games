# Handles all pygame drawing. No game logic here.
import pygame

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.cell_size = 640 // 3           # pixel width/height of each cell
        self.font = pygame.font.SysFont(None, 48)

    def draw_grid(self):
        # Draw 2 vertical and 2 horizontal lines to form the 3x3 grid
        color = (0, 0, 0)
        pygame.draw.line(self.screen, color, (self.cell_size, 0), (self.cell_size, 640), 2)
        pygame.draw.line(self.screen, color, (self.cell_size * 2, 0), (self.cell_size * 2, 640), 2)
        pygame.draw.line(self.screen, color, (0, self.cell_size), (640, self.cell_size), 2)
        pygame.draw.line(self.screen, color, (0, self.cell_size * 2), (640, self.cell_size * 2), 2)

    def draw_piece(self, board):
        # Loop all 9 cells and draw X or O at each cell's center
        for index in range(9):
            cell = board.get_cell(index)
            col = index % 3
            row = index // 3
            center_x = col * self.cell_size + self.cell_size // 2
            center_y = row * self.cell_size + self.cell_size // 2

            if cell == 'o':
                pygame.draw.circle(self.screen, (255, 0, 0), (center_x, center_y), 80, 5)
            elif cell == 'x':
                margin = 80  # how far from center the line endpoints are
                pygame.draw.line(self.screen, (0, 0, 255), (center_x - margin, center_y - margin), (center_x + margin, center_y + margin), 5)
                pygame.draw.line(self.screen, (0, 0, 255), (center_x + margin, center_y - margin), (center_x - margin, center_y + margin), 5)

    def draw_status_text(self, current_player, winner):
        # Show winner/tie message or whose turn it is at the bottom of the screen
        if winner == 'tie':
            text = "It's a tie!  Press R to restart"
        elif winner is not None:
            text = f'Player {winner.upper()} wins!  Press R to restart'
        else:
            text = f"Player {current_player.upper()}'s turn"

        surface = self.font.render(text, True, (0, 200, 0))
        rect = surface.get_rect(center=(320, 615))
        self.screen.blit(surface, rect)  # stamp text surface onto screen
