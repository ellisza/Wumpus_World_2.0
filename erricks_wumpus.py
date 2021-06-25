# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys, math
from pygame.locals import *

FPS = 5
WINDOWWIDTH = 500
WINDOWHEIGHT = 500
CELLSIZE = 50
RADIUS = math.floor(CELLSIZE / 2.5)
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#                R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
LIGHTBLUE = (193, 225, 236)
DARKGRAY = (40, 40, 40)
LIGHTGRAY = (83, 83, 83)
YELLOW = (255, 255, 0)
LAKER_PURPLE = (85, 37, 130)
LAKER_GOLD = (253, 185, 39)
LAKER_BLACK = (6, 25, 34)
BGCOLOR = WHITE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0  # syntactic sugar: index of the worm's head


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.SysFont(
        'sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheadingbolditalicsitkadisplaybolditalicsitkabannerbolditalic',
        18)
    pygame.display.set_caption('Wumpus World')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    mainGrid = Grid(10, 10)
    mapElements = getRandomLocations(13)

    coords = mapElements[0]
    mainGrid.tiles[coords[0]][coords[1]].hasWumpus = True
    addStenches(coords, mainGrid)

    coords = mapElements[1]
    mainGrid.tiles[coords[0]][coords[1]].hasPit = True
    addBreezes(coords, mainGrid)

    coords = mapElements[2]
    mainGrid.tiles[coords[0]][coords[1]].hasPit = True
    addBreezes(coords, mainGrid)

    coords = mapElements[3]
    mainGrid.tiles[coords[0]][coords[1]].hasPit = True
    addBreezes(coords, mainGrid)

    coords = mapElements[4]
    mainGrid.tiles[coords[0]][coords[1]].hasGold = True

    coords = mapElements[5]
    mainGrid.tiles[coords[0]][coords[1]].hasWumpus = True
    addStenches(coords, mainGrid)

    coords = mapElements[6]
    mainGrid.tiles[coords[0]][coords[1]].hasPit = True
    addBreezes(coords, mainGrid)

    coords = mapElements[7]
    mainGrid.tiles[coords[0]][coords[1]].hasPit = True
    addBreezes(coords, mainGrid)

    coords = mapElements[8]
    mainGrid.tiles[coords[0]][coords[1]].hasPit = True
    addBreezes(coords, mainGrid)

    coords = mapElements[9]
    mainGrid.tiles[coords[0]][coords[1]].hasWumpus = True
    addStenches(coords, mainGrid)

    coords = mapElements[10]
    mainGrid.tiles[coords[0]][coords[1]].hasPit = True
    addBreezes(coords, mainGrid)

    coords = mapElements[11]
    mainGrid.tiles[coords[0]][coords[1]].hasPit = True
    addBreezes(coords, mainGrid)

    coords = mapElements[12]
    mainGrid.tiles[coords[0]][coords[1]].hasPit = True
    addBreezes(coords, mainGrid)

    # Set start point for agent
    startx1 = 0
    starty1 = 9
    startx2 = 0
    starty2 = 0
    startx3 = 9
    starty3 = 0

    agentCoord1 = Agent(startx1, starty1, UP)
    addNoises([startx1, starty1], mainGrid)
    agentCoord2 = Agent(startx2, starty2, RIGHT)
    addNoises([startx2, starty2], mainGrid)
    agentCoord3 = Agent(startx3, starty3, DOWN)
    addNoises([startx3, starty3], mainGrid)


    previous_locations1 = []
    previous_locations2 = []
    previous_locations3 = []
    while True:  # main game loop
        previous_locations1.append(agentCoord1)
        previous_locations2.append(agentCoord2)
        previous_locations3.append(agentCoord3)

        event = pygame.event.wait()  # event handling loop
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                terminate()
            if not agentCoord1.isDead:
                if event.key == K_UP:
                    if agentCoord1.direction == DOWN:
                        agentCoord1.y = min(agentCoord1.y + 1, 9)
                    elif agentCoord1.direction == UP:
                        agentCoord1.y = max(agentCoord1.y - 1, 0)
                    elif agentCoord1.direction == LEFT:
                        agentCoord1.x = max(agentCoord1.x - 1, 0)
                    elif agentCoord1.direction == RIGHT:
                        agentCoord1.x = min(agentCoord1.x + 1, 9)
                elif event.key == K_LEFT:
                    if agentCoord1.direction == UP:
                        agentCoord1.direction = LEFT
                    elif agentCoord1.direction == LEFT:
                        agentCoord1.direction = DOWN
                    elif agentCoord1.direction == DOWN:
                        agentCoord1.direction = RIGHT
                    else:
                        agentCoord1.direction = UP
                elif event.key == K_RIGHT:
                    if agentCoord1.direction == UP:
                        agentCoord1.direction = RIGHT
                    elif agentCoord1.direction == RIGHT:
                        agentCoord1.direction = DOWN
                    elif agentCoord1.direction == DOWN:
                        agentCoord1.direction = LEFT
                    else:
                        agentCoord1.direction = UP
                elif event.key == K_RETURN:
                    pass
                else:
                    print(event.key)
                    return

        # check if gold is in same tile as agent
        if mainGrid.tiles[agentCoord1.x][agentCoord1.y].hasGold:
            mainGrid.tiles[agentCoord1.x][agentCoord1.y].hasGold = False
            agentCoord1.hasGold = True

        # check if agent has died by wumpus
        if mainGrid.tiles[agentCoord1.x][agentCoord1.y].hasWumpus:
            agentCoord1.isDead = True
            if agentCoord1.hasGold == True:
                agentCoord1.hasGold = False
                mainGrid.tiles[agentCoord1.x][agentCoord1.y].hasGold = True

        # check if agent falls in pit
        if mainGrid.tiles[agentCoord1.x][agentCoord1.y].hasPit:
            agentCoord1.isDead = True
            if agentCoord1.hasGold == True:
                agentCoord1.hasGold = False
                mainGrid.tiles[agentCoord1.x][agentCoord1.y].hasGold = True

        # Check location for senses, pass those to agents current location senses array.
        if mainGrid.tiles[agentCoord1.x][agentCoord1.y].hasBreeze:
            agentCoord1.senses[0] = True
        else:
            agentCoord1.senses[0] = False

        if mainGrid.tiles[agentCoord1.x][agentCoord1.y].hasStench:
            agentCoord1.senses[1] = True
        else:
            agentCoord1.senses[1] = False

        # if mainGrid.tiles[agentCoord1.x][agentCoord1.y].hasNoise:
        #    agentCoord1.senses[2] = True
        # else:
        #    agentCoord1.senses[2] = False

        # Let agent make a decision on next move
        # moveAgent1 = agentCoord1.moveDecision()
        moveAgent1 = agentCoord1.moveDecisionOne()

        # Tell agent to make it's key press
        agentCoord1.makeMove(moveAgent1)

        # After updating senses
        DISPLAYSURF.fill(WHITE)
        drawGrid()
        addNoises([agentCoord1.x, agentCoord1.y], mainGrid)
        addNoises([agentCoord2.x, agentCoord2.y], mainGrid)
        addNoises([agentCoord3.x, agentCoord3.y], mainGrid)
        mainGrid.draw(agentCoord1)
        mainGrid.draw(agentCoord2)
        mainGrid.draw(agentCoord3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def getRandomLocations(num):
    possible_locations = []
    for i in range(10):
        for j in range(10):
            possible_locations.append([i, j])

    used = set()
    locations = []
    i = 0
    while i < num:
        idx = random.randint(1, len(possible_locations) - 1)
        if idx in used or possible_locations[idx] == [0, 9] or possible_locations[idx] == [0, 0] or possible_locations[
            idx] == [9, 0]:
            continue
        used.add(idx)
        locations.append(possible_locations[idx])
        i += 1
    return locations


def getValidMoves(coords):
    valid_moves = []
    x = coords['x']
    y = coords['y']
    if y - 1 > 0:
        valid_moves.append({'x': x, 'y': y - 1})
    if y + 1 < 10:
        valid_moves.append({'x': x, 'y': y + 1})
    if x - 1 > 0:
        valid_moves.append({'x': x - 1, 'y': y})
    if x + 1 < 10:
        valid_moves.append({'x': x + 1, 'y': y})
    return valid_moves


def addStenches(coords, grid):
    x = coords[0]
    y = coords[1]
    if y - 1 >= 0:
        grid.tiles[x][y - 1].hasStench = True
    if y + 1 < 10:
        grid.tiles[x][y + 1].hasStench = True
    if x - 1 >= 0:
        grid.tiles[x - 1][y].hasStench = True
    if x + 1 < 10:
        grid.tiles[x + 1][y].hasStench = True


def addBreezes(coords, grid):
    x = coords[0]
    y = coords[1]
    if y - 1 >= 0:
        grid.tiles[x][y - 1].hasBreeze = True
    if y + 1 < 10:
        grid.tiles[x][y + 1].hasBreeze = True
    if x - 1 >= 0:
        grid.tiles[x - 1][y].hasBreeze = True
    if x + 1 < 10:
        grid.tiles[x + 1][y].hasBreeze = True


def addNoises(coords, grid):
    x = coords[0]
    y = coords[1]
    if y - 1 >= 0:
        grid.tiles[x][y - 1].hasNoise = True
    if y + 1 < 10:
        grid.tiles[x][y + 1].hasNoise = True
    if x - 1 >= 0:
        grid.tiles[x - 1][y].hasNoise = True
    if x + 1 < 10:
        grid.tiles[x + 1][y].hasNoise = True


def moveAgent(coords, previous_locations):
    valid_moves = getValidMoves(coords)
    idx = random.randint(0, len(valid_moves) - 1)

    return valid_moves[idx]


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, LAKER_BLACK)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.SysFont(
        'sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheadingbolditalicsitkadisplaybolditalicsitkabannerbolditalic',
        100)
    titleSurf1 = titleFont.render('Wumpus', True, LAKER_PURPLE, LAKER_BLACK)
    titleSurf2 = titleFont.render('2.0', True, LAKER_GOLD)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (math.floor(WINDOWWIDTH / 2), math.floor(WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (math.floor(WINDOWWIDTH / 2), math.floor(WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def showGameOverScreen():
    gameOverFont = pygame.font.SysFont(
        'sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheadingbolditalicsitkadisplaybolditalicsitkabannerbolditalic',
        150)
    gameSurf = gameOverFont.render('Game', True, RED)
    overSurf = gameOverFont.render('Over', True, RED)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (math.floor(WINDOWWIDTH / 2), 500)
    overRect.midtop = (math.floor(WINDOWWIDTH / 2), gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, LAKER_BLACK)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawAgent(agentCoord, direction):
    x = agentCoord['x'] * CELLSIZE
    y = agentCoord['y'] * CELLSIZE
    xcenter = agentCoord['x'] * CELLSIZE + math.floor(CELLSIZE / 2)
    ycenter = agentCoord['y'] * CELLSIZE + math.floor(CELLSIZE / 2)
    pygame.draw.circle(DISPLAYSURF, LAKER_BLACK, (xcenter, ycenter), RADIUS / 2)
    if direction == RIGHT:
        directionSurf = BASICFONT.render('R', True, LAKER_BLACK)
        directionRect = directionSurf.get_rect()
        directionRect.topleft = (x + 35, y + 35)
        DISPLAYSURF.blit(directionSurf, directionRect)
    elif direction == LEFT:
        directionSurf = BASICFONT.render('L', True, LAKER_BLACK)
        directionRect = directionSurf.get_rect()
        directionRect.topleft = (x + 35, y + 35)
        DISPLAYSURF.blit(directionSurf, directionRect)
    elif direction == UP:
        directionSurf = BASICFONT.render('U', True, LAKER_BLACK)
        directionRect = directionSurf.get_rect()
        directionRect.topleft = (x + 35, y + 35)
        DISPLAYSURF.blit(directionSurf, directionRect)
    elif direction == DOWN:
        directionSurf = BASICFONT.render('D', True, LAKER_BLACK)
        directionRect = directionSurf.get_rect()
        directionRect.topleft = (x + 35, y + 35)
        DISPLAYSURF.blit(directionSurf, directionRect)


def drawDeadAgent(agentCoord):
    agentDeadFont = pygame.font.SysFont(
        'sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheadingbolditalicsitkadisplaybolditalicsitkabannerbolditalic',
        10)
    x = agentCoord['x'] * CELLSIZE
    y = agentCoord['y'] * CELLSIZE
    xcenter = agentCoord['x'] * CELLSIZE + math.floor(CELLSIZE / 2)
    ycenter = agentCoord['y'] * CELLSIZE + math.floor(CELLSIZE / 2)
    pygame.draw.circle(DISPLAYSURF, RED, (xcenter, ycenter), RADIUS / 2)
    directionSurf = agentDeadFont.render('DEAD', True, RED)
    directionRect = directionSurf.get_rect()
    directionRect.topleft = (x + 18, y + 40)
    DISPLAYSURF.blit(directionSurf, directionRect)


def drawWumpus(wumpusCoord):
    x = wumpusCoord['x'] * CELLSIZE
    y = wumpusCoord['y'] * CELLSIZE
    wormInnerSegmentRect = pygame.Rect(x + 10, y + 10, CELLSIZE - 20, CELLSIZE - 20)
    pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormInnerSegmentRect)


def drawDeadWumpus(wumpusCoord):
    x = wumpusCoord['x'] * CELLSIZE
    y = wumpusCoord['y'] * CELLSIZE
    wormInnerSegmentRect = pygame.Rect(x + 10, y + 10, CELLSIZE - 20, CELLSIZE - 20)
    pygame.draw.rect(DISPLAYSURF, RED, wormInnerSegmentRect)


def drawPit(coords):
    x = coords['x'] * CELLSIZE
    y = coords['y'] * CELLSIZE
    xcenter = coords['x'] * CELLSIZE + math.floor(CELLSIZE / 2)
    ycenter = coords['y'] * CELLSIZE + math.floor(CELLSIZE / 2)
    pygame.draw.circle(DISPLAYSURF, LAKER_PURPLE, (xcenter, ycenter), RADIUS - 5)


def drawGold(goldCoord):
    x = goldCoord['x'] * CELLSIZE
    y = goldCoord['y'] * CELLSIZE
    pygame.draw.circle(DISPLAYSURF, LAKER_GOLD, (x + 5, y + 45), RADIUS / 5)


def drawBreeze(coords):
    x = coords['x'] * CELLSIZE
    y = coords['y'] * CELLSIZE
    pygame.draw.circle(DISPLAYSURF, LIGHTBLUE, (x + 45, y + 5), RADIUS / 5)


def drawStench(coords):
    x = coords['x'] * CELLSIZE
    y = coords['y'] * CELLSIZE
    pygame.draw.circle(DISPLAYSURF, GREEN, (x + 5, y + 5), RADIUS / 5)

def drawNoise(coords):
    x = coords['x'] * CELLSIZE
    y = coords['y'] * CELLSIZE
    pygame.draw.circle(DISPLAYSURF, DARKGRAY, (x + 25, y + 5), RADIUS / 5)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


class Agent:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.arrows = 3
        self.direction = direction
        self.hasGold = False
        self.isDead = False
        self.score = 0
        # These are Breeze, Stench, Noise in order
        self.senses = [False, False, False]

        self.model = []
        temp = []
        for i in range(0, 10):
            temp = []
            for j in range(0, 10):
                temp2 = {'Breeze': False, 'Stench': False, 'Wumpus': False, 'Pit': False, 'Noise': False, 'Visited': False, 'Potential_Agent': False,
                         'Breeze_Adjacent': 0, 'Stench_Adjacent': 0, 'X': j, 'Y': i}
                temp.append(temp2)
            self.model.append(temp)
        self.movesMade = []
        self.return_mode = False
        self.return_rotations = 0
        self.next_move_turn_right = False
        self.num_rotations = 0



    def moveDecision(self):

        # We need to code this
        # Have this return a movement. Either turn left or right, move forward, or shoot an arrow.
        # For now, we'll have him go up as a test.
        if self.direction == UP:
            return "forward"

    # Helper Function - Removes all Noise Flags in all rooms in self.model, along with setting Potential_Agent to False in all rooms in self.model
    def clearNoiseFlagsFromModel(self):
        for i in range(0, 10):
            for j in range(0, 10):
                rm = self.model[i][j]
                rm['Noise'] = False
                rm['Potential_Agnet'] = False

    # Helper Function - Returns the room object in self.model at desiredX,desiredY location - returns None if it went out of bounds
    def getRoomInModel(self, desiredX, desiredY):
        if desiredX >= 0 and desiredY >= 0 and desiredX < 10 and desiredY < 10:
            return self.model[desiredX][desiredY]

    # Helper Function - Returns the room object in self.model that is above the agents current room - returns None if it went out of bounds
    def getModelRoomAbove(self):
        return self.getRoomInModel(self.x, self.y-1)

    # Helper Function - Returns the room object in the self.model that is below the agents current room - returns None if it went out of bounds
    def getModelRoomBelow(self):
        return self.getRoomInModel(self.x, self.y+1)

    # Helper Function - Returns the room object in the self.model that is to the right of the agents current room - returns None if it went out of bounds
    def getModelRoomRight(self):
        return self.getRoomInModel(self.x+1, self.y)

    # Helper Function - Returns the room object in the self.model that is to the left of the agents current room - Returns None if it wen tout of bounds
    def getModelRoomLeft(self):
        return self.getRoomInModel(self.x-1, self.y)

    # Helper Function - Loops through each room object in the self.model and updates the Breeze_Adjacent and Stench_Adjacent counts, Also updates the Potential_Agent 
    def runModelCheck(self):
        for i in range(0, 10):
            for j in range(0, 10):
                current_room = self.model[j][i]
                above = self.getModelRoomAbove()
                below = self.getModelRoomBelow()
                right = self.getModelRoomRight()
                left = self.getModelRoomLeft()

                if current_room['Noise'] == True:
                    if above != None:
                        above['Potential Agent'] = True
                    if below != None:
                        below['Potential_Agent'] = True
                    if right != None:
                        right['Potential_Agent'] = True
                    if left != None:
                        left['Potential_Agent'] = True

                stench_count = 0
                breeze_count = 0
                if above != None and above['Stench'] == True:
                    stench_count = stench_count + 1
                if above != None and above['Breeze'] == True:
                    breeze_count = breeze_count + 1
                if below != None and below['Stench'] == True:
                    stench_count = stench_count + 1
                if below != None and below['Breeze'] == True:
                    breeze_count = breeze_count + 1
                if right != None and right['Stench'] == True:
                    stench_count = stench_count + 1
                if right != None and right['Breeze'] == True:
                    breeze_count = breeze_count + 1
                if left != None and left['Stench'] == True:
                    stench_count = stench_count + 1
                if left != None and left['Breeze'] == True:
                    breeze_count = breeze_count + 1

                current_room['Breeeze_Adjacent'] = breeze_count
                current_room['Stench_Adjacent'] = stench_count

    # Helper Function - updates the self.model based on the new information obtained in our newly arrived room (based on self.senses) - calls self.runModelCheck() at end
    def updateModel(self):
        current_room = self.model[self.x][self.y]
        current_room['Visited'] = True
        current_room['Stench'] = self.senses[1]
        current_room['Breeze'] = self.senses[0]
        # current_room['Noise'] = self.senses[2]
        self.runModelCheck()
        if current_room['Stench'] == True or current_room['Breeze'] == True:
            if self.next_move_turn_right == False:
                self.next_move_turn_right = True

    # Helper Function - Returns the room object in self.model of the room ahead of us (based on our direction) if it's a valid move, if it's an out of bounds move it'll return None
    def canMoveFoward(self):
        if self.direction == UP:
            if self.y > 0:
                return self.getModelRoomAbove()
        elif self.direction == DOWN:
            if self.y < 9:
                return self.getModelRoomBelow()
        elif self.direction == LEFT:
            if self.x > 0:
                return self.getModelRoomLeft()
        elif self.direction == RIGHT:
            if self.x < 9:
                return self.getModelRoomRight()
        return None

    # HELPER FUNCTION SPECIFIC TO WASECAS AGENT LOGIC
    def getRoomRating(self, roomObject):
        if roomObject['Wumpus'] == True:
            return '7'
        if roomObject['Pit'] == True:
            return '6'
        if roomObject['Potential_Agent'] == True:
            if roomObject['Visited'] == True:
                return '4'
            else:
                return '5'
        if roomObject['Breeze'] == True or roomObject['Stench'] == True:
            if roomObject['Visited'] == True:
                return '0'
            else:
                return '2'
        return '1'

    # HELPER FUNCTION SPECIFIC TO WASECAS AGENT LOGIC
    def getNeighborSafetyRatings(self):
        # 0 - Nothing is Known / Room has been visited
        # 1 - Nothing is Known / Room has not been visited
        # 2 - Room has Breeze or Stench / Room has been Visited
        # 3 - Room has Breeze or Stench / Room has not been Visisted
        # 4 - Room has Potential Agent / Room has been Visisted
        # 5 - Room has Potential Agent / Room has not been Visisted
        # 6 - Room has Pit
        # 7 - Room has Wumpus
        current_room = self.getRoomInModel(self.x, self.y)
        above = self.getModelRoomAbove()
        below = self.getModelRoomBelow()
        right = self.getModelRoomRight()
        left = self.getModelRoomLeft()

        results = [None, None, None, None]
        if above != None:
            results[1] = self.getRoomRating(above)
        if below != None:
            results[3] = self.getRoomRating(below)
        if left != None:
            results[0] = self.getRoomRating(left)
        if right != None:
            results[2] = self.getRoomRating(right)
        return results

    # HELPER FUNCTION SPECIFIC TO WASECAS AGENT LOGIC
    def determineNecessaryMove(self, dir):
        room_ahead = self.canMoveFoward()

        if self.direction == UP:
            if dir == 0:    # Desired direction is left
                return 'left'
            elif dir == 1:  # Desired direction is up
                if room_ahead != None:
                    return 'forward'
            elif dir == 2:  # Desired direction is right
                return 'right'
            elif dir == 3:  # Desired direction is down
                return 'right'
        elif self.direction == DOWN:
            if dir == 0:    # Desired direction is left
                return 'right'
            elif dir == 1:  # Desired direction is up
                return 'right'
            elif dir == 2:  # Desired direction is right
                return 'left'
            elif dir == 3:  # Desired direction is down
                if room_ahead != None:
                    return 'forward'
        elif self.direction == RIGHT:
            if dir == 0:    # Desired direction is left
                return 'right'
            elif dir == 1:  # Desired direction is up
                return 'left'
            elif dir == 2:  # Desired direction is right
                if room_ahead != None:
                    return 'forward'
            elif dir == 3:  # Desired direction is down
                return 'right'
        elif self.direction == LEFT:
            if dir == 0:    # Desired direction is left
                if room_ahead != None:
                    return 'forward'
            elif dir == 1:  # Desired direction is up
                return 'right'
            elif dir == 2:  # Desired direction is right
                return 'right'
            elif dir == 3:  # Desired direction is down
                return 'left'
        return 'right'

    def canMoveInDir(self, dir):
        desired_rm = None
        if dir == 0: # left
            desired_rm = self.getModelRoomLeft()
        elif dir == 1: # above
            desired_rm = self.getModelRoomAbove()
        elif dir == 2: # right
            desired_rm = self.getModelRoomRight()
        elif dir == 3: # below
            desired_rm = self.getModelRoomBelow()
        if desired_rm == None:
            return False
        return True

    # HELPER FUNCTION SPECIFIC TO WASECAS AGENT LOGIC
    def regularMove(self):
        room_ahead = self.canMoveFoward()
        if (self.senses[0] == True or self.senses[1] == True or (room_ahead != None and room_ahead['Visited'] == True)) and self.num_rotations < 3:
            rnd = random.randint(0, 1)
            if rnd == 0:
                return 'right'
            return 'left'
        else:
            if room_ahead != None and room_ahead['Wumpus'] == False and room_ahead['Pit'] == False and room_ahead['Potential_Agent'] == False:
                return 'forward'
            else:
                return 'right'


    # HELPER FUNCTION SPECIFIC TO WASECAS AGENT LOGIC
    def returningToStart(self):
        if self.return_rotations < 2:
            self.return_rotations = self.return_rotations + 1
            return 'right'
        else:
            if len(self.movesMade) > 0:
                move_to_reverse = self.movesMade.pop()
                if move_to_reverse == 0:    # Reverse a Forward Action
                    return 'forward'
                elif move_to_reverse == 1:  # Reverse a Right Rotation
                    return 'left'
                elif move_to_reverse == 2:  # Reverse a Left Rotation
                    return 'right'

    # FUNCTION SPECIFIC TO WASECAS AGENT LOGIC
    def moveDecisionOne(self):
        self.clearNoiseFlagsFromModel()
        self.updateModel()
        if self.hasGold == True:
            if self.return_mode == False:
                self.return_mode = True
                self.movesMade.reverse()
            return self.returningToStart()
        else:
            result = self.regularMove()
            if result == 'forward':
                self.num_rotations = 0
                self.movesMade.append(0)
            elif result == 'right':
                self.num_rotations = self.num_rotations + 1
                self.movesMade.append(1)
            elif result == 'left':
                self.num_rotations = self.num_rotations + 1
                self.movesMade.append(2)
            return result            

    def makeMove(self, move):
        if move == "forward":
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
            pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_UP))
        elif move == "left":
            if self.direction == UP:
                self.direction = LEFT
            elif self.direction == LEFT:
                self.direction = DOWN
            elif self.direction == DOWN:
                self.direction = RIGHT
            elif self.direction == RIGHT:
                self.direction = UP
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
            pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_LEFT))
        elif move == "right":
            if self.direction == UP:
                self.direction = RIGHT
            elif self.direction == RIGHT:
                self.direction = DOWN
            elif self.direction == DOWN:
                self.direction = LEFT
            elif self.direction == LEFT:
                self.direction = UP
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
            pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT))
        elif move == "shoot":
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
            pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_UP))
        else:
            pass

    def draw(self):
        coords = {'x': self.x, 'y': self.y}
        if self.hasGold:
            drawGold(coords)
        if self.isDead:
            drawDeadAgent(coords)
        else:
            drawAgent(coords, self.direction)


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.startX = x
        self.startY = y
        self.hasStench = False
        self.hasBreeze = False
        self.hasWumpus = False
        self.hasPit = False
        self.hasGold = False
        self.hasNoise = False
        self.tilesVisited = []

    def draw(self, agent):
        coords = {'x': self.x, 'y': self.y}
        if self.hasPit:
            drawPit(coords)
        if self.hasWumpus:
            drawWumpus(coords)
        if self.hasStench:
            drawStench(coords)
        if self.hasBreeze:
            drawBreeze(coords)
        if self.hasGold:
            drawGold(coords)
        if self.hasNoise:
            self.hasNoise = False
            drawNoise(coords)
        agent.draw()
        


class Grid:
    def __init__(self, width, height):
        self.tiles = []
        for w in range(width):
            self.tiles.append([])
            for h in range(height):
                self.tiles[w].append(Tile(w, h))

    def draw(self, agent):
        for row in self.tiles:
            for tile in row:
                tile.draw(agent)


if __name__ == '__main__':
    main()