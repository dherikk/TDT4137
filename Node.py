import heapq
import numpy as np
from warnings import warn
from Map import *

class Node:

    def __init__(self, par=None, pos=None):
        self.par = par
        self.pos = pos
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f
    
    def __gt__(self, other):
      return self.f > other.f

    def __eq__(self, other):
        return self.pos == other.pos
    
    def __repr__(self):
      return f"{self.pos} - g: {self.g} h: {self.h} f: {self.f}"


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.pos)
        current = current.par
    return path[::-1]

def dist(actual_pos, goal_pos, norm="manhattan"):
  if norm=="manhattan" or "L1":
    return np.abs(actual_pos[0]-goal_pos[0]) + np.abs(actual_pos[1]-goal_pos[1])
  if norm=="euclidean" or "L2":
    return np.sqrt(np.abs(actual_pos[0]-goal_pos[0])**2 + np.abs(actual_pos[1]-goal_pos[1])**2)

# Check if a neighbor should be added to open list
def add_to_open(open, neighbour):
    for node in open:
        if (neighbour == node and neighbour.f >= node.f):
            return False
    return True


def astar(map, start, end):
    """
    Returns the path as a list of tuples from start to end in the given map
    :param map:     the given map
    :param start:   the start node
    :param end:     the goal node
    :return:
    """

    #setup the start and goalnodes
    start_node = Node(None, start)
    goal_node = Node(None, end)
    start_node.g = 0
    start_node.h = dist(start_node.pos, goal_node.pos)
    start_node.f = start_node.g+start_node.h
    goal_node.g = goal_node.h = goal_node.f = 0
    images = []
    

    #initialize the open and closed lists
    open_list = []
    closed_list = []
    open_list.append(start_node) ###############
    
    n_iter=0
    #loop until you find the goal node
    while len(open_list) > 0:

        n_iter+=1
        #get the current node and add it to the closed list
        current_node = open_list[-1] ########
        closed_list.append(current_node)
        
        #if we are at goal
        if current_node==goal_node:
            return return_path(current_node)
        
        #unzip the current location
        (x,y)=current_node.pos
        
        #define the nodes neighbours
        neighbours=[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
        
        #generate children
        for new_pos in neighbours:
            
            #get value from map
            map_value=map[new_pos[0]][new_pos[1]]
            
            #avoid roadblocks
            if map_value ==' # ':
                continue
            
            #create neighbour node
            neighbour=Node(current_node,new_pos)
            
            #check if new node is already in closed_list
            if neighbour in closed_list:
                continue
            
            #set the dists
            #neighbour.g = dist(neighbour.pos, start_node.pos, 'L1')
            neighbour.g = dist(neighbour.pos, start_node.pos, 'L1')
            neighbour.h = dist(neighbour.pos, goal_node.pos, 'L1')
            neighbour.f = neighbour.g + neighbour.h
            
            #check if we should explore
            if add_to_open(open_list, neighbour):
                open_list.append(neighbour)
                
    #no path is found
    return None

def main():
    map1=Map_Obj(task=1)
    kart=map1.get_maps()[1]
    #get the start and goal nodes and unzip their components
    start=map1.get_start_pos()
    startnode=(start[0],start[1])
    goal=map1.get_goal_pos()
    goalnode=(goal[0],goal[1])
    print(startnode,goalnode)
    #run the algorithm
    res=astar(kart,startnode,goalnode)
    #and print the result
    print(res)
    visual=kart
    #visualize the path
    """for koord in res:
        visual[koord[0]][koord[1]] = '-> '
    #show the solution
    map1.print_map(visual)
    map1.show_map(visual)"""

if __name__ == '__main__':
        main()
