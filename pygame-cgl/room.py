import random
import math
import copy
from globals import *

SQUARE_MIN_SIZE = 4
SQUARE_MAX_SIZE = 12

BLOB_MIN_SIZE = 5
BLOB_MAX_SIZE = 20
LARGE_BLOB_MIN_SIZE = 20
LARGE_BLOB_MAX_SIZE = 30

CELL_CHANCE = 3
NUM_CELL_AUTOS = 3
NUM_CELL_AUTOS_LARGE = 3
MIN_BEST_LEN = 25

CORRIDOR_CHANCE = 3
CORRIDOR_MIN = 4
CORRIDOR_MAX = 10

BIRTH = 3
DEATH = 1

class Room:
	def __init__(self, room_type):
		self.room_type = room_type
		self.tiles = []
		self.w = 0
		self.h = 0
		self.originX = 0
		self.originY = 0
		self.doors = []

		self.found = []
		self.current = []
		self.best = []

		if self.room_type == 'square':
			self.generateSquare()
		elif self.room_type == 'blob':
			self.generateBlob()
		elif self.room_type == 'large blob':
			self.generateLargeBlob()

		if rand(0, CORRIDOR_CHANCE) == 0:
			self.addCorridor()

		self.makeWalls()
		self.addDoors()
		

	def generateSquare(self):
		self.w = rand(SQUARE_MIN_SIZE, SQUARE_MAX_SIZE)
		self.h = rand(SQUARE_MIN_SIZE, SQUARE_MAX_SIZE)
		for j in range(self.h):
			row = []
			for i in range(self.w):
				if j == 0 or j == self.h - 1 or i == 0 or i == self.w - 1:
					row.append(0)
				else:
					row.append(1)
			self.tiles.append(row)

	def generateBlob(self):
		create_better_blob = True

		while(create_better_blob):
			create_better_blob = False
			self.tiles = []
			self.w = rand(BLOB_MIN_SIZE, BLOB_MAX_SIZE)
			self.h = rand(BLOB_MIN_SIZE, BLOB_MAX_SIZE)

			for j in range(self.h):
				row = []
				for i in range(self.w):
					if rand(0, CELL_CHANCE) == 0:
						row.append(1)
					else:
						row.append(0)
				self.tiles.append(row)

			for _ in range(NUM_CELL_AUTOS):
				self.cellAuto()

			newSize = self.findLargestBlob()

			if newSize < MIN_BEST_LEN:
				create_better_blob = True

	def generateLargeBlob(self):
		create_better_blob = True

		while(create_better_blob):
			create_better_blob = False
			self.tiles = []
			self.w = rand(LARGE_BLOB_MIN_SIZE, LARGE_BLOB_MAX_SIZE)
			self.h = rand(LARGE_BLOB_MIN_SIZE, LARGE_BLOB_MAX_SIZE)

			for j in range(self.h):
				row = []
				for i in range(self.w):
					if rand(0, CELL_CHANCE) == 0:
						row.append(1)
					else:
						row.append(0)
				self.tiles.append(row)

			for _ in range(NUM_CELL_AUTOS_LARGE):
				self.cellAuto()

			newSize = self.findLargestBlob()

			if newSize < MIN_BEST_LEN:
				create_better_blob = True

	def addDoors(self):
		topDoor = 20
		while topDoor > 0:
			topDoor -= 1
			randX = rand(0, self.w - 1)
			randY = 0
			if self.tiles[randY][randX] == 2 and self.tiles[randY + 1][randX] == 1:
				#self.tiles[randY][randX] = 3
				self.doors.append((randY, randX))
				topDoor = 0

		botDoor = 20
		while botDoor > 0:
			botDoor -= 1
			randX = rand(0, self.w - 1)
			randY = self.h - 1
			if self.tiles[randY][randX] == 2 and self.tiles[randY - 1][randX] == 1:
				#self.tiles[randY][randX] = 3
				self.doors.append((randY, randX))
				botDoor = 0

		rightDoor = 20
		while rightDoor > 0:
			rightDoor -= 1
			randX = self.w - 1
			randY = rand(0, self.h - 1)
			if self.tiles[randY][randX] == 2 and self.tiles[randY][randX - 1] == 1:
				#self.tiles[randY][randX] = 3
				self.doors.append((randY, randX))
				rightDoor = 0

		leftDoor = 20
		while leftDoor > 0:
			leftDoor -= 1
			randX = 0
			randY = rand(0, self.h - 1)
			if self.tiles[randY][randX] == 2 and self.tiles[randY][randX + 1] == 1:
				#self.tiles[randY][randX] = 3
				self.doors.append((randY, randX))
				leftDoor = 0

	def printTiles(self):
		for j in range(self.h):
			s = ""
			for i in range(self.w):
				s += str(TYPE_ARRAY[self.tiles[j][i]])
			print(s)

		print("  ")

	def cellAuto(self):
		array = copy.deepcopy(self.tiles)
		for j in range(self.h):
			for i in range(self.w):
				n = self.getSurrounding(j, i)
				if self.tiles[j][i] == 1 and n <= DEATH:
					array[j][i] = 0
				elif (self.tiles[j][i] == 0 and n >= BIRTH):
					array[j][i] = 1

		self.tiles = copy.deepcopy(array)

	def getSurrounding(self, j, i):
		jMin = -1 if j > 0 else 0
		jMax = 1 if j < self.h - 1 else 0
		iMin = -1 if i > 0 else 0
		iMax = 1 if i < self.w - 1 else 0

		n = 0
		for jj in range(jMin, jMax + 1):
			for ii in range(iMin, iMax + 1):
				if self.tiles[jj + j][ii + i] == 1 and not(jj == 0 and ii == 0):
					n += 1
		return n

	def makeWalls(self):
		array = copy.deepcopy(self.tiles)

		for j in range(self.h):
			for i in range(self.w):
				if self.tiles[j][i] == 0 and self.getSurrounding(j, i) > 0:
					array[j][i] = 2

		self.tiles = copy.deepcopy(array)

	def findLargestBlob(self):
		for j in range(self.h):
			for i in range(self.w):
				if self.tiles[j][i] == 1 and (j, i) not in self.found:
					self.getSurroundingRecusion(j, i)

					if len(self.current) > len(self.best):
						self.best = copy.deepcopy(self.current)
					self.current = []

		newMaxH = 0
		newMaxW = 0
		newMinH = self.h
		newMinW = self.w
		for i in self.best:
			if i[0] > newMaxH:
				newMaxH = i[0]
			if i[1] > newMaxW:
				newMaxW = i[1]

			if i[0] < newMinH:
				newMinH = i[0]
			if i[1] < newMinW:
				newMinW = i[1]

		self.h = (newMaxH - newMinH) + 3
		self.w = (newMaxW - newMinW) + 3
		array = [[0 for i in range(self.w)] for j in range(self.h)]
		for i in self.best:
			array[i[0] - (newMinH - 1)][i[1] - (newMinW - 1)] = 1

		self.tiles = copy.deepcopy(array)
		return len(self.best)

	def getSurroundingRecusion(self, j, i):
		jMin = -1 if j > 0 else 0
		jMax = 1 if j < self.h - 1 else 0
		iMin = -1 if i > 0 else 0
		iMax = 1 if i < self.w - 1 else 0

		self.found.append((j, i))
		self.current.append((j, i))

		for jj in range(jMin, jMax + 1):
			for ii in range(iMin, iMax + 1):
				if not(jj == -1 and ii == -1) and not(jj == 1 and ii == -1) and not(jj == -1 and ii == 1) and not(jj == 1 and ii == 1):
					if self.tiles[jj + j][ii + i] == 1 and (jj + j, ii + i) not in self.found:
						self.getSurroundingRecusion(jj + j, ii + i)

	def addCorridor(self):
		randSize = rand(CORRIDOR_MIN, CORRIDOR_MAX)
		# print("X")
		# print(X_MAX)
		# print(self.w + randSize)
		# print("Y")
		# print(Y_MAX)
		# print(self.h + randSize)
		cDir = rand(3, 3)

		array = []
		if cDir == 0: #up
			array = [[0 for i in range(self.w)] for j in range(self.h + randSize)]
			for j in range(self.h):
				for i in range(self.w):
					array[j + randSize][i] = self.tiles[j][i]

			self.h = (self.h + randSize)
			searching = True
			randX = 0
			while searching:
				randX = rand(1, self.w - 2)
				if array[randSize + 2][randX] == 1:
					searching = False

			array[randSize][randX] = 3

			for j in range(1, randSize):
				array[j][randX] = 1

		if cDir == 1: #left
			array = [[0 for i in range(self.w + randSize)] for j in range(self.h)]
			for j in range(self.h):
				for i in range(self.w):
					array[j][i + randSize] = self.tiles[j][i]

			self.w = (self.w + randSize)
			searching = True
			randY = 0
			while searching:
				randY = rand(1, self.h - 2)
				if array[randY][randSize + 2] == 1:
					searching = False

			array[randY][randSize] = 3

			for i in range(1, randSize):
				array[randY][i] = 1

		if cDir == 2: #down
			array = [[0 for i in range(self.w)] for j in range(self.h + randSize)]
			for j in range(self.h):
				for i in range(self.w):
					array[j][i] = self.tiles[j][i]

			searching = True
			randX = 0
			while searching:
				randX = rand(1, self.w - 2)
				if array[self.h - 2][randX] == 1:
					searching = False

			array[self.h - 1][randX] = 3
			
			for j in range(self.h, (self.h + randSize) - 1):
				array[j][randX] = 1

			self.h = (self.h + randSize)

		if cDir == 3: #right
			array = [[0 for i in range(self.w + randSize)] for j in range(self.h)]
			for j in range(self.h):
				for i in range(self.w):
					array[j][i] = self.tiles[j][i]

			searching = True
			randY = 0
			while searching:
				randY = rand(1, self.h - 2)
				if array[randY][self.w - 2] == 1:
					searching = False

			array[randY][self.w - 1] = 3

			for i in range(self.w, (self.w + randSize) - 1):
				array[randY][i] = 1

			self.w = (self.w + randSize)

		self.tiles = copy.deepcopy(array)

