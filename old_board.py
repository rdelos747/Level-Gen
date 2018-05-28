import pygame
import random
from gen_types import *
from tile import *

SQUARE_ROOM_MIN = 4
SQUARE_ROOM_MAX = 8
ROOM_MIN_W = 5
ROOM_MAX_W = 10
ROOM_MIN_H = 5
ROOM_MAX_H = 10
RAND_CHANCE = 3
BIRTH = 3
DEATH = 1
#OVERCROWD = 4
#STARVE = 1

#BLOBS
MIN_NUM_BLOBS = 5
MAX_NUM_BLOBS = 10
MIN_BLOB_W = 20
MAX_BLOB_W = 40
MIN_BLOB_H = 15
MAX_BLOB_H = 30

# TASKS = [
# 	'init blobs',
# 	'generate',
# 	'generate',
# 	'generate',
# 	'wall',
# 	'sanitize',
# 	'convert lone walls',
# 	'add holes',
# 	'sanitize',
# 	'sanitize',
# 	'convert lone walls',
# 	'add holes'
# ]
TASKS = [
	'choose space',
	'choose space',
	'choose space',
	'choose space',
	'choose space',
	'choose space',
	'choose space',
	'sanitize',
	'sanitize',
	'sanitize'
]

class Board:
	def __init__(self, s):
		self.s = s
		self.tiles = []
		self.taskNum = 0
		self.nextX = -1
		self.nextY = -1

		#create initial tiles
		#randomized 0 or 1
		for j in range(Y_MAX):
			row = []
			for i in range(X_MAX):
				#if random.randint(0, RAND_CHANCE) == 0:
				#	row.append(Tile(self.s, 'wall', i, j))
				#else:

				#trying blob method, so don't need above logic
				row.append(Tile(self.s, 'none', i, j))
			self.tiles.append(row)

	# ########################
	# R E N D E R
	# ####################################

	def render(self):
		print("render")
		for j in range(Y_MAX):
			for i in range(X_MAX):
				self.tiles[j][i].render()

	# ########################
	# A R R A Y
	# ####################################

	def getTileVals(self):
		a = []
		for j in range(Y_MAX):
			row = []
			for i in range(X_MAX):
				row.append(TYPES[self.tiles[j][i].t][4])
			a.append(row)
		return a

	def writeTiles(self, a):
		for j in range(Y_MAX):
			for i in range(X_MAX):
				self.tiles[j][i].t = TYPE_INDEX[a[j][i]]

	def getSurrounding(self, j, i, t):
		jMin = -1 if j > 0 else 0
		jMax = 1 if j < Y_MAX - 1 else 0
		iMin = -1 if i > 0 else 0
		iMax = 1 if i < X_MAX - 1 else 0

		n = 0
		for jj in range(jMin, jMax + 1):
			for ii in range(iMin, iMax + 1):
				if self.tiles[jj + j][ii + i].t == t and not(jj == 0 and ii == 0):
					n += 1
		return n

	# ########################
	# C R E A R E  D R I V E R
	# ####################################

	def create(self):
		if (self.taskNum < len(TASKS)):
			if (TASKS[self.taskNum] == 'generate'):
				self.generate()
			elif (TASKS[self.taskNum] == 'wall'):
				self.makeWalls()
			elif (TASKS[self.taskNum] == 'init blobs'):
				self.initBlobs()
			elif (TASKS[self.taskNum] == 'sanitize'):
				self.sanitize()
			elif (TASKS[self.taskNum] == 'add holes'):
				self.addHoles()
			elif (TASKS[self.taskNum] == 'convert lone walls'):
				self.convertLoneWalls()

			elif (TASKS[self.taskNum] == 'choose space'):
				self.chooseSpaceType()

			self.taskNum += 1

	# ########################
	# G E N
	# ####################################

	def initBlobs(self):
		numBlobs = random.randint(MIN_NUM_BLOBS, MAX_NUM_BLOBS)
		for _ in range(numBlobs):
			blobW = random.randint(MIN_BLOB_W, MAX_BLOB_W)
			blobH = random.randint(MIN_BLOB_H, MAX_BLOB_H)
			blobX = random.randint(0, X_MAX - blobW)
			blobY = random.randint(0, Y_MAX - blobH)

			for j in range(blobH):
				for i in range(blobW):
					if (random.randint(0, RAND_CHANCE) == 0):
						self.tiles[j + blobY][i + blobX].t = 'floor'
					else:
						self.tiles[j + blobY][i + blobX].t = 'none'

	def chooseSpaceType(self):
		print(" ")
		print("choosing type:")
		self.findNextPoint()
		print("searching at: " + str(self.nextY) + " " + str(self.nextX))
		print("====================")
		if random.randint(0, 1) == 0:
			self.generateBlob()
		else:
			self.generateRoom()

	def findNextPoint(self):
		if self.nextX == -1 and self.nextY == -1:
			#must be first time
			self.nextX = random.randint(15, X_MAX - 15)
			self.nextY = random.randint(15, Y_MAX - 15)
		else:
			searchingForWall = True
			while(searchingForWall):
				randX = random.randint(10, X_MAX - 10)
				randY = random.randint(10, Y_MAX - 10)

				if self.tiles[randY][randX].t == 'wall' and self.getSurrounding(randY, randX, 'none') > 0:
					self.nextX = randX
					self.randY = randY
					searchingForWall = False

	def generateBlob(self):
		print("generating blob")
		blobW = random.randint(MIN_BLOB_W, MAX_BLOB_W)
		blobH = random.randint(MIN_BLOB_H, MAX_BLOB_H)
		blobX = random.randint(0, X_MAX - blobW)
		blobY = random.randint(0, Y_MAX - blobH)

		for j in range(blobH):
			for i in range(blobW):
				if self.tiles[j + blobY][i + blobX].t != 'wall':
					if (random.randint(0, RAND_CHANCE) == 0):
						self.tiles[j + blobY][i + blobX].t = 'floor'
					else:
						self.tiles[j + blobY][i + blobX].t = 'none'

		self.generate()
		self.generate()
		self.generate()
		self.generate()
		self.makeWalls()

	def generateRoom(self):
		print("generating room")
		roomW = random.randint(ROOM_MIN_W, ROOM_MAX_W)
		roomH = random.randint(ROOM_MIN_H, ROOM_MAX_H)
		roomX = random.randint(0, X_MAX - roomW)
		roomY = random.randint(0, Y_MAX - roomH)
		#roomX = random.randint(self.nextX - 10, self.nextX)

		for j in range(roomH):
			for i in range(roomW):
				if j == 0 or j == roomH - 1 or i == 0 or i == roomW - 1:
					self.tiles[j + roomY][i + roomX].t = 'wall'
				else:
					self.tiles[j + roomY][i + roomX].t = 'floor'

	# CELL AUTO
	def generate(self):
		print("generating")
		array = self.getTileVals()
		for j in range(Y_MAX):
			for i in range(X_MAX):
				n = self.getSurrounding(j, i, 'floor')
				#if self.tiles[j][i].t != 'wall':
				if self.tiles[j][i].t != 'none' and n <= DEATH:
					array[j][i] = TYPES['none'][4]
				elif (self.tiles[j][i].t == 'none' and n >= BIRTH):
					array[j][i] = TYPES['floor'][4]

		self.writeTiles(array)

	def makeWalls(self):
		print("making walls")
		array = self.getTileVals()

		for j in range(Y_MAX):
			for i in range(X_MAX):

				if self.tiles[j][i].t == 'none' and self.getSurrounding(j, i, 'floor') > 0:
					array[j][i] = TYPES['wall'][4]

				if j == 0 and self.tiles[j][i].t == 'floor':
					array[j][i] = TYPES['wall'][4]
				if j == Y_MAX - 1 and self.tiles[j][i].t == 'floor':
					array[j][i] = TYPES['wall'][4]
				if i == 0 and self.tiles[j][i].t == 'floor':
					array[j][i] = TYPES['wall'][4]
				if i == X_MAX - 1 and self.tiles[j][i].t == 'floor':
					array[j][i] = TYPES['wall'][4]

		self.writeTiles(array)

	def sanitize(self):
		print('sanitizing')
		array = self.getTileVals()

		for j in range(Y_MAX):
			for i in range(X_MAX):
				if self.tiles[j][i].t == 'wall' and self.getSurrounding(j, i, 'wall') > 5:
					array[j][i] = TYPES['floor'][4]
		self.writeTiles(array)
		self.makeWalls()

	def convertLoneWalls(self):
		print('clearing lone walls')
		array = self.getTileVals()

		for j in range(Y_MAX):
			for i in range(X_MAX):
				if self.tiles[j][i].t == 'wall' and self.getSurrounding(j, i, 'floor') >= 7:
					array[j][i] = TYPES['floor'][4]

		self.writeTiles(array)

	def addHoles(self):
		print('adding holes')
		array = self.getTileVals()

		for j in range(Y_MAX):
			for i in range(X_MAX):
				if self.tiles[j][i].t == 'floor' and self.getSurrounding(j, i, 'wall') >= 6:
					for jj in range(j - 1, j + 2):
						for ii in range(i - 1, i + 2):
							array[jj][ii] = TYPES['none'][4]

		self.writeTiles(array)
		array = self.getTileVals()

		for j in range(Y_MAX):
			for i in range(X_MAX):
				if self.tiles[j][i].t == 'floor' and self.getSurrounding(j, i, 'none') > 0:
					array[j][i] = TYPES['wall'][4]

		self.writeTiles(array)



	# def getSurroundingWalls(self, j, i):
	# 	jMin = -1 if j > 0 else 0
	# 	jMax = 1 if j < Y_MAX - 1 else 0
	# 	iMin = -1 if i > 0 else 0
	# 	iMax = 1 if i < X_MAX - 1 else 0

	# 	n = 0
	# 	for jj in range(jMin, jMax + 1):
	# 		for ii in range(iMin, iMax + 1):
	# 			if self.tiles[jj + j][ii + i].t == 'wall' and not(jj == 0 and ii == 0):
	# 				n += 1
	# 	return n




