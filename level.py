import pygame
import random
import math
import copy
from globals import *
from gen_types import *
from tile import *

BIRTH = 3
DEATH = 1

ENV_TYPES = [
	{
		'shallowName': 'grass',
		'shallowChance': 3,
		'shallowCycles':6,
		'shallowBirth':2,
		'shallowDeath':1,
		'deepName': 'tall grass',
		'deepChance':10,
		'deepCycles':2,
		'deepBirth':2,
		'deepDeath':1
	},
	{
		'shallowName': 'water',
		'shallowChance': 2,
		'shallowCycles':6,
		'shallowBirth':2,
		'shallowDeath':1,
		'deepName': 'deep water',
		'deepChance':10,
		'deepCycles':2,
		'deepBirth':2,
		'deepDeath':1
	}
]

class Level:
	def __init__(self, screen, board):
		self.tiles = []
		for j in range(Y_MAX):
			row = []
			for i in range(X_MAX):
				tileType = ''
				if board.tiles[j][i] == 0:
					tileType = 'none'
				elif board.tiles[j][i] == 1:
					tileType = 'floor'
				elif board.tiles[j][i] == 2:
					tileType = 'wall'
				elif board.tiles[j][i] == 3:
					tileType = 'door'

				row.append(Tile(screen, tileType, j, i))
			self.tiles.append(row)

		self.addEnvironments()
		self.addEnvironments()
		self.addEnvironments()

		self.addFlavors()

	def typeAt(self, j, i, t):
		return t == self.tiles[j][i].t

	def setType(self, j, i, t):
		self.tiles[j][i].t = t

	def autoArray(self, c):
		array = []
		for j in range(Y_MAX):
			row = []
			for i in range(X_MAX):
				if chance() < c and self.typeAt(j, i, 'floor'):
					row.append(1)
				else:
					row.append(0)
			array.append(row)
		return array

	def getSurrounding(self, j, i, a):
		jMin = -1 if j > 0 else 0
		jMax = 1 if j < Y_MAX - 1 else 0
		iMin = -1 if i > 0 else 0
		iMax = 1 if i < X_MAX - 1 else 0

		n = 0
		for jj in range(jMin, jMax + 1):
			for ii in range(iMin, iMax + 1):
				if a[jj + j][ii + i] == 1 and not(jj == 0 and ii == 0):
					n += 1
		return n

	def render(self):
		for j in range(Y_MAX):
			for i in range(X_MAX):
				self.tiles[j][i].render()

	def addEnvironments(self):
		randEnvType = ENV_TYPES[rand(0, len(ENV_TYPES) - 1)]
		#randEnvType = ENV_TYPES[0]

		#PROCESS SHALLOW
		shallowLayer = self.autoArray(randEnvType['shallowChance'])
		shallowCycles = randEnvType['shallowCycles']
		while shallowCycles > 0:
			shallowCycles -= 1
			array = copy.deepcopy(shallowLayer)

			for j in range(Y_MAX):
				for i in range(X_MAX):
					n = self.getSurrounding(j, i, shallowLayer)
					if shallowLayer[j][i] == 1 and n <= randEnvType['shallowDeath']:
						array[j][i] = 0
					elif shallowLayer[j][i] == 0 and n >= randEnvType['shallowBirth']:
						array[j][i] = 1
			shallowLayer = copy.deepcopy(array)

		#PROCESS DEEP
		deepLayer = self.autoArray(randEnvType['deepChance'])
		deepCycles = randEnvType['deepCycles']
		while deepCycles > 0:
			deepCycles -= 1
			array = copy.deepcopy(deepLayer)

			for j in range(Y_MAX):
				for i in range(X_MAX):
					n = self.getSurrounding(j, i, deepLayer)
					if deepLayer[j][i] == 1 and n <= randEnvType['deepDeath']:
						array[j][i] = 0
					elif deepLayer[j][i] == 0 and n >= randEnvType['deepBirth']:
						array[j][i] = 1
			deepLayer = copy.deepcopy(array)

		for j in range(Y_MAX):
			for i in range(X_MAX):
				if self.typeAt(j, i, 'floor') and deepLayer[j][i] == 1 and shallowLayer[j][i] == 1:
					self.setType(j, i, randEnvType['deepName'])
				if self.typeAt(j, i, 'floor') and shallowLayer[j][i] == 1:
					self.setType(j, i, randEnvType['shallowName'])
				# if shallowLayer[j][i] == 1:
				# 	self.setType(j, i, randEnvType['shallowName'])
				# if deepLayer[j][i] == 1:
				# 	self.setType(j, i, randEnvType['deepName'])

	def addFlavors(self):
		pass