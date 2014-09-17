"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)


SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

# NEGAMAX VERSION:
def mm_move(board, player):
    """
    Make a move on the board.
    (player is which player should move next)
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    winner = board.check_win()
    if winner != None:
        return SCORES[winner], (-1, -1)
    else:
        empty_squares = board.get_empty_squares()
        cur_max = None
        cur_best_move = None
        for square in empty_squares:
            board_clone = board.clone()
            board_clone.move(square[0], square[1], player)
            next_player = provided.switch_player(player)
            next_result = mm_move(board_clone, next_player)
            if next_result[0] == SCORES[player]:
                return next_result[0], square
            elif (cur_max == None)\
            or (next_result[0] * SCORES[player] > cur_max * SCORES[player]):
                cur_max = next_result[0]
                cur_best_move = square
        return cur_max, cur_best_move
                
    
# 2 CASES VERSION (if X, if O...):    
#    winner = board.check_win()
#    if winner != None:
#        return SCORES[winner], (-1, -1)
#    else:
#        empty_squares = board.get_empty_squares()          
#        if player == provided.PLAYERX:
#            cur_best_score = -1
#        if player == provided.PLAYERO:
#            cur_best_score = 1
#        cur_best_move = empty_squares[0]
#        for square in empty_squares:
#            board_clone = board.clone()
#            board_clone.move(square[0], square[1], player)
#            next_player = provided.switch_player(player)
#            next_result = mm_move(board_clone, next_player)
#            
#            if player == provided.PLAYERX:
#                if next_result[0] == 1:
#                    return next_result[0], square
#                elif next_result[0] >= cur_best_score:
#                    cur_best_score = next_result[0]
#                    cur_best_move = square
#                    
#            if player == provided.PLAYERO:
#                if next_result[0] == -1:
#                    return next_result[0], square
#                elif next_result[0] <= cur_best_score:
#                    cur_best_score = next_result[0]
#                    cur_best_move = square
#        return cur_best_score, cur_best_move
    

    
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
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)


