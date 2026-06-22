# Random AI — picks any empty cell at random, no strategy.
import random
from agents.agent import Agent

class RandomAI(Agent):
    def get_move(self, board, events=None):
        empty_cells = [i for i in range(9) if board.get_cell(i) == ' ']
        index = random.choice(empty_cells)
        print(f'[RandomAI]  picks cell {index} (random choice)')
        return index
