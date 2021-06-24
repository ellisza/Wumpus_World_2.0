# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys, math
from pygame.locals import *

FPS = 5
WINDOWWIDTH = 1000
WINDOWHEIGHT = 1000
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
    mainGrid = Grid(20, 20)
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
    starty1 = 19
    startx2 = 0
    starty2 = 0
    startx3 = 19
    starty3 = 0

    agentCoord1 = Agent(startx1, starty1, UP)
    agentCoord2 = Agent(startx2, starty2, RIGHT)
    agentCoord3 = Agent(startx3, starty3, DOWN)

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
                        agentCoord1.y = min(agentCoord1.y + 1, 19)
                    elif agentCoord1.direction == UP:
                        agentCoord1.y = max(agentCoord1.y - 1, 0)
                    elif agentCoord1.direction == LEFT:
                        agentCoord1.x = max(agentCoord1.x - 1, 0)
                    elif agentCoord1.direction == RIGHT:
                        agentCoord1.x = min(agentCoord1.x + 1, 19)
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
        moveAgent1 = agentCoord1.moveDecision()

        # Tell agent to make it's key press
        agentCoord1.makeMove(moveAgent1)

        # After updating senses
        DISPLAYSURF.fill(WHITE)
        drawGrid()
        mainGrid.draw()
        agentCoord1.draw()
        agentCoord2.draw()
        agentCoord3.draw()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def getRandomLocations(num):
    possible_locations = []
    for i in range(20):
        for j in range(20):
            possible_locations.append([i, j])

    used = set()
    locations = []
    i = 0
    while i < num:
        idx = random.randint(1, len(possible_locations) - 1)
        if idx in used or possible_locations[idx] == [0, 19] or possible_locations[idx] == [0, 0] or possible_locations[
            idx] == [19, 0]:
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
    if y + 1 < 20:
        valid_moves.append({'x': x, 'y': y + 1})
    if x - 1 > 0:
        valid_moves.append({'x': x - 1, 'y': y})
    if x + 1 < 20:
        valid_moves.append({'x': x + 1, 'y': y})
    return valid_moves


def addStenches(coords, grid):
    x = coords[0]
    y = coords[1]
    if y - 1 >= 0:
        grid.tiles[x][y - 1].hasStench = True
    if y + 1 < 20:
        grid.tiles[x][y + 1].hasStench = True
    if x - 1 >= 0:
        grid.tiles[x - 1][y].hasStench = True
    if x + 1 < 20:
        grid.tiles[x + 1][y].hasStench = True


def addBreezes(coords, grid):
    x = coords[0]
    y = coords[1]
    if y - 1 >= 0:
        grid.tiles[x][y - 1].hasBreeze = True
    if y + 1 < 20:
        grid.tiles[x][y + 1].hasBreeze = True
    if x - 1 >= 0:
        grid.tiles[x - 1][y].hasBreeze = True
    if x + 1 < 20:
        grid.tiles[x + 1][y].hasBreeze = True


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
    pygame.draw.circle(DISPLAYSURF, LAKER_PURPLE, (xcenter, ycenter), RADIUS)


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


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


