from room import Room
from cave import Cave
import random


class Agent:
    def __init__(self, c, d=False):
        self.score = 0
        self.treasure = False
        self.arrow = True
        # self.prevMove = None
        self.dead = False
        self.finished = False
        self.cave_object = c
        self.moves = [] #0 = Left, 1 = Up, 2 = Right, 3 = Down
        self.prev_five_rooms = []
        self.display = d

    
    # Method I used once I got the Treasure to take my previous move list in reverse to make it back to the goal position
    def backtrack(self):
        self.moves.reverse()
        while(len(self.moves) > 0):
            prev_move = self.moves.pop()
            new_cell = None
            if prev_move == 0:
                # Move = Left, need to make a right
                new_cell = self.cave_object.move_right()
            elif prev_move == 1:
                # Move = Up, need to move down
                new_cell = self.cave_object.move_down()
            elif prev_move == 2:
                # Made a right, need to make a left
                new_cell = self.cave_object.move_left()
            elif prev_move == 3:
                # Made a down move, need to move up
                new_cell = self.cave_object.move_up()
            self.examine_move_made(new_cell)
            if self.display == True:
                self.cave_object.text_display()
        current_cell = self.cave_object.get_current_cell()
        if current_cell.row == 0 and current_cell.col == 0:
            if self.display == True:
                print("YOU WIN")
                print("score: " + str(self.score))

    # cell to shoot is a room object - there are convenient getter functions in the cave class you can use to get a room in any direction of a given row and column 
    def use_arrow(self, cell_to_shoot):
        # shoot arrow at cell in sepcified direction
        if self.arrow == True:
            if self.display == True:
                print("Using Arrow")
            if cell_to_shoot.wumpus == True:
                if self.display == True:
                    print("Successfully shot wumpus")
                cell_to_shoot.wumpus = False
                self.cave_object.remove_stench()
            self.score = self.score - 10
            self.arrow = False

    # function to add a visited room to my list of moves to use later for backtracking
    def add_room_to_history(self, rm):
        self.prev_five_rooms.append(rm)
        if len(self.prev_five_rooms) > 5:
            self.prev_five_rooms.pop()

    # Given a room object, it checks if it's a valid move (not running into a wall) - also does additional safety checks based on information about a cell (which it only has if it has visited the cell before - so model based - i assumed if player has been there it has access to the cells information - so i didnt have to log all the information about a cell twice)
    def check_move(self, desired_cell):
        above = self.cave_object.get_cell_above(desired_cell.row, desired_cell.col)
        below = self.cave_object.get_cell_below(desired_cell.row, desired_cell.col)
        l = self.cave_object.get_cell_left(desired_cell.row, desired_cell.col)
        r = self.cave_object.get_cell_right(desired_cell.row, desired_cell.col)

        found_stench = False
        found_breeze = False

        curr = self.cave_object.get_current_cell()
        if above != None and above.breadcrumbs == True and above != curr:
            if above.stench == True:
                found_stench = True
            elif above.breeze == True:
                found_breeze = True
        if below != None and below.breadcrumbs == True and below != curr:
            if below.stench == True:
                found_stench = True
            elif below.breeze == True:
                found_breeze = True
        if l != None and l.breadcrumbs == True and l != curr:
            if l.stench == True:
                found_stench = True
            elif l.breeze == True:
                found_breeze = True
        if r != None and r.breadcrumbs == True and r != curr:
            if r.stench == True:
                found_stench = True
            elif r.breeze == True:
                found_breeze = True

        # return 0 if nothing found, 1 if breeze only found, 2 if stench only found, 3 if both breeze and stench found
        if found_breeze == True and found_stench == True:
            return 3
        elif found_breeze == True and found_stench == False:
            return 1
        elif found_stench == True and found_breeze == False:
            return 2
        elif found_breeze == False and found_stench == False:
            return 0

    # My method for selecting the next move for my agent to make - not the best - honestly was just trying to get a passing grade
    def random_move(self):
        current_cell = self.cave_object.get_current_cell()
        attempts = 0
        attempted = []
        while(True):
            dir = random.randint(0, 3)
            if dir not in attempted:
                attempted.append(dir)
                attempts = attempts + 1
            new_location = None
            if dir == 0:    # Left
                new_location = self.cave_object.get_cell_left(current_cell.row, current_cell.col)
            elif dir == 1: # Up
                new_location = self.cave_object.get_cell_above(current_cell.row, current_cell.col)
            elif dir == 2: # Right
                new_location = self.cave_object.get_cell_right(current_cell.row, current_cell.col)
            elif dir == 3: # Down
                new_location = self.cave_object.get_cell_below(current_cell.row, current_cell.col)

            if new_location != None:
                check_result = 0
                if self.arrow == True:
                    if current_cell.stench == True or current_cell.breeze == True:
                        check_result = self.check_move(new_location)
                if check_result == 0 or attempts >= 4:
                    if dir == 0:
                        actual_new_loc = self.cave_object.move_left()
                    elif dir == 1:
                        actual_new_loc = self.cave_object.move_up()
                    elif dir == 2:
                        actual_new_loc = self.cave_object.move_right()
                    elif dir == 3:
                        actual_new_loc = self.cave_object.move_down()

                    actual_new_loc.breadcrumbs = True
                    self.moves.append(dir)
                    self.add_room_to_history(actual_new_loc)
                    self.examine_move_made(actual_new_loc)
                    break

    # Once a move is made, the random_move method calls this method. This method exames the new cell location and determines whether it is to grab the treasure or potentially is dead (ends the game)
    def examine_move_made(self, new_cell):
        if new_cell != None:
            self.score = self.score - 1
            if new_cell.goal == True:
                if self.treasure == True:
                    self.finished = True
                    self.score = self.score + 200
            elif new_cell.treasure == True:
                new_cell.treasure = False
                self.treasure = True
            elif new_cell.wumpus == True:
                self.dead = True
                self.score = self.score - 200
            elif new_cell.pit == True:
                self.dead = True
                self.score = self.score - 100

    # Runs my agent
    def run_agent(self):
        while(self.dead == False and self.treasure == False):
            curr_cell = self.cave_object.get_current_cell()
            if curr_cell.stench == True:
                u_r = self.cave_object.get_upper_right_diagonal(curr_cell.row, curr_cell.col)
                u_l = self.cave_object.get_upper_left_diagonal(curr_cell.row, curr_cell.col)
                l_r = self.cave_object.get_lower_left_diagonal(curr_cell.row, curr_cell.col)
                l_l = self.cave_object.get_lower_right_diagonal(curr_cell.row, curr_cell.col)

                if u_r != None and u_r.breadcrumbs == True and u_r.stench == True:
                    # shoot arrow to right
                    cell_to_shoot_at = self.cave_object.get_cell_right(curr_cell.row, curr_cell.col)
                    if cell_to_shoot_at != None:
                        self.use_arrow(cell_to_shoot_at)
                elif u_l != None and u_l.breadcrumbs == True and u_l.stench == True:
                    # Shoot arrow to left
                    cell_to_shoot_at = self.cave_object.get_cell_left(curr_cell.row, curr_cell.col)
                    if cell_to_shoot_at != None:
                        self.use_arrow(cell_to_shoot_at)
                elif l_r != None and l_r.breadcrumbs == True and l_r.stench == True:
                    # shoot arrow to right
                    cell_to_shoot_at = self.cave_object.get_cell_right(curr_cell.row, curr_cell.col)
                    if cell_to_shoot_at != None:
                        self.use_arrow(cell_to_shoot_at)
                elif l_l != None and l_l.breadcrumbs == True and l_l.stench == True:
                    # shoot arrow to left
                    cell_to_shoot_at = self.cave_object.get_cell_left(curr_cell.row, curr_cell.col)
                    if cell_to_shoot_at != None:
                        self.use_arrow(cell_to_shoot_at)
            self.random_move()
            if self.display == True:
                self.cave_object.text_display()
        if self.dead == True:
            if self.display == True:
                print ("YOU LOSE")
        elif self.treasure == True:
            # Make way back to starting point
            if self.display == True:
                print("FOUND TREASURE")
            self.backtrack()
