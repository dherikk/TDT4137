import numpy as np
from operator import attrgetter
import pandas as pd
from PIL import Image

class Node():
    def __init__(self, pos, par, g, h, f):
        self.pos = pos
        self.par = par
        self.g = g
        self.h = h
        self.f = f

class Map_Obj():
    def __init__(self, task=1):
        self.task = task
        self.start_pos, self.goal_pos, self.end_goal_pos, self.path_to_map = self.fill_critical_positions(
            task)
        self.int_map, self.str_map = self.read_map(self.path_to_map)
        self.tmp_cell_value = self.get_cell_value(self.goal_pos)
        self.set_cell_value(self.start_pos, ' S ')
        self.set_cell_value(self.goal_pos, ' G ')
        self.tick_counter = 0
        self.images = []

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
        return image
    
    def get_path(self, node):
        end = []
        while(node != None and node.par != None):
            end.append(node.pos)
            node = node.par
        end.append(node.pos)
        for i in end:
            self.str_map[i[0]][i[1]] = ' S '
        self.images.append(self.show_map())
        return end
    
    def astar(self):
        ### Open og closed list for å ha orden på utforskede noder og potensielt utforskbare noder
        open_list = []
        closed_list = []
        ### Setter endekordinatene
        end = self.get_goal_pos()
        ### Lager et nodeobjekt med startnode og regner ut g, h, f
        start = Node(self.get_start_pos(),
        None,
        0,
        np.sqrt((end[0]-self.get_start_pos()[0])**2 + (end[1]-self.get_start_pos()[1])**2),
        np.sqrt((end[0]-self.get_start_pos()[0])**2 + (end[1]-self.get_start_pos()[1])**2))
        ### Legger til startnode i listen
        open_list.append(start)
        while len(open_list) > 0:
            ### Finner node i listen med laves f-verdi og setter den som current (den vi utforsker)
            current = min(open_list,key=attrgetter('f'))
            ### Fjerner denne fra open list og setter den i closed list
            open_list.remove(current)
            closed_list.append(current)
            """for i in open_list:
                self.str_map[i.pos[0]][i.pos[1]] = ' O '
            for i in closed_list:
                self.str_map[i.pos[0]][i.pos[1]] = ' C '
            self.images.append(self.show_map())"""
            ### Sjekker først om current er endenoden, da vil vi finne pathen ved hjelp av Node.parent til hver node fra endenoden.
            if current.pos == end:
                end = self.get_path(current)

                ### FOR ANIMERING: 
                ### - FJERN KOMMENTERING AV KODEN OVER
                ### - KJØR KODEN SOM VANLIG
                ### - VIL OVERSKRIVE taskx.gif lokalt

                ### Visualiserer path
                self.images[0].save(f"task{self.task}.gif",
                save_all=True, append_images=self.images[1:], optimize=False, duration=len(self.images)*3, loop=0)
                self.images.clear()
                return end

            ### Sjekker om nabonodene er aktuelle for å sette i openlist
            for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:

                ### Hvis noden allerede er i closed list
                if len([node for node in closed_list if (node.pos[0] == current.pos[0] + x) and (node.pos[1] == current.pos[1] + y) ]) > 0:
                    continue

                ### Hvis noden ikke er utforskbar 
                if(self.get_cell_value([current.pos[0] + x, current.pos[1] + y])) < 0:
                    continue

                ### Setter g-, h-, og f-verdi i henhold til oppgaven
                if self.task < 3:
                    g = current.g + 1
                else:
                    g = current.g + self.get_cell_value(current.pos) + 1
                
                ### Sjekker om noden er sjekket ut før (ser om den finnes i open list)
                child = [node for node in open_list if (node.pos[0] == current.pos[0] + x) and (node.pos[1] == current.pos[1] + y) ]

                ### Hvis den er i open list, sjekk g-verdier
                if len(child) > 0:
                    if (g > child[0].g):
                        continue
                    else:
                        open_list.remove(child[0])
                h = np.sqrt((end[0]-current.pos[0])**2 + (end[1]-current.pos[1])**2)
                f = g + h

                ### Legger til noden i open list med g-, h-, og f-verdier
                open_list.append(Node([current.pos[0] + x, current.pos[1] + y ], current, g, h, f))

def main():
    ### Kjør main for å generere alle bildene.
    ### Vil ta betydelig mer tid med animering.
    task1=Map_Obj(task=1)
    task2=Map_Obj(task=2)
    task3=Map_Obj(task=3)
    task4=Map_Obj(task=4)
    res1 = task1.astar()
    res2 = task2.astar()
    res3 = task3.astar()
    res4 = task4.astar()
    print(res1, res2, res3, res4)

if __name__ == '__main__':
        main()