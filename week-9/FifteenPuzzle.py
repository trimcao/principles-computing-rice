"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors

Name: Tri Minh Cao
Email: trimcao@gmail.com
Date: November 2015

Note: the GUI only works with CodeSkulptor
"""

import poc_fifteen_gui
import math

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods
    
    def desired_tile(self, row, col):
        """
        The desired tile number from a position in the grid
        """
        return (row * self._width + col)
    
    def move_zero(self, row, col):
        """
        Return the string needed for the zero tile to move to a
        target tile
        """
        zero_row, zero_col = self.current_position(0, 0)
        move = ''
        move_vert = zero_row - row
        move_horiz = zero_col - col
        
        # move up first one step, then move horizontally
        # (but only when zero_row > 1, i.e. zero tile is not in
        # the first two rows)
        if (zero_row > 1 and move_vert > 0):
            move += 'u'
            move_vert -= 1
        
        if (move_horiz < 0):
            move += (-1) * move_horiz * 'r'
        else:
            move += move_horiz * 'l' 
            
        if (move_vert < 0):
            move += (-1) * move_vert * 'd'
        else:
            move += move_vert * 'u'
      
        return move
    
    def position_tile(self, current_row, current_col, target_row, target_col):
        """
        Helper function to position tile to a target position
        """
        move_str = ''
        
        # actually we only need to move to the tile above the target tile                         
        move_str += self.move_zero(current_row, current_col)
        # check for the last move, if it is up, then it is the same as last time
        # if is is 'l', then we do 'ur'
        # if it is 'r', then we do 'ul'
        if (move_str[-1] == 'u'):
            current_row  += 1
        elif (move_str[-1] == 'l'):
            move_str += 'ur'
            current_col += 1
        elif (move_str[-1] == 'r'):
            move_str += 'ul'
            current_col -= 1
            
        # move the target tile to the correct col
        while (current_col != target_col):
            if ((current_col - target_col) < 0):
                move_str += 'rdlur'
                current_col += 1
            else:
                move_str += 'ldrul'
                current_col -= 1
        
        # move the target tile to the correct row
        while (current_row != target_row):
            move_str += 'lddru'
            # remember that we plan a move here, not actually move anything
            current_row += 1
        # conclude the move
        move_str += 'ld'    
        return move_str
    
    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # check if the tile at (target_row, target_col) is 0
        if (self._grid[target_row][target_col] != 0):
            return False
        
        # check the current row
        for col in range(target_col + 1, self._width):
            if (self._grid[target_row][col] != self.desired_tile(target_row, col)):
                return False
            
        # check the rows below
        for row in range(target_row + 1, self._height):
            for col in range(self._width):
                if (self._grid[row][col] != self.desired_tile(row, col)):
                    return False
        
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # assume that the lower_row_invariant holds in
        # the beginning
        
        # detect the position of the target tile
        current_row, current_col = self.current_position(target_row, target_col)                
        move_str = self.position_tile(current_row, current_col, target_row, target_col) 
        self.update_puzzle(move_str)
        return move_str

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        move_str = ''
        self.update_puzzle('ur')        
        current_row, current_col = self.current_position(target_row, 0) 
        if (current_row == target_row) and (current_col == 0):
             pass
        else:
            # reposition the target tile to position (i - 1, 1)
            move_str += self.position_tile(current_row, current_col, target_row - 1, 1)
            # add the 3x2 solve string
            move_str += 'ruldrdlurdluurddlur'
        # move the zero tile to the next position
        num_steps = self._width - 1 - 1
        move_str += num_steps * 'r'
        self.update_puzzle(move_str)
        # add 'ur' to the beginning of the move_str
        move_str = 'ur' + move_str
        return move_str

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if (self._grid[0][target_col] != 0):
            return False
        # check second row
        for col in range(target_col, self._width):
            if (self._grid[1][col] != self.desired_tile(1, col)):
                return False
        # check the current row
        for col in range(target_col + 1, self._width):
            if (self._grid[0][col] != self.desired_tile(0, col)):
                return False
        # check the rows below
        for row in range(2, self._height):
            for col in range(self._width):
                if (self._grid[row][col] != self.desired_tile(row, col)):
                    return False    
        
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if (self._grid[1][target_col] != 0):
            return False
        
        # check the current row
        for col in range(target_col + 1, self._width):
            if (self._grid[1][col] != self.desired_tile(1, col)):
                return False
            
        # check the rows below
        for row in range(2, self._height):
            for col in range(self._width):
                if (self._grid[row][col] != self.desired_tile(row, col)):
                    return False
                
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        move_str = ''
        self.update_puzzle('ld')        
        current_row, current_col = self.current_position(0, target_col) 
        if (current_row == 0) and (current_col == target_col):
             pass
        else:
            # reposition the target tile to position (i - 1, 1)
            move_str += self.position_tile(current_row, current_col, 1, target_col - 1)
            # add the 2x3 solve string
            move_str += 'urdlurrdluldrruld'
        # update the puzzle
        self.update_puzzle(move_str)
        # add 'ld' to the beginning of the move_str
        move_str = 'ld' + move_str
        return move_str

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        current_row, current_col = self.current_position(1, target_col)                
        move_str = self.position_tile(current_row, current_col, 1, target_col)
        # because in the first two rows, we solve each column first
        # after solving the tile, we place the zero tile on row0 and on the same col
        move_str += 'ur'
        self.update_puzzle(move_str)
        return move_str

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        move_str = ''
        # first, move 'ul'
        move_str += 'ul'
        self.update_puzzle('ul')
        while (not self.row0_invariant(0)):
            move_str += 'drul'
            self.update_puzzle('drul')  
            
        return move_str

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_str = ''
        # move the zero tile to the lower right of the grid
        move_str += self.move_zero(self._height - 1, self._width - 1)
        self.update_puzzle(self.move_zero(self._height - 1, self._width - 1))
        # solve all the tiles in the lower rows
        for row in range(self._height - 1, 1, -1):
            for col in range(self._width - 1, -1, -1):
                if (col == 0):
                    move_str += self.solve_col0_tile(row)
                else:
                    move_str += self.solve_interior_tile(row, col)
        # solve the right most columns in the first two rows        
        for col in range(self._width - 1, 1, -1):
            move_str += self.solve_row1_tile(col)
            move_str += self.solve_row0_tile(col)
        # solve the last 2x2 grid    
        move_str += self.solve_2x2()
        return move_str

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

# test desired_tile
#test = Puzzle(3, 4)
#print test.desired_tile(2,2)
#print test.desired_tile(1,1)
#print test.desired_tile(1,2)

# test lower_row_invariant
#initial_grid = [[3, 0, 2], [4, 1, 5], [6, 7, 8]]
#test = Puzzle(3, 3, initial_grid)
#print test.lower_row_invariant(1 ,1)

#q8_grid = [[4, 13, 1, 3], [5, 10, 2, 7], [8, 12, 6, 11], [9, 0, 14, 15]]
#test = Puzzle(4, 4, q8_grid)
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, q8_grid))
#print test.solve_interior_tile(3, 1)
#print test.move_zero(1, 2)

## TEST solve_interior_grid
#solve_interior_grid = [[13, 5, 6, 14], [15, 9, 7, 2], [11, 4, 3, 1], [8, 12, 10, 0]]
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, solve_interior_grid))
#test = Puzzle(4, 4, solve_interior_grid)
#print test.solve_interior_tile(3,3)
#print test.solve_interior_tile(3,2)
#print test.solve_interior_tile(3,1)
#print test

#solve_interior_grid2 = [[1, 2, 3, 7], [4, 13, 5, 6], [12, 11, 8, 10], [15, 14, 9, 0]]
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, solve_interior_grid2))
#test = Puzzle(4, 4, solve_interior_grid2)
#print test.solve_interior_tile(3,3)
#print test.solve_interior_tile(3,2)

## TEST solve_col0_grid
#solve_col0_grid = [[4, 10, 5, 2], [9, 11, 7, 6], [1, 8, 12, 3], [0, 13, 14, 15]]
#solve_col0_grid2 = [[4, 5, 6, 12], [9, 10, 11, 2], [1, 8, 7, 3], [0, 13, 14, 15]]
#solve_col0_grid3 = [[10, 8, 5, 2], [12, 4, 3, 7], [1, 11, 9, 6], [0, 13, 14, 15]]
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, solve_col0_grid3))
#test = Puzzle(4, 4, solve_col0_grid3)
#print test.solve_col0_tile(3)
#print test

#solve_col0_grid4 = [[3, 2, 1], [6, 5, 4], [0, 7, 8]]
#poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, solve_col0_grid4))
#test = Puzzle(3, 3, solve_col0_grid4)
#print test.solve_col0_tile(2)
#print test

#solve_col0_grid5 = [[8, 2, 10, 9, 1], [7, 6, 5, 4, 3], [0, 11, 12, 13, 14], [15, 16, 17, 18, 19]]
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 5, solve_col0_grid5))
#test = Puzzle(4, 5, solve_col0_grid5)
#print test.solve_col0_tile(2)
#print test

## TEST row0_invariant
#test = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
#print test.row0_invariant(0)

## TEST solve_row1_tile
#solve_row1_grid = [[4, 7, 3, 5], [6, 2, 1, 0], [8, 9, 10, 11], [12, 13, 14, 15]]
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4), solve_row1_grid)
#test = Puzzle(4, 4, solve_row1_grid)
#print test.solve_row1_tile(3)

## TEST solve_row0_tile
#solve_row1_grid = [[5, 4, 2, 0], [1, 3, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, solve_row1_grid))
#test = Puzzle(4, 4, solve_row1_grid)
#print test.solve_row0_tile(3)
#print test

## TEST solve_row1_tile
#solve_row1_grid = [[2, 5, 4], [1, 3, 0], [6, 7, 8]]
#poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, solve_row1_grid))
#test = Puzzle(3, 3, solve_row1_grid)
#print test.solve_row1_tile(2)

## TEST solve_2x2 
#solve_2x2_grid = [[3, 1, 2], [4, 0, 5], [6, 7, 8]]
#poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, solve_2x2_grid))
#test = Puzzle(3, 3, solve_2x2_grid)
#print test.solve_2x2()                           

## TEST solve_puzzle
#solve_puzzle_grid = [[5, 2, 6, 4, 9], [10, 1, 24, 3, 0], [11, 12, 8, 7, 22],
#                     [15, 20, 18, 16, 14], [21, 17, 23, 19, 13]]
#poc_fifteen_gui.FifteenGUI(Puzzle(5, 5, solve_puzzle_grid))
#poc_fifteen_gui.FifteenGUI(Puzzle(3, 3))
#test = Puzzle(5, 5, solve_puzzle_grid)
#print test.solve_puzzle()
#print test

                           

