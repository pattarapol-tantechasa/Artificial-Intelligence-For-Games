# Entry point. Swap agents here to change game mode (Human vs AI, AI vs AI, etc.)
import pygame
from game import Game
from agents.human import HumanAgent
from agents.random_ai import RandomAI
from agents.smart_ai import SmartAI
from agents.random_search_ai import RandomSearchAI
from agents.efficient_search_ai import EfficientSearchAI
from agents.minimax_ai import MinimaxAI

pygame.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption('Tic-Tac-Toe - AI vs AI')

# --- Matchup switchboard — uncomment the pair you want ---
# player_x = HumanAgent();      player_o = HumanAgent()          # Human vs Human
# player_x = HumanAgent();      player_o = RandomAI()            # Human vs RandomAI
# player_x = HumanAgent();      player_o = SmartAI()             # Human vs SmartAI

# player_x = HumanAgent();      player_o = RandomSearchAI()      # Human vs RandomSearchAI
player_x = HumanAgent();      player_o = EfficientSearchAI()   # Human vs EfficientSearchAI
# player_x = HumanAgent();      player_o = MinimaxAI()           # Human vs MinimaxAI

game = Game(screen, player_x, player_o)
game.run()

pygame.quit()
