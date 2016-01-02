"""
Zombie Apocalypse mini-project
Name: Tri Minh Cao
Email: trimcao@gmail.com
Date: October 2015
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
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
        poc_grid.Grid.clear(self) # not sure on this
        self._zombie_list = []
        self._human_list = []
        
        
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
        # replace with an actual generator
        return (zombie for zombie in self._zombie_list)

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
        # replace with an actual generator
        return (human for human in self._human_list)
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        height = self.get_grid_height()
        width = self.get_grid_width()
        visited = poc_grid.Grid(height, width)
        distance_grid = [[(height * width) for dummy_idx in range(width)]
                         for dummy_idx2 in range(height)]
        boundary = poc_queue.Queue()
        if (entity_type == HUMAN):
            for each in self._human_list:
                boundary.enqueue(each)
        elif (entity_type == ZOMBIE):
            for each in self._zombie_list:
                boundary.enqueue(each)
        # initialize the visited and distance_grid
        for each in boundary:
            visited.set_full(each[0], each[1])
            distance_grid[each[0]][each[1]] = 0
        # use breadth-first search to generate the distance field
        while (len(boundary) > 0):
            current_cell = boundary.dequeue()
            neighbors = visited.four_neighbors(current_cell[0], current_cell[1])
            for each in neighbors:
                if not (self.is_empty(each[0], each[1])):
                    visited.set_full(each[0], each[1])
                if (visited.is_empty(each[0], each[1])):
                    visited.set_full(each[0], each[1])
                    distance_grid[each[0]][each[1]] = distance_grid[current_cell[0]][current_cell[1]] + 1
                    boundary.enqueue(each)
        
        return distance_grid
        
        
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for idx in range(len(self._human_list)):
            position = self._human_list[idx]
            neighbors = self.eight_neighbors(position[0], position[1])
   
            # create possible moves list
            possible_moves = []
            # note that one possible move is stay at the same spot
            possible_moves.append(position)
            for idx2 in range(len(neighbors)):
                each_move = neighbors[idx2]
                if (self.is_empty(each_move[0], each_move[1])):
                    possible_moves.append(each_move)
            #print possible_moves
            ideal_move = []
            max_distance = -1
            # find the move(s) that has maximal distance from zombie
            for each_move in possible_moves:
                #if (each_move not in self.
                distance = zombie_distance_field[each_move[0]][each_move[1]] 
                if (distance > max_distance):
                    max_distance = distance
                    ideal_move = []
                    ideal_move.append(each_move)
                elif (distance == max_distance):
                    ideal_move.append(each_move)
            # choose one move from the ideal_move list (randomly)
            next_move = random.choice(ideal_move)
            self._human_list[idx] = next_move
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for idx in range(len(self._zombie_list)):
            position = self._zombie_list[idx]
            neighbors = self.four_neighbors(position[0], position[1])
   
            # create possible moves list
            possible_moves = []
            # note that one possible move is stay at the same spot
            possible_moves.append(position)
            for idx2 in range(len(neighbors)):
                each_move = neighbors[idx2]
                if (self.is_empty(each_move[0], each_move[1])):
                    possible_moves.append(each_move)
            ideal_move = []
            min_distance = float("inf")
            # find the move(s) that has maximal distance from zombie
            for each_move in possible_moves:
                distance = human_distance_field[each_move[0]][each_move[1]] 
                if (distance < min_distance):
                    min_distance = distance
                    ideal_move = []
                    ideal_move.append(each_move)
                elif (distance == min_distance):
                    ideal_move.append(each_move)
            # choose one move from the ideal_move list (randomly)
            next_move = random.choice(ideal_move)
            self._zombie_list[idx] = next_move

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

#poc_zombie_gui.run_gui(Apocalypse(30, 40))
#test = Apocalypse(4, 4, None, [(0,0)], [(3,2), (2, 0)])
#test = Apocalypse(6, 5, None, [(0,0)], [(3,2), (2, 0)])
#test = Apocalypse(4, 4, [(1,2), (2,2)], [(0,0)], [(1,1)])
#test.move_humans(test.compute_distance_field(ZOMBIE))
#print test.compute_distance_field(HUMAN)
#print test.compute_distance_field(ZOMBIE)

#obj = Apocalypse(3, 3, [(0, 0), (0, 1), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)], [(0, 2)], [(1, 1)])
#poc_zombie_gui.run_gui(obj)
#dist = [[9, 9, 0], [9, 9, 9], [9, 9, 9]]
#obj.move_humans(dist)
#for each in obj.humans():
#    print each
