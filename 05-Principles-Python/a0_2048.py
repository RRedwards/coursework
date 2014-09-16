"""
Clone of 2048 game.
"""

import poc_2048_gui  
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
    Helper function that merges a single row or column in 2048
    """
    result = []
    placeholder = 0
    last_tile_merged = False

    for item in line:
        result.append(0)
        # merging logic
        if placeholder > 0\
        and item == result[placeholder - 1]\
        and item > 0\
        and last_tile_merged == False:
            result[placeholder - 1] += item
            last_tile_merged = True
        # sliding logic
        elif item > 0:
            result[placeholder] = item
            placeholder += 1
            last_tile_merged = False
    return result


def mk_grid(width, height):
    """
    Initializes grid with 0's
    """
    arr = [ [0 for dummy_col in range(width)]\
               for dummy_row in range(height)]
    return arr


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):

        self.grid_height = grid_height
        self.grid_width = grid_width
        
        self.cells = []
        self.reset()
        
        top_row = [(0, yyy) for yyy in range(grid_width)]
        bottom_row = [(grid_height - 1, yyy) for yyy in range(grid_width)]
        left_col = [(xxx, 0) for xxx in range(grid_height)]
        right_col = [(xxx, grid_width - 1) for xxx in range(grid_height)]

        def build_line(start_pos, direction, length):
            """
            builds coordinate list of row or col line from start_pos
            """
            line = [start_pos]
            for item in range(1, length):
                line.append((line[item - 1][0] + OFFSETS[direction][0],\
                line[item - 1][1] + OFFSETS[direction][1]))
            return line

        up_cols =    [build_line(item, UP, grid_height) for item in top_row]
        down_cols =  [build_line(item, DOWN, grid_height) for item in bottom_row]
        left_rows =  [build_line(item, LEFT, grid_width) for item in left_col]
        right_rows = [build_line(item, RIGHT, grid_width) for item in right_col]
        
        self.lines = { UP: up_cols,\
                 DOWN: down_cols,\
                 LEFT: left_rows,\
                 RIGHT: right_rows}
        
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.cells = mk_grid(self.grid_width, self.grid_height)
        
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        temp = []
        for item in self.cells:
            temp.append(str(item))    
        return '\n'.join(temp)
    
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height
    
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width

    
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        lines_to_move = self.lines[direction]
        line_values = [[self.get_tile(jjj[0], jjj[1]) for jjj in iii] for iii in lines_to_move]
        
        merged_values = [merge(line) for line in line_values]

        zip_list = [zip(iii[0], iii[1]) for iii in zip(lines_to_move, merged_values)]
            
        new_grid = mk_grid(self.grid_width, self.grid_height)
        for iii in zip_list:
            for jjj in iii:
                row = jjj[0][0]
                col = jjj[0][1]
                new_grid[row][col] = jjj[1]
        
        if self.cells != new_grid:
            self.cells = new_grid
            self.new_tile()
        
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        if random.randrange(0, 10) > 8:
            rand_value = 4
        else:
            rand_value = 2
        new_pos = self.cell_picker()
        self.set_tile(new_pos[0], new_pos[1], rand_value)
        
        
    def cell_picker(self):
        """
        Helper function that shuffles empty_cells list and returns first item
        """
        shuffled_list = self.empty_cells()
        random.shuffle(shuffled_list)
        return shuffled_list[0]
    
    
    def empty_cells(self):
        """
        Helper function to return list of empty cells
        """
        zeroes = []
        for iii in range(self.grid_height):
            for jjj in range(self.grid_width):
                if self.cells[iii][jjj] == 0:
                    zeroes.append([iii, jjj])
        return zeroes
        
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self.cells[row][col] = value

        
    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        return self.cells[row][col]
    
    
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

