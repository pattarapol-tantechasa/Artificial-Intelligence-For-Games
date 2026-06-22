# Base class for all agents. Enforces that every agent implements get_move().
class Agent:
    def get_move(self, board, events=None):
        raise NotImplementedError
