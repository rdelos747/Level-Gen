import pygame
import random
import math
import copy
from globals import *
from gen_types import *
from tile import *

BIRTH = 3
DEATH = 1

GRASS_CHANCE = 20
GRASS_CYCLES = 2
GRASS_BIRTH = 3
GRASS_DEATH = 1
T_GRASS_CHANCE = 10
T_GRASS_CYCLES = 2
T_GRASS_BIRTH = 2
T_GRASS_DEATH = 1

WATER_CHANCE = 10
WATER_CYCLES = 10
WATER_BIRTH = 3
WATER_DEATH = 1
D_WATER_CHANCE = 10
D_WATER_CYCLES = 2
D_WATER_BIRTH = 2
D_WATER_DEATH = 1

MUSHROOM_MIN = 5
MUSHROOM_MAX = 8
MUSHROOM_FLOOR_CHANCE = 30
MUSHROOM_CHANCE = 15
MUSHROOM_FLOOR_CYCLES = 2
MUSHROOM_BIRTH = 3
MUSHROOM_DEATH = 1

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

	def getSurroundingSub(self, j, i, a, h, w):
		jMin = -1 if j > 0 else 0
		jMax = 1 if j < h - 1 else 0
		iMin = -1 if i > 0 else 0
		iMax = 1 if i < w - 1 else 0

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
		#the nice thing about doing it this way, is that different level types can call
		#the following functions different number of times
		self.addWater()
		self.addGrass()

		self.addMushrooms('red')
		self.addMushrooms('purple')

	def addFlavors(self):
		pass

	def addGrass(self):
		#PROCESS SHALLOW
		shallowLayer = self.autoArray(GRASS_CHANCE)
		shallowCycles = GRASS_CYCLES
		while shallowCycles > 0:
			shallowCycles -= 1
			array = copy.deepcopy(shallowLayer)

			for j in range(Y_MAX):
				for i in range(X_MAX):
					n = self.getSurrounding(j, i, shallowLayer)
					if shallowLayer[j][i] == 1 and n <= GRASS_DEATH:
						array[j][i] = 0
					elif shallowLayer[j][i] == 0 and n >= GRASS_BIRTH:
						array[j][i] = 1
			shallowLayer = copy.deepcopy(array)

		#PROCESS DEEP
		deepLayer = self.autoArray(T_GRASS_CHANCE)
		deepCycles = T_GRASS_CYCLES
		while deepCycles > 0:
			deepCycles -= 1
			array = copy.deepcopy(deepLayer)

			for j in range(Y_MAX):
				for i in range(X_MAX):
					n = self.getSurrounding(j, i, deepLayer)
					if deepLayer[j][i] == 1 and n <= T_GRASS_DEATH:
						array[j][i] = 0
					elif deepLayer[j][i] == 0 and n >= T_GRASS_BIRTH:
						array[j][i] = 1
			deepLayer = copy.deepcopy(array)

		for j in range(Y_MAX):
			for i in range(X_MAX):
				if self.typeAt(j, i, 'floor') and deepLayer[j][i] == 1 and shallowLayer[j][i] == 1:
					self.setType(j, i, 'tall grass')
				elif self.typeAt(j, i, 'floor') and shallowLayer[j][i] == 1:
					self.setType(j, i, 'grass')

	def addWater(self):
		#PROCESS SHALLOW
		shallowLayer = self.autoArray(WATER_CHANCE)
		shallowCycles = WATER_CYCLES
		while shallowCycles > 0:
			shallowCycles -= 1
			array = copy.deepcopy(shallowLayer)

			for j in range(Y_MAX):
				for i in range(X_MAX):
					n = self.getSurrounding(j, i, shallowLayer)
					if shallowLayer[j][i] == 1 and n <= WATER_DEATH:
						array[j][i] = 0
					elif shallowLayer[j][i] == 0 and n >= WATER_BIRTH:
						array[j][i] = 1
			shallowLayer = copy.deepcopy(array)

		#PROCESS DEEP
		deepLayer = self.autoArray(D_WATER_CHANCE)
		deepCycles = D_WATER_CYCLES
		while deepCycles > 0:
			deepCycles -= 1
			array = copy.deepcopy(deepLayer)

			for j in range(Y_MAX):
				for i in range(X_MAX):
					n = self.getSurrounding(j, i, deepLayer)
					if deepLayer[j][i] == 1 and n <= D_WATER_DEATH:
						array[j][i] = 0
					elif deepLayer[j][i] == 0 and n >= D_WATER_BIRTH:
						array[j][i] = 1
			deepLayer = copy.deepcopy(array)

		for j in range(Y_MAX):
			for i in range(X_MAX):
				if self.typeAt(j, i, 'floor') and deepLayer[j][i] == 1 and shallowLayer[j][i] == 1:
					self.setType(j, i, 'deep water')
				elif self.typeAt(j, i, 'floor') and shallowLayer[j][i] == 1:
					self.setType(j, i, 'water')

				# if deepLayer[j][i] == 1 and shallowLayer[j][i] == 1:
				# 	self.setType(j, i, 'deep water')
				# elif shallowLayer[j][i] == 1:
				# 	self.setType(j, i, 'water')

	def addMushrooms(self, mType):
		randW = rand(MUSHROOM_MIN, MUSHROOM_MAX)
		randH = rand(MUSHROOM_MIN, MUSHROOM_MAX)
		shallowLayer = []
		for j in range(randH):
			row = []
			for i in range(randW):
				if chance() < MUSHROOM_FLOOR_CHANCE:
					row.append(1)
				else:
					row.append(0)
			shallowLayer.append(row)

		deepLayer = []
		for j in range(randH):
			row = []
			for i in range(randW):
				if chance() < MUSHROOM_CHANCE:
					row.append(1)
				else:
					row.append(0)
			deepLayer.append(row)

		shallowCycles = MUSHROOM_FLOOR_CYCLES
		while shallowCycles > 0:
			shallowCycles -= 1
			array = copy.deepcopy(shallowLayer)

			for j in range(randH):
				for i in range(randW):
					n = self.getSurroundingSub(j, i, shallowLayer, randH, randW)
					if shallowLayer[j][i] == 1 and n <= MUSHROOM_DEATH:
						array[j][i] = 0
					elif shallowLayer[j][i] == 0 and n >= MUSHROOM_BIRTH:
						array[j][i] = 1
			shallowLayer = copy.deepcopy(array)

		randX = 0
		randY = 0

		numTries = 20
		while numTries > 0:
			
			numTries -= 1
			randX = rand(0, X_MAX - randW)
			randY = rand(0, Y_MAX - randH)

			#try to at least place rand point on a floor tile
			if self.typeAt(j + randY, i + randX, 'floor') or self.typeAt(j + randY, i + randX, 'grass'):
				numTries = 0

		for j in range(randH):
			for i in range(randW):
				if self.typeAt(j + randY, i + randX, 'floor') or self.typeAt(j + randY, i + randX, 'grass'):
					if deepLayer[j][i] == 1 and shallowLayer[j][i] == 1:
						self.setType(j + randY, i + randX, mType + ' mushroom')
					elif shallowLayer[j][i] == 1:
						self.setType(j + randY, i + randX, mType + ' mushroom floor')