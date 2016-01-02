"""
Mini-max Tic-Tac-Toe Player
Name: Tri Minh Cao
Email: trimcao@gmail.com

Note: This program only runs with provided methods from CodeSkulptor
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}


def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    # base case:
    winner = board.check_win()
    if (winner != None):
        return (SCORES[winner], (-1, -1))
    # recursive case
    else:
        possible_moves = board.get_empty_squares()
        # score_list is a list of tuple containing score and move
        score_list = []
        next_player = provided.switch_player(player)
        for idx in range(len(possible_moves)):
            next_move = possible_moves[idx]
            new_board = board.clone()
            # current player make the move
            new_board.move(next_move[0], next_move[1], player)
            result = mm_move(new_board, next_player)
            # multiply the score by SCORES[player] to always maximize the score
            # even with PLAYERO
            score = SCORES[player] * result[0]
            score_list.append((score, next_move))
            # if the score is 1, aka maximum score, we stop searching
            if (score == 1):
                break
        
        # return the ideal move
        ideal_result = max(score_list)
        # multiply the score by SCORES[player] to get the correct score for 
        # PLAYERO
        ideal_result = (SCORES[player] * ideal_result[0], ideal_result[1])
        return ideal_result
                 
        

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

# test switch_player method
#print provided.switch_player(provided.PLAYERO)
#print provided.PLAYERX

# create a test board
#board = provided.TTTBoard(3)
#board.move(0, 0, provided.PLAYERO)
#board.move(1, 0, provided.PLAYERO)
#board.move(2, 1, provided.PLAYERO)
#board.move(0, 1, provided.PLAYERX)
#board.move(1, 1, provided.PLAYERX)
#board.move(2, 2, provided.PLAYERX)
#board.move(0, 2, provided.PLAYERX)

#print board

#print mm_move(board, provided.PLAYERX)
#board2 = provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]])
#print board2
#print mm_move(board2, provided.PLAYERO)
