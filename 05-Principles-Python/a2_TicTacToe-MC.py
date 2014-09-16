"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 8    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
    
# Add your functions here.

def mk_grid(width, height):
    """
    Helper fn: initializes grid with 0's
    """
    arr = [ [0 for dummy_col in range(width)]\
               for dummy_row in range(height)]
    return arr

def mc_trial(board, player):
    """
    Takes a current board & next player to move.
    Plays a game starting with the given player
    by making random moves, alternating between players.
    Returns when the game is over.
    """
    while board.check_win() == None:
        empty_squares = board.get_empty_squares()
        next_move = random.choice(empty_squares)
        board.move(next_move[0], next_move[1], player)
        player = provided.switch_player(player)
    else:
        return

def mc_update_scores(scores, board, player):
    """
    Takes scores grid (a list of lists) w/ same dim as TTT board,
    a board from a completed game,
    and which player the machine player is.
    Scores the completed board and updates the scores grid.
    """
    if (board.check_win() == provided.DRAW) or (board.check_win() == None):
        return
    dim = board.get_dim()        
    for row in range(dim):
        for col in range(dim):
            scores[row][col] += calc_score(board, player, row, col)
            
def calc_score(board, player, row, col):
    """
    Helper function that takes a completed board where there is a winner,
    which player the machine player is,
    and a row and col of the board,
    Determines the score for the square at that row and col.
    """
    winner = board.check_win()
    square = board.square(row, col)
    if square == provided.EMPTY:
        return 0
    elif square == winner:
        if winner == player:
            return MCMATCH
        else:
            return MCOTHER
    else:
        if winner == player:
            return -MCOTHER
        else:
            return -MCMATCH
    
def get_best_move(board, scores):
    """
    Takes a current board and a grid of scores.
    Finds all of the empty squares with the maximum score
    and randomly return one of them as a (row, column) tuple.
    """
    empty_squares = board.get_empty_squares()  # [(r, c), ...]
    max_scores = []
    for pos in empty_squares:
        value = scores[pos[0]][pos[1]]
        if (len(max_scores) == 0):
            max_scores.append((pos[0], pos[1], value))
        elif (value == max_scores[0][2]):
            max_scores.append((pos[0], pos[1], value))
        elif value > max_scores[0][2]:
            max_scores = [(pos[0], pos[1], value)] 
    move = random.choice(max_scores)
    return (move[0], move[1])

def mc_move(board, player, trials):
    """
    Takes a current board, which player the machine player is,
    and the number of trials to run.
    Uses Monte Carlo simulation to return a move for the machine player
    in the form of a (row, column) tuple.
    """
    dim = board.get_dim()
    scores = mk_grid(dim, dim)
    for dummy_num in range(NTRIALS):
        board_clone = board.clone()
        mc_trial(board_clone, player)
        mc_update_scores(scores, board_clone, player)
    return get_best_move(board, scores)
    

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

