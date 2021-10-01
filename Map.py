import numpy as np
from Node import *
import time
import heapq
import pandas as pd
from PIL import Image


class Map_Obj():
    def __init__(self, task=1):
        self.start_pos, self.goal_pos, self.end_goal_pos, self.path_to_map = self.fill_critical_positions(
            task)
        self.int_map, self.str_map = self.read_map(self.path_to_map)
        self.tmp_cell_value = self.get_cell_value(self.goal_pos)
        self.set_cell_value(self.start_pos, ' S ')
        self.set_cell_value(self.goal_pos, ' G ')
        self.tick_counter = 0

    def read_map(self, path):
        """
        Reads maps specified in path from file, converts them to a numpy array and a string array. Then replaces
        specific values in the string array with predefined values more suitable for printing.
        :param path: Path to .csv maps
        :return: the integer map and string map
        """
        # Read map from provided csv file
        df = pd.read_csv(path, index_col=None,
                         header=None)  #,error_bad_lines=False)
        # Convert pandas dataframe to numpy array
        data = df.values
        # Convert numpy array to string to make it more human readable
        data_str = data.astype(str)
        # Replace numeric values with more human readable symbols
        data_str[data_str == '-1'] = ' # '
        data_str[data_str == '1'] = ' . '
        data_str[data_str == '2'] = ' , '
        data_str[data_str == '3'] = ' : '
        data_str[data_str == '4'] = ' ; '
        return data, data_str

    def fill_critical_positions(self, task):
        """
        Fills the important positions for the current task. Given the task, the path to the correct map is set, and the
        start, goal and eventual end_goal positions are set.
        :param task: The task we are currently solving
        :return: Start position, Initial goal position, End goal position, path to map for current task.
        """
        if task == 1:
            start_pos = [27, 18]
            goal_pos = [40, 32]
            end_goal_pos = goal_pos
            path_to_map = 'Samfundet_map_1.csv'
        elif task == 2:
            start_pos = [40, 32]
            goal_pos = [8, 5]
            end_goal_pos = goal_pos
            path_to_map = 'Samfundet_map_1.csv'
        elif task == 3:
            start_pos = [28, 32]
            goal_pos = [6, 32]
            end_goal_pos = goal_pos
            path_to_map = 'Samfundet_map_2.csv'
        elif task == 4:
            start_pos = [28, 32]
            goal_pos = [6, 32]
            end_goal_pos = goal_pos
            path_to_map = 'Samfundet_map_Edgar_full.csv'
        elif task == 5:
            start_pos = [14, 18]
            goal_pos = [6, 36]
            end_goal_pos = [6, 7]
            path_to_map = 'Samfundet_map_2.csv'

        return start_pos, goal_pos, end_goal_pos, path_to_map

    def get_cell_value(self, pos):
        return self.int_map[pos[0], pos[1]]

    def get_goal_pos(self):
        return self.goal_pos

    def get_start_pos(self):
        return self.start_pos

    def get_end_goal_pos(self):
        return self.end_goal_pos

    def get_maps(self):
        # Return the map in both int and string format
        return self.int_map, self.str_map

    def move_goal_pos(self, pos):
        """
        Moves the goal position towards end_goal position. Moves the current goal position and replaces its previous
        position with the previous values for correct printing.
        :param pos: position to move current_goal to
        :return: nothing.
        """
        tmp_val = self.tmp_cell_value
        tmp_pos = self.goal_pos
        self.tmp_cell_value = self.get_cell_value(pos)
        self.goal_pos = [pos[0], pos[1]]
        self.replace_map_values(tmp_pos, tmp_val, self.goal_pos)

    def set_cell_value(self, pos, value, str_map=True):
        if str_map:
            self.str_map[pos[0], pos[1]] = value
        else:
            self.int_map[pos[0], pos[1]] = value

    def print_map(self, map_to_print):
        # For every column in provided map, print it
        for column in map_to_print:
            print(column)

    def pick_move(self):
        """
        A function used for moving the goal position. It moves the current goal position towards the end_goal position.
        :return: Next coordinates for the goal position.
        """
        if self.goal_pos[0] < self.end_goal_pos[0]:
            return [self.goal_pos[0] + 1, self.goal_pos[1]]
        elif self.goal_pos[0] > self.end_goal_pos[0]:
            return [self.goal_pos[0] - 1, self.goal_pos[1]]
        elif self.goal_pos[1] < self.end_goal_pos[1]:
            return [self.goal_pos[0], self.goal_pos[1] + 1]
        else:
            return [self.goal_pos[0], self.goal_pos[1] - 1]

    def replace_map_values(self, pos, value, goal_pos):
        """
        Replaces the values in the two maps at the coordinates provided with the values provided.
        :param pos: coordinates for where we want to change the values
        :param value: the value we want to change to
        :param goal_pos: The coordinate of the current goal
        :return: nothing.
        """
        if value == 1:
            str_value = ' . '
        elif value == 2:
            str_value = ' , '
        elif value == 3:
            str_value = ' : '
        elif value == 4:
            str_value = ' ; '
        else:
            str_value = str(value)
        self.int_map[pos[0]][pos[1]] = value
        self.str_map[pos[0]][pos[1]] = str_value
        self.str_map[goal_pos[0], goal_pos[1]] = ' G '

    def tick(self):
        """
        Moves the current goal position every 4th call if current goal position is not already at the end_goal position.
        :return: current goal position
        """
        # For every 4th call, actually do something
        if self.tick_counter % 4 == 0:
            # The end_goal_pos is not set
            if self.end_goal_pos is None:
                return self.goal_pos
            # The current goal is at the end_goal
            elif self.end_goal_pos == self.goal_pos:
                return self.goal_pos
            else:
                # Move current goal position
                move = self.pick_move()
                self.move_goal_pos(move)
                #print(self.goal_pos)
        self.tick_counter += 1

        return self.goal_pos

    def set_start_pos_str_marker(self, start_pos, map):
        # Attempt to set the start position on the map
        if self.int_map[start_pos[0]][start_pos[1]] == -1:
            self.print_map(self.str_map)
            print('The selected start position, ' + str(start_pos) +
                  ' is not a valid position on the current map.')
            exit()
        else:
            map[start_pos[0]][start_pos[1]] = ' S '

    def set_goal_pos_str_marker(self, goal_pos, map):
        # Attempt to set the goal position on the map
        if self.int_map[goal_pos[0]][goal_pos[1]] == -1:
            self.print_map(self.str_map)
            print('The selected goal position, ' + str(goal_pos) +
                  ' is not a valid position on the current map.')
            exit()
        else:
            map[goal_pos[0]][goal_pos[1]] = ' G '

    def show_map(self, map=None):
        """
        A function used to draw the map as an image and show it.
        :param map: map to use
        :return: nothing.
        """
        # If a map is provided, set the goal and start positions
        if map is not None:
            self.set_start_pos_str_marker(self.start_pos, map)
            self.set_goal_pos_str_marker(self.goal_pos, map)
        # If no map is provided, use string_map
        else:
            map = self.str_map

        # Define width and height of image
        width = map.shape[1]
        height = map.shape[0]
        # Define scale of the image
        scale = 20
        # Create an all-yellow image
        image = Image.new('RGB', (width * scale, height * scale),
                          (255, 255, 0))
        # Load image
        pixels = image.load()

        # Define what colors to give to different values of the string map (undefined values will remain yellow, this is
        # how the yellow path is painted)
        colors = {
            ' # ': (211, 33, 45),
            ' . ': (215, 215, 215),
            ' , ': (166, 166, 166),
            ' : ': (96, 96, 96),
            ' ; ': (36, 36, 36),
            ' S ': (255, 0, 255),
            ' G ': (0, 128, 255),
            ' O ': (0, 255, 0),
            ' C ': (0, 0, 255)
        }
        # Go through image and set pixel color for every position
        for y in range(height):
            for x in range(width):
                if map[y][x] not in colors: continue
                for i in range(scale):
                    for j in range(scale):
                        pixels[x * scale + i,
                               y * scale + j] = colors[map[y][x]]
        # Show image
        return image

    def return_path(self, current_node):
        path = []
        current = current_node
        while current is not None:
            path.append(current.pos)
            current = current.par
        g = path[::-1]
        for i in g:
            self.str_map[i[0]][i[1]] = ' S '
        return g

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


    def astar(self, start, end):
        """
        Returns the path as a list of tuples from start to end in the given map
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
        images.append(self.show_map())
        

        #initialize the open and closed lists
        open_list = []
        closed_list = []
        heapq.heapify(open_list) 
        heapq.heappush(open_list, start_node)
        ###############open_list.append(start_node) 
        
        n_iter=0
        #loop until you find the goal node
        while len(open_list) > 0:

            n_iter+=1
            #get the current node and add it to the closed list
            ########current_node = open_list[-1] 
            current_node = heapq.heappop(open_list)
            closed_list.append(current_node)

            for i in open_list:
                self.str_map[i.pos[0]][i.pos[1]] = ' O '
            for i in closed_list:
                self.str_map[i.pos[0]][i.pos[1]] = ' C '
            images.append(self.show_map())
            print("Image array length", len(images))
            #if we are at goal
            if current_node==goal_node:
                temp = self.return_path(current_node)
                images[0].save('task2.gif',
                save_all=True, append_images=images[1:], optimize=False, duration=len(images)*3, loop=0)
                return temp
            
            #unzip the current location
            (x,y)=current_node.pos
            
            #define the nodes neighbours
            neighbours=[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
            
            #generate children
            for new_pos in neighbours:
                
                #get value from map
                map_value=self.int_map[new_pos[0]][new_pos[1]]
                
                #avoid roadblocks
                if map_value == -1:
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
    map1=Map_Obj(task=2)
    #get the start and goal nodes and unzip their components
    start=map1.get_start_pos()
    startnode=(start[0],start[1])
    goal=map1.get_goal_pos()
    goalnode=(goal[0],goal[1])
    print(startnode,goalnode)
    #run the algorithm
    res=map1.astar(startnode ,goalnode)
    #and print the result
    print(res)

if __name__ == '__main__':
        main()