"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

#import poc_fifteen_gui
from user37_zTJC9SJzQM_0 import PimpedGUI

# see code at:
# http://www.codeskulptor.org/#user37_zTJC9SJzQM_0.py

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

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
    
        tile_0_ok = self._grid[target_row][target_col] == 0
        
        row_end_ok = self.solved((target_row, target_row + 1), (target_col + 1, self._width))
                
        last_rows_ok = self.solved((target_row + 1, self._height), (0, self._width))
        
        return tile_0_ok and row_end_ok and last_rows_ok
    
    
    def solved(self, row_range, col_range):
        """
        Helper fn that takes takes tuples of the form
        (start, stop) for row_range and col_range.
        Returns a boolean if puzzle is solved in that range
        """
        solved = True
        row_start, row_stop = row_range
        col_start, col_stop = col_range
        for row in range(row_start, row_stop):
            for col in range(col_start, col_stop):
                posn_of_desired_tile = self.current_position(row, col)
                cell_ok = (row, col) == posn_of_desired_tile
                if cell_ok == False:
                    solved = False
        return solved
    

    def _same_col_alg(self, target_row, target_col, alt_row, alt_col):
        """
        Helper fn for position_tile
        Called when 0-tile is directly above target tile, in same column as target position
        Updates puzzle and returns a move string
        Updated puzzle will have target tile in target position with 0-tile above it
        """
        move_string = ""
        (cur_row, cur_col) = self.current_position(alt_row, alt_col)
        tile_done = (target_row, target_col) == (cur_row, cur_col)
        while not tile_done:
            self.update_puzzle("lddru")
            move_string = "".join((move_string, "lddru"))
            (cur_row, cur_col) = self.current_position(alt_row, alt_col)
            tile_done = (target_row, target_col) == (cur_row, cur_col)
        return move_string
    
        
    def _bring_right(self, target_row, target_col, alt_row, alt_col):
        """
        Helper fn for position_tile
        Called when 0-tile is in same row and to the right of target tile
        Updates puzzle and returns a move string
        Updated puzzle can be of 2 forms:
        1: target tile's row < target_row
            results in updated positions ready for same_col_alg to move down
        2: target tile's row == target_row
            results in target tile in final position and 0-tile to its left
            --> could do "ur" for 2nd case to make same as 1st case,
                but results in 4 unnecessary moves (same_col_alg does "ld" again)
        """
        move_string = ""
        (cur_row, cur_col) = self.current_position(alt_row, alt_col)
        zero_col = self.current_position(0, 0)[1]
        tile_done = (target_row, target_col) == (cur_row, cur_col)
        
        # move 0-tile left to the target tile's column --> (result is 0-T)
        while cur_col < zero_col:
            self.update_puzzle("l")
            move_string = "".join((move_string, "l"))
            (cur_row, cur_col) = self.current_position(alt_row, alt_col)
            zero_col = self.current_position(0, 0)[1]
            tile_done = (target_row, target_col) == (cur_row, cur_col)

        # corner case where target tile started in left side of target row:
        # NOTE: can delete this, but adds 4 unnecessary moves
        if cur_row == target_row:
            while not tile_done:
                self.update_puzzle("urrdl")
                move_string = "".join((move_string, "urrdl"))
                (cur_row, cur_col) = self.current_position(alt_row, alt_col)
                tile_done = (target_row, target_col) == (cur_row, cur_col)
        
        # move target tile to target_col
        if cur_row < target_row:
            if cur_row == 0:
                # move down to row 1
                self.update_puzzle("druld")
                move_string = "".join((move_string, "druld"))
            while cur_col < target_col:
                self.update_puzzle("urrdl")
                move_string = "".join((move_string, "urrdl"))
                (cur_row, cur_col) = self.current_position(alt_row, alt_col)
            # re-position 0-tile above target tile
            self.update_puzzle("ur")
            move_string = "".join((move_string, "ur"))
            
        return move_string
    
    
    def _bring_left(self, target_row, target_col, alt_row, alt_col):
        """
        Helper fn for position tile
        Called when 0-tile is in same row and to the left of target tile
        Updates puzzle and returns a move string
        Updated puzzle will have 0- and target-tile positions ready for same_col_alg
        """
        move_string = ""
        (cur_row, cur_col) = self.current_position(alt_row, alt_col)
        zero_col = self.current_position(0, 0)[1]
        
        # move 0-tile right to the target tile's column --> (result is T-0)
        while cur_col > zero_col:
            self.update_puzzle("r")
            move_string = "".join((move_string, "r"))
            (cur_row, cur_col) = self.current_position(alt_row, alt_col)
            zero_col = self.current_position(0, 0)[1]
            
        # move target tile to target_col
        if cur_row == 0:
            # move down to row 1
            self.update_puzzle("dlurd")
            move_string = "".join((move_string, "dlurd"))
        while cur_col > target_col:
            self.update_puzzle("ulldr")
            move_string = "".join((move_string, "ulldr"))
            (cur_row, cur_col) = self.current_position(alt_row, alt_col)
        # re-position 0-tile above target tile
        self.update_puzzle("ul")
        move_string = "".join((move_string, "ul"))
        
        return move_string
    
    
    def position_tile(self, target_row, target_col, alt_row, alt_col):
        """
        Helper fn for 4 other solve methods
        Place the tile that will be at alt_row, alt_col when puzzle is finished
        at target_row, target_col
        and 0-tile to its left
        Note:   target posn == alt posn for solve_interior_tile and solve_row1_tile
                target posn != alt posn for solve_col0_tile and solve_row0_tile
        Updates puzzle and returns a move string
        """
        move_string = ""
        
        # get current position of target tile and 0-tile
        (cur_row, cur_col) = self.current_position(alt_row, alt_col)
        zero_row, zero_col = self.current_position(0, 0)
        
        # move 0 tile up to same row as target tile
        while cur_row < zero_row: # and not tile_done:
            self.update_puzzle("u")
            move_string = "".join((move_string, "u"))
            (cur_row, cur_col) = self.current_position(alt_row, alt_col)
            zero_row, zero_col = self.current_position(0, 0)
        
        # move target tile to target column
        if cur_col < zero_col:
            right_moves = self._bring_right(target_row, target_col, alt_row, alt_col)
            move_string = "".join((move_string, right_moves))     
        if cur_col > zero_col:   # and not tile_done:
            left_moves = self._bring_left(target_row, target_col, alt_row, alt_col)
            move_string = "".join((move_string, left_moves))
        
        # re-check posn's, & if target tile has been moved to target position
        (cur_row, cur_col) = self.current_position(alt_row, alt_col)
        zero_row, zero_col = self.current_position(0, 0)
        tile_done = (target_row, target_col) == (cur_row, cur_col)
        
        # move target tile down to target
        if cur_col == zero_col: # and zero_row == cur_row + 1:
            if not tile_done:   # check to avoid unnecessary fn call
                down_moves = self._same_col_alg(target_row, target_col, alt_row, alt_col)
                move_string = "".join((move_string, down_moves))
            # reposition 0-tile left of target tile
            self.update_puzzle("ld")
            move_string = "".join((move_string, "ld"))
            
        return move_string
    
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        and 0-tile to its left
        Updates puzzle and returns a move string
        Note: target_row > 1 and target_col > 0
        """
        assert self.lower_row_invariant(target_row, target_col)
        move_string = self.position_tile(target_row, target_col, target_row, target_col)
        return move_string

    
    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0)
        move_string = ""
        self.update_puzzle("ur")
        move_string = "".join((move_string, "ur"))
        
        # check if (target_row, 0) has just been solved
        (cur_row, cur_col) = self.current_position(target_row, 0)
        tile_done = (cur_row, cur_col) == (target_row, 0)
        
        if not tile_done:
            next_moves = self.position_tile(target_row - 1, 1, target_row, 0)
            move_string = "".join((move_string, next_moves))
            col0_magic = "ruldrdlurdluurddlur"
            self.update_puzzle(col0_magic)
            move_string = "".join((move_string, col0_magic))
            
        # move 0-tile to the right end of next row
        zero_col = self.current_position(0, 0)[1]
        while zero_col < self._width - 1:
            self.update_puzzle("r")
            move_string = "".join((move_string, "r"))
            zero_col = self.current_position(0, 0)[1]
        
        return move_string


    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """

        tile_0_ok = self._grid[0][target_col] == 0
    
        last_rows_ok = True
        # check if there are any last rows, or if it is a 2x2 puzzle:
        if self._height > 2:
            last_rows_ok = self.solved((2, self._height), (0, self._width))
        
        right_cols_ok = True
        # check if there are any cols to the right:
        if target_col < self._width - 1:
            right_cols_ok = self.solved((0, 2), (target_col + 1, self._width))
                    
        # check whether position (1, target_col) is also solved
        below_tile_0_ok = self.solved((1, 2), (target_col, target_col + 1))
        
        return tile_0_ok and last_rows_ok and right_cols_ok and below_tile_0_ok
    
    
    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
            
        # this will also check the 0-tile:
        lower_rows_ok = self.lower_row_invariant(1, target_col)
        
        right_cols_ok = True
        # check if there are any cols to the right:
        if target_col < self._width - 1:
            right_cols_ok = self.solved((0, 1), (target_col + 1, self._width))
                    
        return lower_rows_ok and right_cols_ok

    
    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        move_string = ""
        self.update_puzzle("ld")
        move_string = "".join((move_string, "ld"))
        
        # check if (0, target_col) has just been solved
        (cur_row, cur_col) = self.current_position(0, target_col)
        tile_done = (cur_row, cur_col) == (0, target_col)
        
        if not tile_done:
            next_moves = self.position_tile(1, target_col - 1, 0, target_col)
            move_string = "".join((move_string, next_moves))
            row0_magic = "urdlurrdluldrruld"
            self.update_puzzle(row0_magic)
            move_string = "".join((move_string, row0_magic))
            
        return move_string
    

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        move_string = self.position_tile(1, target_col, 1, target_col)
        self.update_puzzle("ur")
        move_string = "".join((move_string, "ur"))
        return move_string
    

    ###########################################################
    # Phase 3 methods
         
    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1)
        move_string = ""
        self.update_puzzle("lu")
        move_string = "".join((move_string, "lu"))
        
        while not self.solved((0, 2), (0, 2)):
            self.update_puzzle("rdlu")
            move_string = "".join((move_string, "rdlu"))
            
        return move_string
        

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        
        # find 0-tile and move it to end of grid
        zero_row, zero_col = self.current_position(0, 0)
        while zero_row < self._height - 1:
            self.update_puzzle("d")
            move_string = "".join((move_string, "d"))
            zero_row = self.current_position(0, 0)[0]
        while zero_col < self._width - 1:
            self.update_puzzle("r")
            move_string = "".join((move_string, "r"))
            zero_col = self.current_position(0, 0)[1]
            
        # initialize target position
        target_row, target_col = self.current_position(0, 0)
            
        # solve bottom rows:
        while target_row > 1:
            while target_col > 0:
                next_string = self.solve_interior_tile(target_row, target_col)
                move_string = "".join((move_string, next_string))
                target_col = self.current_position(0, 0)[1]
            next_string = self.solve_col0_tile(target_row)
            move_string = "".join((move_string, next_string))
            target_row, target_col = self.current_position(0, 0)
            
        # solve top 2 rows except for leftmost 2x2 square:
        while target_col > 1:
            if target_row == 1:
                next_string = self.solve_row1_tile(target_col)
                move_string = "".join((move_string, next_string))
                target_row, target_col = self.current_position(0, 0)
            if target_row == 0:
                next_string = self.solve_row0_tile(target_col)
                move_string = "".join((move_string, next_string))
                target_row, target_col = self.current_position(0, 0)
        
        # solve 2x2:
        next_string = self.solve_2x2()
        move_string = "".join((move_string, next_string))
        
        return move_string

    
# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, [[5, 4, 1, 3], [8, 0, 2, 7], [10, 13, 6, 11], [9, 12, 14, 15]]))
#poc_fifteen_gui.FifteenGUI(Puzzle(2, 2, [[0, 1], [3, 2]]))
PimpedGUI(Puzzle(4, 4))

