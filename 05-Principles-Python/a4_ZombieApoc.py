"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
#import poc_zombie_gui
import user35_yAju7CXSXh2dU3K as poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    
    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._human_list = []
        self._zombie_list = []
        
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
               
            
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)
          
        
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        return (cell for cell in self._zombie_list)

    
    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        return (cell for cell in self._human_list)
        
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        height = self.get_grid_height()
        width =  self.get_grid_width()
        visited = poc_grid.Grid(height, width)
        distance_field = [[height * width for dummy_col in range(width)]\
                          for dummy_row in range(height)]
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            for zombie in self.zombies():
                boundary.enqueue(zombie)
        if entity_type == HUMAN:
            for human in self.humans():
                boundary.enqueue(human)
        
        for cell in boundary:
            visited.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0
            
        while len(boundary) > 0:
            cur_cell = boundary.dequeue()
            neighbors = self.four_neighbors(cur_cell[0], cur_cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    if self.is_empty(neighbor[0], neighbor[1]):
                        boundary.enqueue(neighbor)
                        distance_field[neighbor[0]][neighbor[1]] = \
                        min([distance_field[neighbor[0]][neighbor[1]], \
                            distance_field[cur_cell[0]][cur_cell[1]] + 1])
        return distance_field
    
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        def is_open(cell):
            """
            Internal helper fn for filter
            """
            return self.is_empty(cell[0], cell[1])
        
        moved_humans = []
        for human in self.humans():
            best_move = human  # initialize best move to be cur pos, for now
            nbrs = self.eight_neighbors(human[0], human[1])
            nbrs = filter(is_open, nbrs)
            for nbr in nbrs:
                if zombie_distance[nbr[0]][nbr[1]] > \
                zombie_distance[best_move[0]][best_move[1]]:
                    best_move = nbr
            moved_humans.append(best_move)
        self._human_list = moved_humans
    
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        # can ignore checking for obstacles for zombies
        # because of the way compute_distance_field works
        
        moved_zombies = []
        for zombie in self.zombies():
            best_move = zombie  # initialize best move to be cur pos, for now
            nbrs = self.four_neighbors(zombie[0], zombie[1])
            for nbr in nbrs:
                if human_distance[nbr[0]][nbr[1]] < \
                human_distance[best_move[0]][best_move[1]]:
                    best_move = nbr
            moved_zombies.append(best_move)
        self._zombie_list = moved_zombies


#test1 = Zombie(5, 5, [(2, 2), (4, 1)], [(0,0)], [(1, 2)])
#print test1.zombies()
#print test1.num_zombies()
#df1 = test1.compute_distance_field(ZOMBIE)
#for i in df1:
#    print i

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(30, 40))
