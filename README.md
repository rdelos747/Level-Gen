# Python-Level-Gen

Quick and dirty level generator implemented in python. Heavily inspired by roguelikes like Rogue and Brogue.

Pygame is used to render 'ascii' tiles to the screen, but this is only meant for testing the algorithm.
A better platform should be used for real game development (SpriteKit, SDL, GameMaker, Unity, whatever)

## INSTALLATION

Download the repo and cd into the directory. The run:

```
python3 ./level_gen.py
```

(yes, this requires python3 for some reason)

## Explanation

#### Board Stage
board.py creates a 2d grid of 0's, then creates a room object (from room.py) with its own smaller 2d grid, which can be a square or a blob.
Within a room, 0's are empty space, 1's are floor, 2's are walls, and 3's are doors.

Squares are simple rooms of random width and height with all sides covered in walls. Blobs are populated with random noise of 1's and 0's, and cell auto is run a few times until the floor is satisfactory. In the event two small blobs are generated, the room will choose the largest sub-blob to use as the blob, and adjust the width and height of the room.

The room will then add a door on the perimeter of each side of its grid if candidate spaces can be found. Once the board has a nice room, it will try to add it in an empty space, as long as one of the doors intersect wall space that has been added from a previous door. The board will continue this process a set number of times. Currently, 20 times is a nice tradeoff of speed and density.

After all rooms have been added, the board will attempt to sanitize the grid - clear all 'bad doors', add random holes in the walls to make more room connections, add bridges, and a final sanity check to make sure no empty space can be accessed by any floor tiles.

#### Level Stage
The grid created by the board object is passed to the level object (in level.py), and all tiles are converted to corresponding visual representations. Each tile is now a colored rectangle that contains a character. 

The level now attempts to generate environments by choosing cell auto parameters from a list of environment types. The level creates 2 new grids (shallow and deep) of the same width and height of the level and populates each with noise (1's and 0's). Alive shallow grid tiles are placed into the grid if the level grid contains a floor in their location. Alive deep tiles are then placed if they exist where shallow tiles have been placed. These tiles are then converted to visual representations specified by the environment type (as of now, short/ tall grass, or shallow/ deep water).

The level now attempts to generate flavors, which are smaller and fewer than environments.


## Mechanics

#### Mushrooms

Mushrooms spawn randomly throughout the level. Different colors have different functions. It is possible to see 'mushroom ground' tiles with no actual mushrooms present. The user may plant an existing mushroom at on a 'mushroom ground' tile of the same color, and one will eventually spawn in an adjacent open space.