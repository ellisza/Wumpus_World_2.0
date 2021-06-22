# Room class which represents an individual cell in the overall grid (cave)
class Room:
    def __init__(self):
        self.row = None     # the cells row number
        self.col = None     # the cells column number
        self.current = False    # marked as True if it's the players current position - will need to get rid of / adjust for project
        self.wumpus = False     # Marked True if the Wumpus is here
        self.pit = False        # Marked True if a Pit is placed here
        self.treasure = False   # Marked True if the Treasure is placed here - will be marked False when the Treasure is taken from here
        self.stench = False     # Marked True if there is a stench here - marked back to False when Wumpus is killed
        self.breeze = False     # Marked True if there is a breeze here
        self.breadcrumbs = False    # Marked True if player has been to this cell - will need to adjust for project
        self.goal = False       # Marked True if this is the players initial position / goal cell - will need to adjust for project

    
    # Returns True if this cell has a Wumpus, Pit, Treasure, Stench, Breeze or is the Goal (used when finding random cells in setup)
    def has_something(self):
        if self.wumpus == True or self.pit == True or self.treasure == True or self.stench == True or self.breeze == True or self.goal == True:
            return True
        return False


    # Function that returns the cells text representation for the display
    def get_text_rep(self):
        result = [" ", " ", " ", " "]
        if self.goal:
            result[0] = "G"
        elif self.treasure:
            result[0] = "T"
        elif self.wumpus:
            result[0] ="W"
        elif self.pit:
            result[0] = "P"

        if self.stench:
            result[1] = "S"
        elif self.breeze:
            result[1] = "B"

        if self.current:
            result[2] = "C"

        if self.breadcrumbs == True:
            result[3] = "V"
        res = str("[" + str(result[0]) + "," + str(result[1]) + "," + str(result[2]) + "," + str(result[3]) + "]")
        return res
