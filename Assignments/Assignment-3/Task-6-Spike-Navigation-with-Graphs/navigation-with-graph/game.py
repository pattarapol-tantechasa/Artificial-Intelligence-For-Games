game = None

from enum import Enum
import random
import pyglet
from box_world import BoxWorld, search_modes
from graphics import window, COLOUR_NAMES
from  agent import GroundAgent, FlyingAgent

# Mouse mode indicates what the mouse "click" should do...
class MouseModes(Enum):
		CLEAR = 	pyglet.window.key._1
		MUD = 		pyglet.window.key._2
		WATER = 	pyglet.window.key._3
		WALL = 		pyglet.window.key._4
		FOREST = 	pyglet.window.key._5
		HILL = 		pyglet.window.key._6
		ICE = 		pyglet.window.key._7

class SearchModes(Enum):
		DFS = 		1
		BFS = 		2
		Dijkstra = 	3
		AStar = 	4

class Game():
	def __init__(self, map):
		self.world = BoxWorld.FromFile(map)
		# Mouse mode indicates what the mouse "click" should do...
		self.mouse_mode = MouseModes.MUD
		window._update_label('mouse', 'Click to place: '+self.mouse_mode.name)

		# search mode cycles through the search algorithm used by box_world
		self.search_mode = 1
		window._update_label('search', 'Search Type: '+SearchModes(self.search_mode).name)
		# search limit
		self.search_limit = 0 # unlimited.
		window._update_label('status', 'Status: Loaded')
  
		self.agent = [GroundAgent(), GroundAgent(), FlyingAgent(), FlyingAgent()]
  
		for agent in self.agent:
			start = random.randint(0, len(self.world.boxes) - 1)
			while self.world.boxes[start].type == "WALL":
				start = random.randint(0, len(self.world.boxes) - 1)
			target = random.randint(0, len(self.world.boxes) - 1)
			while self.world.boxes[target].type == "WALL" or target == start:
				target = random.randint(0, len(self.world.boxes) - 1)
				
			agent.start_idx = start
			agent.target_idx = target
			agent.plan_path(self.world)
			pyglet.clock.schedule_interval(agent.update, 1/60)

		pyglet.clock.schedule_interval(self.update, 1/60)

	def update(self, dt):
		self.check_collisions()
		# decay threat costs over time, rebuild graph once if any changed
		changed = False
		for box in self.world.boxes:
			if hasattr(box, 'threat') and box.threat > 0:
				box.threat = max(0, box.threat - dt * 2.0)
				# fade color from red back to original
				t = box.threat / 20.0  # 1.0 = full threat (red), 0.0 = safe (original)
				orig = box.original_color
				r = int(255 * t + orig[0] * (1 - t))
				g = int(0   * t + orig[1] * (1 - t))
				b = int(0   * t + orig[2] * (1 - t))
				box.box.color = (r, g, b, 255)
				changed = True
			elif hasattr(box, 'threat') and box.threat == 0 and hasattr(box, 'original_color'):
				box.box.color = box.original_color
				del box.original_color  # cleanup so we can re-save next collision
				box.threat = -1  # sentinel so we don't re-enter this branch
		if changed:
			self.world.reset_navgraph()

	
	def plan_path(self):
		for agent in self.agent:
			start = random.randint(0, len(self.world.boxes) - 1)
			while self.world.boxes[start].type == "WALL":
				start = random.randint(0, len(self.world.boxes) - 1)
			target = random.randint(0, len(self.world.boxes) - 1)
			while self.world.boxes[target].type == "WALL" or target == start:
				target = random.randint(0, len(self.world.boxes) - 1)
				
			agent.start_idx = start
			agent.target_idx = target
			agent.plan_path(self.world)
		
     
     
		# self.world.plan_path(self.search_mode, self.search_limit)
		# window._update_label('status', 'Status: Path Planned')
		# if self.world.path and self.world.path.path:
		# 	self.agent.set_path(self.world.boxes, self.world.path.path)

	def input_mouse(self, x, y, button, modifiers):
		box = self.world.get_box_by_pos(x,y)
		if box:
			box.set_type(self.mouse_mode.name)
			self.world.reset_navgraph()
			self.plan_path()
			window._update_label('status','Status: Graph Changed')

	def input_keyboard(self, symbol, modifiers):
		# mode change?
		if symbol in MouseModes:
			self.mouse_mode = MouseModes(symbol)
			window._update_label('mouse', 'Click to place: '+self.mouse_mode.name)

		# Change search mode? (Algorithm)
		elif symbol == pyglet.window.key.M:
			self.search_mode += 1
			if self.search_mode > len(search_modes):
				self.search_mode = 1
			self.plan_path()
			window._update_label('search', 'Search Type: '+SearchModes(self.search_mode).name)
		elif symbol == pyglet.window.key.N:
			self.search_mode -= 1
			if self.search_mode <= 0:
				self.search_mode = len(search_modes)
			self.plan_path()
			window._update_label('search', 'Search Type: '+SearchModes(self.search_mode).name)
		# Plan a path using the current search mode?
		elif symbol == pyglet.window.key.SPACE:
			self.plan_path()
		elif symbol == pyglet.window.key.UP:
			self.search_limit += 1
			window._update_label('status', 'Status: limit=%d' % self.search_limit)
			self.plan_path()
		elif symbol == pyglet.window.key.DOWN:
			if self.search_limit > 0:
				self.search_limit -= 1
				window._update_label('status', 'Status: limit=%d' % self.search_limit)
				self.plan_path()
		elif symbol == pyglet.window.key._0:
			self.search_limit = 0
			window._update_label('status', 'Status: limit=%d' % self.search_limit)
			self.plan_path()
   
	def check_collisions(self):
		for i in range(len(self.agent)):
			for j in range(i + 1, len(self.agent)):
				a = self.agent[i]
				b = self.agent[j]
				idx_a = a.current_tile_idx()
				idx_b = b.current_tile_idx()
				if idx_a is not None and idx_a == idx_b:
					self.on_collision(idx_a, a, b)
    
	def on_collision(self, tile_idx, a, b):
		print(f"[COLLISION] Tile {tile_idx} is now dangerous! Cost spiked.")
		box = self.world.boxes[tile_idx]
		box.threat = 20.0
		# save original color and flash red
		if not hasattr(box, 'original_color'):
			box.original_color = tuple(box.box.color)
		box.box.color = COLOUR_NAMES['RED']
		self.world.reset_navgraph()
		# respawn loser (agent b)
		new_start = random.randint(0, len(self.world.boxes) - 1)
		while self.world.boxes[new_start].type == "WALL":
			new_start = random.randint(0, len(self.world.boxes) - 1)
		b.start_idx = new_start
		b.target_idx = random.randint(0, len(self.world.boxes) - 1)
		while self.world.boxes[b.target_idx].type == "WALL" or b.target_idx == b.start_idx:
			b.target_idx = random.randint(0, len(self.world.boxes) - 1)
		b.plan_path(self.world)
		print(f"[RESPAWN] Agent respawned at tile {b.start_idx}, heading to {b.target_idx}")
		# repath everyone else
		for agent in self.agent:
			if agent is not b:
				print(f"[REPATH] Agent avoiding tile {tile_idx}, replanning...")
				agent.plan_path(agent.world)
				