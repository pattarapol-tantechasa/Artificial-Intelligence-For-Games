# Entry point. Swap agents here to change game mode (Human vs AI, AI vs AI, etc.)
import pygame
from game import Game
from agents.human import HumanAgent
from agents.random_ai import RandomAI
from agents.smart_ai import SmartAI

pygame.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption('Tic-Tac-Toe - AI vs AI')

player_x = RandomAI()
player_o = SmartAI()

game = Game(screen, player_x, player_o)
game.run()

pygame.quit()
