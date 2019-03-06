import pygame
import random
import math
import copy
from globals import *
from room import *

# ###########################
# BOARD / ROOM GLOBALS
# ###################################################

TYPE_ARRAY = [
	" ",
	c6+".",
	c1+"#",
	c0+"+",
	c0+"9"
]

DOOR_CHANCE = 3
SQUARE_CHANCE = 30
LARGE_BLOB_CHANCE = 50

NUM_CYCLES = 20
DOOR_REMOVAL_CHANCE = 0.6
HOLE_CHANCE = 0.1
BRIDGE_CHANCE = 10

# ###########################
# B O A R D
# ###################################################

class Board:
	#def __init__(self, screen):
	def __init__(self):
		#self.s = screen
		self.total = 0
		self.tiles = [[0 for i in range(X_MAX)] for j in range(Y_MAX)]
		self.rooms = []
		self.rounds = NUM_CYCLES
		self.found = []

		while self.rounds > 0:
			if self.rounds == NUM_CYCLES:
				c = chance()
				if c <= LARGE_BLOB_CHANCE:
					self.addRoom('large blob')
				elif c <= SQUARE_CHANCE:
					self.addRoom('square')
				else:
					self.addRoom('blob')
			else:
				c = chance()
				if c <= SQUARE_CHANCE:
					self.addRoom('square')
				else:
					self.addRoom('blob')

			self.rounds -= 1

		self.removeBadDoors()
		self.addHoles()
		self.addDoubleHoles()
		self.addBridges()

		#these should always be called at the very end
		self.fixBadDoors()
		self.fixBrokenWalls()
		
	def printTiles(self):
		for j in range(Y_MAX):
			s = ""
			for i in range(X_MAX):
				s += str(TYPE_ARRAY[self.tiles[j][i]])
			print(s)

	def addRoom(self, roomType):
		self.total += 1
		numTrys = 20
		while numTrys > 0:
			numTrys -= 1

			r = Room(roomType)

			#consider new rooms types
			#T square
			#large blob? (perhaps somtimes can be first room on board)

			if len(self.rooms) == 0:
				numTrys = 0
				randX = rand(0, X_MAX - r.w)
				randY = rand(0, Y_MAX - r.h)
				for j in range(r.h):
					for i in range(r.w):
						if (self.tiles[randY + j][randX + i] == 0):
							self.tiles[randY + j][randX + i] = r.tiles[j][i]
				self.rooms.append(r)
			elif self.checkAvailable(r):
				numTrys = 0
				for j in range(r.h):
					for i in range(r.w):
						if (self.tiles[r.originY + j][r.originX + i] != 2 or r.tiles[j][i] == 3):
							self.tiles[r.originY + j][r.originX + i] = r.tiles[j][i]
				self.rooms.append(r)

		#return self.total

	def checkAvailable(self, r):
		numTrys = 100
		foundSpace = False
		while numTrys > 0:
			numTrys -= 1

			#pick a random point in level to place 
			#the top left corner of the room
			r.originX = rand(0, X_MAX - r.w)
			r.originY = rand(0, Y_MAX - r.h)

			goodSpace = True

			# for each cell in room
			for j in range(0, r.h):
				for i in range(0, r.w):
					if (self.tiles[j + r.originY][i + r.originX] == 1):
						#if this palce in room is a floor, nah
						goodSpace = False

			goodDoor = False
			doorX = 0
			doorY = 0
			for k in r.doors:
				d_y = r.originY + k[0]
				d_x = r.originX + k[1]
				if self.tiles[d_y][d_x] > 1 and self.getSurrounding(d_y, d_x) == 1:
				#if self.tiles[d_y][d_x] > 1: #not sure why self.getSurrounding.. is necessary,
				# but rooms are not fully connected otherwise
					goodDoor = True
					doorX = k[1]
					doorY = k[0]

			if goodSpace and goodDoor:
				numTrys = 0
				foundSpace = True
				#r.tiles[doorY][doorX] = 3
				for k in r.doors:
					r.tiles[k[0]][k[1]] = 3
					
		return foundSpace

	def getSurrounding(self, j, i):
		jMin = -1 if j > 0 else 0
		jMax = 1 if j < Y_MAX - 1 else 0
		iMin = -1 if i > 0 else 0
		iMax = 1 if i < X_MAX - 1 else 0

		n = 0
		for jj in range(jMin, jMax + 1):
			for ii in range(iMin, iMax + 1):
				if not(jj == -1 and ii == -1) and not(jj == 1 and ii == -1) and not(jj == -1 and ii == 1) and not(jj == 1 and ii == 1):
					if self.tiles[jj + j][ii + i] == 1 and not(jj == 0 and ii == 0):
						n += 1
		return n

	def getSurroundingDoors(self, j, i):
		jMin = -1 if j > 0 else 0
		jMax = 1 if j < Y_MAX - 1 else 0
		iMin = -1 if i > 0 else 0
		iMax = 1 if i < X_MAX - 1 else 0

		n = 0
		for jj in range(jMin, jMax + 1):
			for ii in range(iMin, iMax + 1):
				if not(jj == -1 and ii == -1) and not(jj == 1 and ii == -1) and not(jj == -1 and ii == 1) and not(jj == 1 and ii == 1):
					if self.tiles[jj + j][ii + i] == 3 and not(jj == 0 and ii == 0):
						n += 1
		return n

	# def getSurroundingRecusion(self, j, i):
	# 	jMin = -1 if j > 0 else 0
	# 	jMax = 1 if j < self.h - 1 else 0
	# 	iMin = -1 if i > 0 else 0
	# 	iMax = 1 if i < self.w - 1 else 0

	# 	self.found.append((j, i))
	# 	self.current.append((j, i))

	# 	for jj in range(jMin, jMax + 1):
	# 		for ii in range(iMin, iMax + 1):
	# 			if not(jj == -1 and ii == -1) and not(jj == 1 and ii == -1) and not(jj == -1 and ii == 1) and not(jj == 1 and ii == 1):
	# 				if self.tiles[jj + j][ii + i] == 1 and (jj + j, ii + i) not in self.found:
	# 					self.getSurroundingRecusion(jj + j, ii + i)

	def removeBadDoors(self):
		for j in range(Y_MAX):
			for i in range(X_MAX):
				if self.tiles[j][i] == 3 and self.getSurrounding(j, i) != 2:
					self.tiles[j][i] = 2

	def fixBadDoors(self):
		for j in range(Y_MAX):
			for i in range(X_MAX):
				if self.tiles[j][i] == 3 and self.getSurrounding(j, i) != 2:
					self.tiles[j][i] = 1

	def addHoles(self):
		for j in range(1, Y_MAX - 1):
			for i in range(1, X_MAX -1):
				if self.tiles[j][i] == 2 and self.getSurroundingDoors(j, i) == 0:
					#vertical hole
					if self.tiles[j - 1][i] == 1 and self.tiles[j + 1][i] == 1 and random.random() < HOLE_CHANCE:
						self.tiles[j][i] = 1
					#horizontal hole
					if self.tiles[j][i - 1] == 1 and self.tiles[j][i + 1] == 1 and random.random() < HOLE_CHANCE:
						self.tiles[j][i] = 1

	def addDoubleHoles(self):
		for j in range(1, Y_MAX - 4):
			for i in range(1, X_MAX - 4):
				if self.tiles[j][i] == 1:
					#vertical
					if self.tiles[j + 1][i] == 2 and self.tiles[j + 2][i] == 2 and self.tiles[j + 3][i] == 1 and random.random() < HOLE_CHANCE:
						self.tiles[j + 1][i] = 1
						self.tiles[j + 2][i] = 1
					#horizontal
					if self.tiles[j][i + 1] == 2 and self.tiles[j][i + 2] == 2 and self.tiles[j][i + 3] == 1 and random.random() < HOLE_CHANCE:
						self.tiles[j][i + 1] = 1
						self.tiles[j][i + 2] = 1

	def addBridges(self):
		# horizontal bridges
		for j in range(Y_MAX):
			currentBridge = []
			for i in range(X_MAX - 2):
				if self.tiles[j][i] == 1 and self.tiles[j][i + 1] == 2 and self.tiles[j][i + 2] == 0:
					ii = i + 1
					makeBridge = True
					foundBridge = False
					while ii < X_MAX - 2 and makeBridge:
						currentBridge.append((j, ii))
						if self.tiles[j][ii] == 2 and self.tiles[j][ii + 1] == 1:
							makeBridge = False
							foundBridge = True
						ii += 1
					if foundBridge and chance() < BRIDGE_CHANCE:
						for k in currentBridge:
							if self.tiles[k[0] - 1][k[1]] != 3:
								self.tiles[k[0] - 1][k[1]] = 2
							self.tiles[k[0]][k[1]] = 1
							if self.tiles[k[0] + 1][k[1]] != 3:
								self.tiles[k[0] + 1][k[1]] = 2
						currentBridge = []

		# vertical bridges
		for i in range(X_MAX):
			currentBridge = []
			for j in range(Y_MAX - 2):
				if self.tiles[j][i] == 1 and self.tiles[j + 1][i] == 2 and self.tiles[j + 2][i] == 0:
					jj = j + 1
					makeBridge = True
					foundBridge = False
					while jj < Y_MAX - 2 and makeBridge:
						currentBridge.append((jj, i))
						if self.tiles[jj][i] == 2 and self.tiles[jj + 1][i] == 1:
							makeBridge = False
							foundBridge = True
						jj += 1
					if foundBridge and chance() < BRIDGE_CHANCE:
						for k in currentBridge:
							self.tiles[k[0]][k[1] - 1] = 2
							self.tiles[k[0]][k[1]] = 1
							self.tiles[k[0]][k[1] + 1] = 2
						currentBridge = []

	def fixBrokenWalls(self):
		for j in range(1, Y_MAX - 1):
			for i in range(1, X_MAX -1):
				if self.tiles[j][i] == 0 and self.getSurrounding(j, i) != 0:
					self.tiles[j][i] = 2