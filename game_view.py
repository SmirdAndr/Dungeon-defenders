

from __future__ import division, print_function, unicode_literals
import six

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pyglet
from pyglet.gl import *
from pyglet import image

from cocos.director import *
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *
from cocos.actions import *
from cocos.sprite import Sprite
from cocos.text import Label

from Images import *
from const import *
from HUD import *
from status import *
from gamemodel import *

import random

class GameView(Layer):
	
	def __init__(self, model):
		super(GameView, self).__init__()
		self.mapx = Quad_side
		self.mapy = Quad_side
		self.end_of_init(model)
		
	def end_of_init(self, model):
		self.model = model
		self.PView = GameView_P(model)
		self.DMView = GameView_DM(model)
		self.curr_player = self.PView
		self.add(self.curr_player)
				
	def next_turn(self):
		if (self.curr_player == self.PView):
			self.remove(self.PView)
			self.add(self.DMView)
			self.curr_player = self.DMView
		elif(self.curr_player == self.DMView):
			self.remove(self.DMView)
			self.add(self.PView)
			self.curr_player = self.PView
			
			
class GameView_DM(GameView):
	
	is_event_handler = True	
	
	def end_of_init(self, model):
		self.HUD = HUD_DM()
		self.add(Buttons())
		self.add(self.HUD, z = -1)
		self.act_tile_sprite = 0
	
	def reload(self):
		self.act_tile_sprite = 0
		
	def draw(self):
		w, h = director.get_window_size()
		if (self.act_tile_sprite):
			self.act_tile_sprite.draw()
		for i in range(self.mapx):
			for j in range (self.mapy):
				c = self.parent.model.map.get((i, j))
				c.draw()
				if (c.open_P == 1):
					Sprite(Images.frame_blue, ((2*i + 1)*Tile_size/2 + left_space, (2*j + 1)*Tile_size/2 + (h - Quad_side*Tile_size)/2)).draw()
				if self.parent.model.map['actual_tile'] == (i, j):
					Sprite(Images.frame_yellow, ((2*i + 1)*Tile_size/2 + left_space, (2*j + 1)*Tile_size/2 + (h - Quad_side*Tile_size)/2)).draw()
		self.parent.model.wizard.draw()
	
	def on_mouse_release(self, x, y, buttons, modifiers):
		
		w, h = director.get_window_size()
		#reaction on map click
		mouse_x, mouse_y = director.get_virtual_coordinates(x, y)
		i = (mouse_x - left_space)//Tile_size
		j = (mouse_y - (h - Quad_side*Tile_size)/2)//Tile_size
		if self.parent.model.map['actual_tile']	!= (-1, -1):
			self.parent.model.map['actual_tile'] = (i, j)
		if (i >= 0) and (j >= 0) and (i < self.mapx) and (j < self.mapy):
			c = self.parent.model.map.get((i, j))
			if (c.open_P == 0):
				c.on_click_DM()
				self.parent.model.map['actual_tile'] = (i, j)
			self.act_tile_sprite = Sprite(c.image, (1500, 800), scale = 4)
		
		#reaction on next turn button  click		
		if (mouse_x <= w) and (mouse_x >= w - Button_size) and (mouse_y >= 0) and (mouse_y <= Button_size):
			self.parent.next_turn()

class Message(Layer):

	def __init__(self, text_title):		
		super(Message, self).__init__()
		w, h = director.get_window_size()
		self.label = Label(text_title, font_name='Times New Roman', font_size=28, anchor_x='center', anchor_y='center', color = (255, 0, 0, 255))
		self.label.position = Quad_side*Tile_size/2 + left_space, (h - Quad_side*Tile_size)/4
			
class GameView_P(GameView):
	
	is_event_handler = True	
	
	def end_of_init(self, model):
		self.HUD = HUD_P()
		self.add(Buttons())
		self.add(self.HUD, z = -1)
		
	def draw(self):
		w, h = director.get_window_size()
		for i in range(self.mapx):
			for j in range (self.mapy):
			
				c = self.parent.model.map.get((i, j))
				if (c.open_P == 1):
					c.draw()
				elif (c.open_P == 0):
					greytile = Sprite(Images.greytile, c.position)
					greytile.draw()
		wiz = self.parent.model.wizard
		wiz.draw()
		for dx, dy in adject_tiles:
			i = wiz.map_posx + dx
			j = wiz.map_posy + dy
			if (i >= 0) and (j >= 0) and (i < self.mapx) and (j < self.mapy):
				Sprite(Images.frame_blue, ((2*i + 1)*Tile_size/2 + left_space, (2*j + 1)*Tile_size/2 + (h - Quad_side*Tile_size)/2)).draw()
	
	def on_mouse_release(self, x, y, buttons, modifiers):
		
		#self.
		w, h = director.get_window_size()
		#reaction on map click
		mouse_x, mouse_y = director.get_virtual_coordinates(x, y)
		i = (mouse_x - left_space)//Tile_size
		j = (mouse_y - (h - Quad_side*Tile_size)/2)//Tile_size
		wiz = self.parent.model.wizard
		if (i >= 0) and (j >= 0) and (i < self.mapx) and (j < self.mapy):
			#print(i, j, wiz.map_posx, wiz.map_posy)
			if ((abs(wiz.map_posx - i) + abs(wiz.map_posy - j) == 1)):
				c = self.parent.model.map.get((i, j))
				c.on_click_P()
				self.parent.model.wizard.replace_hero(i, j)
			else:
				self.label = Message('You must choose an adjective room to the current one')
				self.add(self.label.label)
				self.label.label.do(FadeIn(0) + Delay(3) + FadeOut(1))
			
		#reaction on next turn button  click
		if (mouse_x <= w) and (mouse_x >= w - Button_size) and (mouse_y >= 0) and (mouse_y <= Button_size):
			self.parent.next_turn()
			self.parent.curr_player.reload()
	
		
class Buttons (Layer):
	
	def __init__(self):
		super(Buttons, self).__init__()
		self.img = pyglet.resource.image('next_turn.png')
		w, h = director.get_window_size();
		self.nextturn_button = Sprite(self.img, (w - Button_size/2, Button_size/2))
	
	def draw ( self ):
		self.nextturn_button.draw()

	
def get_newgame_DM():
	gamescene = Scene()
	model = GameModel()
	gamescene.add(GameView(model))
	gamescene.add(Background(), z = -2)
	
	return gamescene