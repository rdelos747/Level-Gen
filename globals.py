import random
import pygame
pygame.font.init()

SCREEN_W = 1000
SCREEN_H = 800
X_MAX = 70
Y_MAX = 40

FONT_SIZE = 15
FONT_COLOR = (0,0,0)

BACKGROUND_COLOR = '000000'
FLOOR_COLOR = '030303'

TILE_W = 14
TILE_H = 18

SCREEN_BK = pygame.Color('0x000000')
FONT_REG = pygame.font.Font('input-reg.ttf', FONT_SIZE)
FONT_ITL = pygame.font.Font('input-italic.ttf', FONT_SIZE)

c0 = '\033[30m'
c1 = '\033[31m'
c2 = '\033[32m'
c3 = '\033[33m'
c4 = '\033[34m'
c5 = '\033[35m'
c6 = '\033[36m'
c7 = '\033[37m'

def chance():
	return random.randint(0, 100)

def rand(minn, maxx):
	return random.randint(minn, maxx)

def rand_f():
	return random.uniform(0, 1)