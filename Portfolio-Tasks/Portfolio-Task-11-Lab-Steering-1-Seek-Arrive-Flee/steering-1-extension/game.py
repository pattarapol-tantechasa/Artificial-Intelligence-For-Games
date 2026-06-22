game = None

from enum import Enum
import pyglet
from world import World
from graphics import window
from agent import Agent  # Agent with seek, arrive, flee and pursuit

class Game():
	def __init__(self):
		self.world = World(window.size[0], window.size[1])
		# prey agent (seek mode, green) — acts as the target for pursuit
		prey = Agent(self.world, mode='seek')
		prey.color = 'GREEN'
		prey.vehicle.color = (0, 255, 0, 255)
		self.world.agents.append(prey)
		self.world.hunter = prey
		# pursuer agent (pursuit mode, blue)
		pursuer = Agent(self.world, mode='pursuit')
		pursuer.color = 'BLUE'
		pursuer.vehicle.color = (0, 0, 255, 255)
		self.world.agents.append(pursuer)
		# unpause the world ready for movement
		self.world.paused = False

	def input_mouse(self, x, y, button, modifiers):
		self.world.input_mouse(x, y, button, modifiers)

	def input_keyboard(self, symbol, modifiers):
		self.world.input_keyboard(symbol, modifiers)

	def update(self, delta):
		self.world.update(delta)