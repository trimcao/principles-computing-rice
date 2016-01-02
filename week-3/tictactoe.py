
"""
Monte Carlo Tic-Tac-Toe Player
by Tri Minh Cao
trimcao@gmail.com
September, 2015
"""

import random
#import poc_ttt_gui
#import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
PLAYX = 'X'
PLAYO = 'O'
WIDTH = 3
RANGE = 3


# Directions, DO NOT MODIFY
VERTICAL = 1
HORIZONTAL = 2
DIAG_DOWN = 3
DIAG_UP = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.

GEN_INIT = {VERTICAL: (-1, 0),
           HORIZONTAL: (0, -1),
           DIAG_DOWN: (-1, -1),
           DIAG_UP: (1, -1)}

OFFSETS = {VERTICAL: (1, 0),
           HORIZONTAL: (0, 1),
           DIAG_DOWN: (1, 1),
           DIAG_UP: (-1, 1)}
# Add your functions here.
def in_board(row, col):
    if (row >= 0 and row < WIDTH and col >=0 and col < WIDTH):
        return True
    else:
        return False

def gen_initial(board, row_start, col_start, direction):
    steps = RANGE
    offset = GEN_INIT[direction]
    # the offset we need is the opposite of values in OFFSETS
    
    initials = []
    for step in range(steps):
        row = row_start + offset[0] * step
        col = col_start + offset[1] * step
        if (in_board(row, col)):
            initials.append((row,col))
    return initials

def traverse(board, initial,  direction):
    steps = RANGE
    offset = OFFSETS[direction]
    for idx in range(len(initial)):
        row_start = initial[idx][0]
        col_start = initial[idx][1]
        temp_list = []
        for step in range(steps):
            row = row_start + step * offset[0]
            col = col_start + step * offset[1]
            if (in_board(row, col)):
                temp_list.append(board[row][col])
            else:
                break
        # check for winning sequence of 'X' or 'O'
        if (temp_list.count('O') == RANGE or temp_list.count('X') == RANGE):
            return True
    else:
        return False

def change_player(player):
    if player == PLAYX:
        return PLAYO
    else:
        return PLAYX

def mc_trial(board, player):
    current_player = player
    game_over = False
    while (not game_over):
        row = random.randrange(0, WIDTH)
        col = random.randrage(0, WIDTH)
        #while (board[row][col] == 'X' or board[row][col] == 'O')

"""
# test gen_initial
test_board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
initial_up = gen_initial(test_board, 0, 2, VERTICAL)
print initial_up
print gen_initial(test_board, 0, 2, HORIZONTAL)

print gen_initial(test_board, 0, 2, DIAG_DOWN)
print gen_initial(test_board, 0, 2, DIAG_UP)
"""

""" Test traverse
"""
test_board = [['X', 'X', 'X'], [0, 0, 0], [0, 0, 0]]

test_board1 = [[0, 'O', 0], [0, 'O', 0], [0, 'O', 0]]
test_board2 = [['X', 0, 0], [0, 'X', 0], [0, 0, 'X']]
test_board3 = [[0, 0, 'O'], [0, 'O', 0], ['O', 0, 0]]
initial_dd = gen_initial(test_board3, 0, 2, DIAG_UP)
result = traverse(test_board3, initial_dd, DIAG_UP)
print result


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.
blank_board = [[0 for col in range(WIDTH)] for row in range(WIDTH)]
#print blank_board
# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

