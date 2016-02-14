from __future__ import division, print_function, unicode_literals

import pyglet

class Images(object):
	
	Tile_images = ['red', 'floor']
	greytile = pyglet.resource.image('tiles/block_black.png')
	floortile = pyglet.resource.image('tiles/block_floor.png')
	image = {tile: pyglet.resource.image('tiles/block_%s.png' %tile) for tile in Tile_images}
	wizard = pyglet.resource.image('wizard.png')
	frame_yellow = pyglet.resource.image('frame_yellow.png')
	frame_blue = pyglet.resource.image('frame_blue.png')