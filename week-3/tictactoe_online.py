
"""
Monte Carlo Tic-Tac-Toe Player

Tri Minh Cao
trimcao@gmail.com
September 2015
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1        # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
SIZE = 3

# Add your functions here.

def change_player(player):
    if player == PLAYERX:
        return PLAYERO
    else:
        return PLAYERX
    
def mc_trial(board, player):
    """
    run a full game 
    outcome can be either player wins or a draw
    """
    current_player = player
    while (board.check_win() == None):
        # continue play
        # choose an empty square in the board
        empty_sq = board.get_empty_squares()
        loc = random.choice(empty_sq)
        board.move(loc[0], loc[1], current_player)
        # change player
        current_player = provided.switch_player(current_player)
   

def mc_update_scores(scores, board, player):
    """
    Process a result board from a monte carlo trial.
    Update the scores to let the computer learns 
    the best next move.
    """
    winner = board.check_win()
    if (winner == provided.DRAW):
        pass
    elif (winner == player):
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                value = board.square(row, col)
                if (value == player):
                    scores[row][col] += SCORE_CURRENT
                elif (value == provided.EMPTY):
                    pass
                else:
                    scores[row][col] -= SCORE_OTHER
    else:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                value = board.square(row, col)
                if (value == player):
                    scores[row][col] -= SCORE_CURRENT
                elif (value == provided.EMPTY):
                    pass
                else:
                    scores[row][col] += SCORE_OTHER 


def get_best_move(board, scores):
    """
    get the best move by using a number of monte carlo
    trials
    """
    # get a list of empty squares
    empty_sq = board.get_empty_squares()
    
    # arbirtrarily chooses a max_score
    max_score = scores[empty_sq[0][0]][empty_sq[0][1]]
    #print max_score
    # add all maximum score locations to max_list
    max_list = []
    for idx in range(len(empty_sq)):
        row = empty_sq[idx][0]
        col = empty_sq[idx][1]
        if (max_score == scores[row][col]):
            max_list.append((row, col))
        elif (scores[row][col] > max_score):
            max_score = scores[row][col]
            max_list = []
            max_list.append((row, col))
        else:
            pass

    # randomly choose a location
    return random.choice(max_list)

def mc_move(board, player, trials):
    """
    Make a move for the computer by using the Monte Carlo method
    """
    width = board.get_dim()
    scores = [[0 for col in range(width)] for row in range(width)]
    
    for idx in range(trials):
        board_trial = board.clone()
        mc_trial(board_trial, player)
        mc_update_scores(scores, board_trial, player)
            
    return get_best_move(board, scores)
                  
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

"""
# Test the mc_update-scores method
test_board = provided.TTTBoard(SIZE)
mc_trial(test_board, provided.PLAYERX)
scores = [[0 for col in range(3)] for row in range(3)]
print scores
mc_update_scores(scores, test_board, provided.PLAYERX)
print scores

test_board = provided.TTTBoard(SIZE)
mc_trial(test_board, provided.PLAYERX)
mc_update_scores(scores, test_board, provided.PLAYERX)
print scores

test_board = provided.TTTBoard(SIZE)
mc_trial(test_board, provided.PLAYERX)
mc_update_scores(scores, test_board, provided.PLAYERX)
print scores

test_board = provided.TTTBoard(SIZE)

loc = get_best_move(test_board, scores)
print loc
"""

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(5, provided.PLAYERX, mc_move, NTRIALS, False)

