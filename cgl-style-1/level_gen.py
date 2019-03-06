import pygame
import math
import sys
import os

#from types import SCREEN_W
from globals import *
from tile import *
from board import *
from level import *

pygame.init()

SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))

board = Board()
#board.printTiles()
level = Level(SCREEN, board)

SCREEN.fill(SCREEN_BK)
#level.render()
pygame.display.update()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit();
			sys.exit();
		elif event.type == pygame.KEYDOWN:
			if (event.key == pygame.K_UP):
				pass


# THINGS TO CONSIDER:
#	LEVEL SIZE MIGHT BE TOO BIG
#	SHOULD MAKE IT MORE LIKELY TO HAVE MULTIPLE ENVIRONMENT TYPES IN SAME LEVEL