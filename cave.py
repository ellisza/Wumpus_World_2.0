from room import Room
import random


# Cave class represents the entire grid - cave class contains 2d array of room objects
class Cave:
    def __init__(self):
        self.rooms = []
        for i in range(0, 5):
            temp = []
            for j in range(0, 5):
                new_room = Room()
                new_room.row = i
                new_room.col = j
                temp.append(new_room)
            self.rooms.append(temp)

        self.wumpus_alive = True
        self.treasure_found = False
        self.gameover = False
        self.current_location = None    # will contain room object of players current position - will need to get rid of for our project

    # Returns room object of players current position - will need to get rid of for our project
    def get_current_cell(self):
        return self.current_location

    # moves return the new cell the agent is currently in - or none if the move wasn't possible (hit a wall)
    def move_left(self):
        new_cell = self.get_cell_left(self.current_location.row, self.current_location.col)
        if new_cell != None:
            self.current_location.current = False
            self.current_location = new_cell
            new_cell.current = True
            new_cell.breadcrumbs = 0
            return new_cell
        return None

    def move_right(self):
        new_cell = self.get_cell_right(self.current_location.row, self.current_location.col)
        if new_cell != None:
            self.current_location.current = False
            self.current_location = new_cell
            new_cell.current = True
            new_cell.breadcrumbs = 2
            return new_cell
        return None

    def move_down(self):
        new_cell = self.get_cell_below(self.current_location.row, self.current_location.col)
        if new_cell != None:
            self.current_location.current = False
            self.current_location = new_cell
            new_cell.current = True
            new_cell.breadcrumbs = 1
            return new_cell
        return None

    def move_up(self):
        new_cell = self.get_cell_above(self.current_location.row, self.current_location.col)
        if new_cell != None:
            self.current_location.current = False
            self.current_location = new_cell
            new_cell.current = True
            new_cell.breadcrumbs = 3
            return new_cell
        return None


    # works with multiple wumpus
    def get_all_wumpus_coords(self):
        results = []
        for row in self.rooms:
            for rm in row:
                if rm.wumpus == True:
                    rm_coords = {'x': rm.row, 'y':rm.col}
                    # rm_coords = [rm.row, rm.col]
                    results.append(rm_coords)
        return results
    
    def get_treasure_coords(self):
        results = []
        for row in self.rooms:
            for rm in row:
                if rm.treasure == True:
                    rm_coords = {'x': rm.row, 'y':rm.col}
                    # rm_coords = [rm.row, rm.col]
                    results.append(rm_coords)
        return results

    def get_all_pit_coords(self):
        results = []
        for row in self.rooms:
            for rm in row:
                if rm.pit == True:
                    rm_coords = {'x': rm.row, 'y':rm.col}
                    results.append(rm_coords)
        return results

    def get_all_stench_coords(self):
        results = []
        for row in self.rooms:
            for rm in row:
                if rm.stench == True:
                    rm_coords = {'x': rm.row, 'y':rm.col}
                    results.append(rm_coords)
        return results

    def get_all_breeze_coords(self):
        results = []
        for row in self.rooms:
            for rm in row:
                if rm.breeze == True:
                    rm_coords = {'x': rm.row, 'y':rm.col}
                    results.append(rm_coords)
        return results

    def get_all_agent_coords(self):
        results = []
        for row in self.rooms:
            for rm in row:
                if rm.current == True:       # Might need to be changed in project
                    rm_coords = {'x': rm.row, 'y':rm.col}
                    results.append(rm_coords)
        return results

    def get_rand_location(self):
        r = random.randint(0, 4)
        c = random.randint(0, 4)
        cell = self.rooms[r][c]
        return cell

    def get_cell_above(self, r, c):
        new_row = r - 1
        if new_row >= 0:
            cell = self.rooms[new_row][c]
            return cell
        else:
            return None

    def get_cell_below(self, r, c):
        new_row = r + 1
        if new_row <= 4:
            cell = self.rooms[new_row][c]
            return cell
        else:
            return None

    def get_cell_right(self, r, c):
        new_col = c + 1
        if new_col <= 4:
            cell = self.rooms[r][new_col]
            return cell
        else:
            return None

    def get_cell_left(self, r, c):
        new_col = c - 1
        if new_col >= 0:
            cell = self.rooms[r][new_col]
            return cell
        else:
            return None

    def get_upper_right_diagonal(self, r, c):
        above = self.get_cell_above(r, c)
        if above != None:
            return self.get_cell_right(above.row, above.col)
        return None

    def get_upper_left_diagonal(self, r, c):
        above = self.get_cell_above(r, c)
        if above != None:
            return self.get_cell_left(above.row, above.col)
        return None

    def get_lower_right_diagonal(self, r, c):
        below = self.get_cell_below(r, c)
        if below != None:
            return self.get_cell_right(below.row, below.col)
        return None

    def get_lower_left_diagonal(self, r, c):
        below = self.get_cell_below(r, c)
        if below != None:
            return self.get_cell_left(below.row, below.col)
        return None

    def setup(self):
        # sets the 0,0 position as the start/goal/current position of player - will need to adjust this for project
        self.current_location = self.rooms[0][0]
        self.rooms[0][0].current = True
        self.rooms[0][0].goal = True

        # Places one Treasure object
        while(True):
            t_room = self.get_rand_location()
            if t_room.has_something() == False:
                t_room.treasure = True
                break

        # Places a Wumpus and adjusts its neighboring cells to have stench
        while(True):
            w_room = self.get_rand_location()
            if w_room.has_something() == False:
                w_room.wumpus = True
                l = self.get_cell_left(w_room.row, w_room.col)
                r = self.get_cell_right(w_room.row, w_room.col)
                u = self.get_cell_above(w_room.row, w_room.col)
                d = self.get_cell_below(w_room.row, w_room.col)

                if l != None:
                    l.stench = True
                if r != None:
                    r.stench = True
                if u != None:
                    u.stench = True
                if d != None:
                    d.stench = True
                break

        # Places 3 pits and adjusts neighboring cells to have a breeze
        for i in range(0, 3):
            while(True):
                p_room = self.get_rand_location()
                if p_room.has_something() == False:
                    p_room.pit = True
                    l = self.get_cell_left(p_room.row, p_room.col)
                    r = self.get_cell_right(p_room.row, p_room.col)
                    u = self.get_cell_above(p_room.row, p_room.col)
                    d = self.get_cell_below(p_room.row, p_room.col)

                    if l != None:
                        l.breeze = True
                    if r != None:
                        r.breeze = True
                    if u != None:
                        u.breeze = True
                    if d != None:
                        d.breeze = True
                    break

    # function to remove stench from board (in the scenario where the wumpus is killed) - will need to do this differently if we have multiple wumpus in our project
    def remove_stench(self):
        for i in range(0, 4):
            for j in range(0, 4):
                c = self.rooms[i][j]
                if c.stench == True:
                    c.stench = False

    # This is my display of the game - i did not do a nice pygame display
    def text_display(self):
        print("--------------------------------------------------")
        print("G: GOAL        C: CURRENT    W: WUMPUS")
        print("T: TREASURE    P: PIT        V: VISITED")
        print("B: BREEZE      S: STENCH")
        for i in range(0, 5):
            for j in range(0, 5):
                r = self.rooms[i][j]
                t = r.get_text_rep()
                print(t, end=" ")
            if i != 4:
                print("\n")
        print("\n--------------------------------------------------")