class Agent:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.arrows = 3
        self.direction = direction
        self.hasGold = False
        self.isDead = False
        self.score = 0
        # These are Breeze, Stench, Noise in order
        self.senses = [False, False, False]

        self.model = []
        temp = []
        for i in range(0, 20):
            temp = []
            for j in range(0, 20):
                temp2 = {'Breeze': False, 'Stench': False, 'Wumpus': False, 'Pit': False, 'Visited': False, 'Breeze_Adjacent': 0, 'Stench_Adjacent': 0}
                temp.append(temp2)
            self.model.append(temp)


    def moveDecision(self):

        # We need to code this
        # Have this return a movement. Either turn left or right, move forward, or shoot an arrow.
        # For now, we'll have him go up as a test.
        if self.direction == UP:
            return "forward"


    # Helper Function for moveDecisionTwo
    def updateModel(self):
        for x in range(0, 20):
            for y in range(0, 20):
                rm = self.model[x][y]
                stench_count = 0
                breeze_count = 0
                if (x-1) >= 0:
                    above = self.model[x-1][y]
                    if above['Stench'] == True:
                        stench_count = stench_count + 1
                    if above['Breeze'] == True:
                        breeze_count = breeze_count + 1
                if (x+1) < 20:
                    below = self.model[x+1][y]
                    if below['Stench'] == True:
                        stench_count = stench_count + 1
                    if below['Breeze'] == True:
                        breeze_count = breeze_count + 1
                if (y-1) >= 0:
                    left = self.model[x][y-1]
                    if left['Stench'] == True:
                        stench_count = stench_count + 1
                    if left['Breeze'] == True:
                        breeze_count = breeze_count + 1
                if (y+1) < 20:
                    right = self.model[x][y+1]
                    if right['Stench'] == True:
                        stench_count = stench_count + 1
                    if right['Breeze'] == True:
                        breeze_count = breeze_count + 1
                rm['Stench_Adjacent'] = stench_count
                rm['Breeze_Adjacent'] = breeze_count
                if stench_count >= 3:
                    rm['Wumpus'] = True
                if breeze_count >= 3:
                    rm['Pit'] = True


    # Need to incorporate logic of when to shoot arrow and once have treasure making way back
    def moveDecisionTwo(self):
        current_room = self.model[self.x][self.y]
        current_room['Breeze'] = self.senses[0]
        current_room['Stench'] = self.senses[1]
        current_room['Visited'] = True
        self.updateModel()
        safe_moves = [0, 0, 0, 0]   # Up, Down, Left, Right
            # 0 means unknown, 1 means unsafe, 2 means possibly unsafe, 3 means visited
        # Check if moving forward is a new room / safe assumption - else check room to left then right then below - if none are safe - either shoot arrow or make random choice
        above, below, right, left = None, None, None, None
        if self.x >= 1:
            above = self.grid[self.x-1][self.y]
        if self.x < 19:
            below = self.grid[self.x+1][self.y]
        if self.y >= 1:
            left = self.grid[self.x][self.y-1]
        if self.y < 19:
            right = self.grid[self.x][self.y+1]
        if above != None:
            if above['Wumpus'] == True or above['Pit'] == True:
                safe_moves[0] = 1
            elif above['Breeze_Adjacent'] > 0 or above['Stench_Adjacent'] > 0:
                safe_moves[0] = 2
        if below != None:
            if below['Wumpus'] == True or below['Pit'] == True:
                safe_moves[1] = 1
            elif below['Breeze_Adjacent'] > 0 or below['Stench_Adjacent'] > 0:
                safe_moves[1] = 2
        if left != None:
            if left['Wumpus'] == True or left['Pit'] == True:
                safe_moves[2] = 1
            elif left['Breeze_Adjacent'] > 0 or left['Stench_Adjacent'] > 0:
                safe_moves[2] = 2
        if right != None:
            if right['Wumpus'] == True or right['Pit'] == True:
                safe_moves[3] = 1
            elif right['Breeze_Adjacent'] > 0 or right['Stench_Adjacent'] > 0:
                safe_moves[3] = 2
        num_safe_moves = 0
        for entry in safe_moves:
            if entry == 0:
                num_safe_moves = num_safe_moves + 1
        if num_safe_moves == 1: # Only one option - Take it whether visited or not
            move_index = safe_moves.index(0)
            if move_index == 0: # Want direction to be UP
                if self.direction == UP: # Move Forward
                    return 'forward'
                elif self.direction == RIGHT: # Want to turn Left
                    return 'left'
                elif self.direction == LEFT: # Want to turn right
                    return 'right'
                elif self.direction == DOWN: # Need to make two turns
                    return 'right'
            elif move_index == 1: # Want direction to be DOWN
                if self.direction == DOWN: # Move Forward
                    return 'forward'
                elif self.direction == RIGHT: # Turn Right
                    return 'right'
                elif self.direction == LEFT: # Turn Left
                    return 'left'
                elif self.direction == UP: # Need to make two turns
                    return 'right'
            elif move_index == 2:   # Want direction to be LEFT
                if self.direction == LEFT: # Move Forward
                    return 'forward'
                elif self.direction == RIGHT: # Need to make two turns
                    return 'left'
                elif self.direction == UP: # Need to turn left
                    return 'left'
                elif self.direction == DOWN: # Need to turn right
                    return 'right'
            elif move_index == 3:   # Want direction to be RIGHT
                if self.direction == RIGHT: # Move Forward
                    return 'forward'
                elif self.direction == UP: # Turn right
                    return 'right'
                elif self.direction == DOWN: # Turn left
                    return 'left'
                elif self.direction == LEFT: # Need to make two turns
                    return 'right'
        elif num_safe_moves > 1:  # Find a safe move not visited yet
            if above != None and safe_moves[0] == 0:
                if above['Visited'] == True:
                    safe_moves[0] = 3
            if below != None and safe_moves[1] == 0:
                if below['Visited'] == True:
                    safe_moves[1] = 3
            if left != None and safe_moves[2] == 0:
                if left['Visited'] == True:
                    safe_moves[2] = 3
            if right != None and safe_moves[3] == 0:
                if right['Visited'] == True:
                    safe_moves[3] = 3
        elif num_safe_moves == 0:   # No Safe moves, go forward if possible, else random direction
        num_safe_moves = 0
        for entry in safe_moves:
            if entry == 0:
                num_safe_moves = num_safe_moves + 1
        if num_safe_moves == 1:
            move_index = safe_moves.index(0)
            if move_index == 0:  # Want direction to be UP
                if self.direction == UP:  # Move Forward
                    return 'forward'
                elif self.direction == RIGHT:  # Want to turn Left
                    return 'left'
                elif self.direction == LEFT:  # Want to turn right
                    return 'right'
                elif self.direction == DOWN:  # Need to make two turns
                    return 'right'
            elif move_index == 1:  # Want direction to be DOWN
                if self.direction == DOWN:  # Move Forward
                    return 'forward'
                elif self.direction == RIGHT:  # Turn Right
                    return 'right'
                elif self.direction == LEFT:  # Turn Left
                    return 'left'
                elif self.direction == UP:  # Need to make two turns
                    return 'right'
            elif move_index == 2:  # Want direction to be LEFT
                if self.direction == LEFT:  # Move Forward
                    return 'forward'
                elif self.direction == RIGHT:  # Need to make two turns
                    return 'left'
                elif self.direction == UP:  # Need to turn left
                    return 'left'
                elif self.direction == DOWN:  # Need to turn right
                    return 'right'
            elif move_index == 3:  # Want direction to be RIGHT
                if self.direction == RIGHT:  # Move Forward
                    return 'forward'
                elif self.direction == UP:  # Turn right
                    return 'right'
                elif self.direction == DOWN:  # Turn left
                    return 'left'
                elif self.direction == LEFT:  # Need to make two turns
                    return 'right'
        elif num_safe_moves > 1:    # go forward if safe, else pick least directio moves needed direction to move
            if self.direction == UP and safe_moves[0] == 0:
                return 'forward'
            elif self.direction == DOWN and safe_moves[1] == 0:
                return 'forward'
            elif self.direction == LEFT and safe_moves[2] == 0:
                return 'forward'
            elif self.direction == RIGHT and safe_moves[3] == 0:
                return 'forward'
            elif self.direction == UP:
                if safe_moves[2] == 0:
                    return 'left'
                else:
                    return 'right'
            elif self.direction == DOWN:
                if safe_moves[2] == 0:
                    return 'right'
                else:
                    return 'left'
            elif self.direction == LEFT:
                if safe_moves[0] == 0:
                    return 'right'
                else:
                    return 'left'
            elif self.direction == RIGHT:
                if safe_moves[0] == 0:
                    return 'left'
                else:
                    return 'right'
        elif num_safe_moves == 0:   # No Safe moves, select a random visited location/direction
            if self.direction == UP and safe_moves[0] == 3:
                return 'forward'
            elif self.direction == DOWN and safe_moves[1] == 3:
                return 'forward'
            elif self.direction == LEFT and safe_moves[2] == 3:
                return 'forward'
            elif self.direction == RIGHT and safe_moves[3] == 3:
                return 'forward'
            else:
                return 'right'


















    def makeMove(self, move):
        if move == "forward":
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
            pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_UP))
        elif move == "left":
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
            pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_LEFT))
        elif move == "right":
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
        self.hasStench = False
        self.hasBreeze = False
        self.hasWumpus = False
        self.hasPit = False
        self.hasGold = False
        self.tilesVisited = []
        # self.hasAgent = False

    def draw(self):
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


class Grid:
    def __init__(self, width, height):
        self.tiles = []
        for w in range(width):
            self.tiles.append([])
            for h in range(height):
                self.tiles[w].append(Tile(w, h))

    def draw(self):
        for row in self.tiles:
            for tile in row:
                tile.draw()


if __name__ == '__main__':
    main()