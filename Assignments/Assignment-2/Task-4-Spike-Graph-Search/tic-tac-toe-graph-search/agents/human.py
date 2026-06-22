# Human agent — reads mouse click events to get the player's chosen cell.
import pygame
from agents.agent import Agent

class HumanAgent(Agent):
    def get_move(self, board, events=None):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                return board.get_cell_from_click(x, y, 640 // 3)
        return None  # no click this frame
