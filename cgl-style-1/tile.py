import pygame
from globals import *
from gen_types import *

class Tile:
	def __init__(self, s, t, j, i):
		self.i = i
		self.j = j
		self.s = s
		self.t = t

	def render(self):
		tileFont = TYPES[self.t]['font']
		tileIcon = TYPES[self.t]['icon']
		tileColor = TYPES[self.t]['color'][rand(0, len(TYPES[self.t]['color']) - 1)]
		#print(tileColor)
		tileBackground = TYPES[self.t]['background'][rand(0, len(TYPES[self.t]['background']) - 1)]
		#print(tileColor)

		tileRect = pygame.Rect(self.i * TILE_W, self.j * TILE_H, TILE_W, TILE_H)
		text = tileFont.render(tileIcon, True, pygame.Color('0x'+tileColor))
		textRect = text.get_rect()
		textRect.center = tileRect.center

		pygame.draw.rect(self.s, pygame.Color('0x'+tileBackground), tileRect)
		self.s.blit(text, textRect)