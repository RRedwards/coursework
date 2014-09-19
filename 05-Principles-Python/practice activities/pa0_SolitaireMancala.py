"""
Solitaire Mancala Shark
"""


class SolitaireMancala:
    """
    Class to run the game logic.
    """

    def __init__(self):
        self.board = [0]

        
    def __str__(self):
        temp = list(self.board)
        temp.reverse()
        return str(temp)

    
    def set_board(self, config):
        self.board = list(config)
    
    
    def get_num_seeds(self, house_num):
        return self.board[house_num]

    
    def is_legal_move(self, house_num):
        return (house_num != 0) and (self.board[house_num] == house_num)

        
    def apply_move(self, house_num):
        if self.is_legal_move(house_num):
            self.board[house_num] = 0
            for house in range(0, house_num):
                self.board[house] += 1
        
        
    def choose_move(self):
        legal_moves = 0
        for index in range(0, len(self.board)):
            if self.is_legal_move(index):
                legal_moves = index
                break
        return legal_moves

    
    def is_game_won(self):
        just_houses = list(self.board[1:])		
        return len(filter(lambda x: x != 0, just_houses)) == 0
      
        
    def plan_moves(self):
        moves_list = []
        board_clone = SolitaireMancala()
        board_clone.set_board(list(self.board))
        next_move = board_clone.choose_move()

        while next_move != 0:
            moves_list.append(next_move)
            board_clone.apply_move(next_move)
            next_move = board_clone.choose_move()
        else:
            return moves_list    
        
        
        
#import poc_mancala_testsuite
#poc_mancala_testsuite.run_test(SolitaireMancala)

import poc_mancala_gui
poc_mancala_gui.run_gui(SolitaireMancala())

