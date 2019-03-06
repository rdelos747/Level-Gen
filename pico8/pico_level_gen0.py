# Idea: use Pico8 map to pre-make rooms, then read those into an arrays.
# Each array contains rooms that are left/right or up/down.
# Use algorithm to place rooms in psudo-random order.

# Pico8 screen is 16x16 blocks
# Pico8 map is 8x4 screens (128x64 blocks)

# Values:
# 0 empty
# 1 left/right
# 2 cross

# Size 1:
# Each room is 1 screen (16x16)
# Map rows 1 and 2 store left/right (1)
# Map row 3 and 4 stores crosses (2)

# Size 2:
# each room is 1/4 screen (8x8), meaning total rooms are now (16x8)
# Map rows 1 - 3 store left/right
# Map rows 4 - 6 store crosses
# Map rows 7 and 8 store wild cards???
#   perhaps wild cards are stand alone rooms that attach to whatever number they are adjacent to

# option 1:
# add multiple overlapping paths (each guarenteed to be connected) ontop of eachother
# issue: it is possible that one or more paths may not overlap, creating unreachable areas

# option 2:
# create one complete path
# add random 1s and 2s in the remaining 0 space
# for each 1, if a two is above or below, roll to make it a 2
# issue, there will be many unreachable, but small, areas

import random

def printArray(a):
  for row in a:
    s = ''
    for r in row:
      if r == 0:
        s += '  '
      elif r == 1:
        s += '- '
      elif r == 2:
        s += '+ '
    print(s)
  print('')

def printCombined(a, b):
  #make sure arrays are same length :)
  for j in range(len(a)):
    s = ''
    for r in a[j]:
      if r == 0:
        s += '  '
      elif r == 1:
        s += '- '
      elif r == 2:
        s += '+ '
    s += '    '
    for r in b[j]:
      if r == 0:
        s += '  '
      elif r == 1:
        s += '- '
      elif r == 2:
        s += '+ '
    print(s)
  print('')

def chance(n):
  return random.randint(0, 99) < n

def rand():
  return random.randint(0, 99)

def randRange(n, m):
  return random.randint(n, m)

def generateArray(a, xmax, ymax):
  LR_NUM = 1
  C_NUM = 2

  i = randRange(0, xmax - 1)
  j = 0
  lastJ = 0
  d = 1 if chance(50) else -1
  #print('creating path', 'starting at', j, i, d)
  while j < ymax:
    if i < 0 or i >= xmax:
      #if i out of bounds, move back and set space to cross, then move down and reverse direction
      i -= d
      a[j][i] = C_NUM
      d *= -1
      lastJ = j
      j += 1
    elif chance(20) or a[j][i] != 0:
      #else if in bounds and chance < 30, go down, and randomize direction
      a[j][i] = C_NUM
      lastJ = j
      j += 1
      d = 1 if chance(50) else -1
    else:
      #set the current space to 1
      if (lastJ != j):
        lastJ = j
        a[j][i] = C_NUM
      elif a[j][i] == 0:
        a[j][i] = LR_NUM
      i += d
  return a

# option 1
# add paths to the same array until array is dense
def option1(xmax, ymax, times):
  a = [[0 for _ in range(xmax)] for _ in range(ymax)]

  for _ in range(times):
    generateArray(a, xmax, ymax)
    #print('option 1 pass', str(i))
    #printArray(a)
  
  return a

def option2(xmax, ymax):
  a = [[0 for _ in range(xmax)] for _ in range(ymax)]
  generateArray(a, xmax, ymax)
  #print('option 2 basic path')
  #printArray(a)

  for _ in range(100):
    rj = randRange(1, ymax - 2)
    ri = randRange(2, xmax - 2)
    if a[rj][ri] == 0:
      a[rj][ri] = 1 if chance(50) else 2
    elif a[rj][ri] == 1:
      if a[rj - 1][ri] == 2 and chance(30):
        a[rj][ri] = 2
      if a[rj + 1][ri] == 2 and chance(30):
        a[rj][ri] = 2
  
  #print('option 2 with noise')
  #printArray(a)

  return a

o1_small = option1(8, 4, 5)
o1_large = option1(16, 8, 5)

o2_small = option2(8, 4)
o2_large = option2(16, 8)

print('[small] option 1, option 2')
printCombined(o1_small, o2_small)
print('[large] option 1, option 2')
printCombined(o1_large, o2_large)