# if len(self.rooms) == 0:
	# 	randX = rand(0, X_MAX -r.w)
	# 	randY = rand(0, Y_MAX - r.h)
	# else:
	# 	room = self.rooms[rand(0, len(self.rooms) - 1)]
	# 	rand_dir = rand(0, 3)

	# 	if rand_dir == 0: #up
	# 		randX = rand(room.originX - (r.w - 3), room.originX + (room.w - 3))
	# 		randY = room.originY - (r.h - 1)

	# 		doorMinX = max(randX, room.originX) + 1
	# 		doorMaxX = min(randX + r.w, room.originX + room.w) - 2
			
	# 		doorX = rand(doorMinX, doorMaxX)
	# 		doorY = randY + (r.h - 1)

	# 	elif rand_dir == 1: #down
	# 		randX = rand(room.originX - (r.w - 3), room.originX + (room.w - 3))
	# 		randY = room.originY + (room.h - 1)

	# 		doorMinX = max(randX + 1, room.originX + 1)
	# 		doorMaxX = min((randX + r.w) - 2, (room.originX + room.w) - 2)

	# 		doorX = rand(doorMinX, doorMaxX)
	# 		doorY = randY

	# 	elif rand_dir == 2: #right
	# 		randX = room.originX + (room.w - 1)
	# 		randY = rand(room.originY - (r.h - 3), room.originY + (room.h - 3))

	# 		doorMinY = max(randY, room.originY) + 1
	# 		doorMaxY = min(randY + r.h, room.originY + room.h) - 2

	# 		doorX = randX
	# 		doorY = rand(doorMinY, doorMaxY)

	# 	elif rand_dir == 3: #right
	# 		randX = room.originX - (r.w - 1)
	# 		randY = rand(room.originY - (r.h - 3), room.originY + (room.h - 3))

	# 		doorMinY = max(randY, room.originY) + 1
	# 		doorMaxY = min(randY + r.h, room.originY + room.h) - 2

	# 		doorX = randX + (r.w - 1)
	# 		doorY = rand(doorMinY, doorMaxY)

	# r.originX = randX
	# r.originY = randY