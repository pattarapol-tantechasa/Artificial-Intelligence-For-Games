# Orchestrates the game loop trinity: process_input, update_model, render.
import pygame
from board import Board
from renderer import Renderer
from agents.human import HumanAgent

class Game:
    def __init__(self, screen, player_x, player_o, ai_delay=600):
        self.board = Board()
        self.renderer = Renderer(screen)
        self.screen = screen
        self.current_player = 'x'
        self.winner = None
        self.running = True
        self.agents = {'x': player_x, 'o': player_o}  # maps player symbol to agent
        self.ai_delay = ai_delay    # milliseconds between AI moves
        self.last_move_time = 0     # timestamp of the last AI move

    def process_input(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # R key resets the board and game state
                self.board.reset()
                self.winner = None
                self.current_player = 'x'

        if self.winner is not None:
            return  # stop accepting input once game is over

        agent = self.agents[self.current_player]

        if isinstance(agent, HumanAgent):
            # Human moves are driven by mouse click events
            index = agent.get_move(self.board, events)
        else:
            # AI moves are paced by ai_delay to make them visible on screen
            now = pygame.time.get_ticks()
            if now - self.last_move_time < self.ai_delay:
                return
            index = agent.get_move(self.board)
            self.last_move_time = now

        if index is not None and self.board.is_valid_move(index):
            self.board.set_cell(index, self.current_player)
            self.winner = self.board.check_for_winner()
            self.switch_turn()

    def switch_turn(self):
        self.current_player = 'o' if self.current_player == 'x' else 'x'

    def update_model(self):
        pass

    def render(self):
        self.screen.fill((255, 255, 255))
        self.renderer.draw_grid()
        self.renderer.draw_piece(self.board)
        self.renderer.draw_status_text(self.current_player, self.winner)

    def run(self):
        # Main game loop — runs every frame until window is closed
        while self.running:
            events = pygame.event.get()
            self.process_input(events)
            self.update_model()
            self.render()
            pygame.display.flip()  # push drawn frame to screen
