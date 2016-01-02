"""
Clone of 2048 game.

Tri Minh Cao
trimcao@gmail.com
Sep 9, 2015
"""

#import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # replace with your code
    new_line = []
    zeroes_count = 0
    for index in range(0, len(line)):
        if (line[index] == 0):
            zeroes_count += 1
        else:
            new_line.append(line[index])
    for index in range(0, zeroes_count):
        new_line.append(0)
        
    move(new_line)    
    merge_helper(new_line)
    move(new_line)
    return new_line

def move(line):
    """
    Function that moves all the blocks to the left
    """
    step_count = 0
    for index in range(0, len(line)):
        while(line[index] == 0) and (step_count < len(line)):
            del line[index]
            line.append(0)
            step_count += 1
            
def merge_helper(line):
    """
    Helper method for merge.
    """
    for index in range(0, len(line) - 1):
        if (line[index] == line[index + 1]):
            if line[index] == 0:
                break
            else:
                line[index] = 2 * line[index]
                line[index + 1] = 0
        
    return line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    TILE = [2, 2, 2, 2, 4, 2, 2, 2, 2, 2]

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self._grid = [[row + col for col in range(grid_width)]
                           for row in range(grid_height)]
        self._initial_list = {UP: [], DOWN: [], LEFT: [], RIGHT: []}
        # Add a dictionary that contains the initial lists
        for idx in range(grid_width):
            self._initial_list[UP].append((0, idx))
            self._initial_list[DOWN].append((grid_height - 1, idx))
        for idx in range(grid_height):
            self._initial_list[LEFT].append((idx, 0))
            self._initial_list[RIGHT].append((idx, grid_width - 1))
        #print self._initial_list
        self.reset()
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        for row in range(self._height):
            for col in range(self._width):
                self._grid[row][col] = 0
        self.new_tile()
        self.new_tile()
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        out = ""
        for row in range(self._height):
            for col in range(self._width):
                out += str(self._grid[row][col]) + " "
            out+= "\n"
        return out

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        changed = False
        initial = self._initial_list[direction]
        offset = OFFSETS[direction]
        # Determine the steps for traversing 
        if (offset[0] == 0):
            steps = self._width
        else:
            steps = self._height

        for each in initial:
            temp_list = []
            for step in range(steps):
                row = each[0] + step * offset[0]
                col = each[1] + step * offset[1]
                temp_list.append(self.get_tile(row, col))
            temp_list = merge(temp_list)
            for step in range(steps):
                row = each[0] + step * offset[0]
                col = each[1] + step * offset[1]
                if (temp_list[step] != self.get_tile(row,col)):
                    self.set_tile(row, col, temp_list[step])
                    changed = True
        if (changed): 
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        added = False
        while (not added):
            rand_row = random.randint(0, self._height - 1)
            rand_col = random.randint(0, self._width - 1)
            if (self._grid[rand_row][rand_col] == 0):
                self._grid[rand_row][rand_col] = random.choice(self.TILE)
                added = True

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
#test = TwentyFortyEight(5, 4)
#print test
