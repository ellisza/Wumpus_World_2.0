# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys,math
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
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
RED          = (255,   0,   0)
GREEN        = (  0, 255,   0)
DARKGREEN    = (  0, 155,   0)
LIGHTBLUE    = (193, 225, 236)
DARKGRAY     = ( 40,  40,  40)
YELLOW       = (255, 255,   0)
LAKER_PURPLE = (85,   37, 130)
LAKER_GOLD   = (253, 185,  39)
LAKER_BLACK  = (6,    25,  34)
BGCOLOR = WHITE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.SysFont('sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheadingbolditalicsitkadisplaybolditalicsitkabannerbolditalic', 18)
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
    # agentCoord1 = {'x': startx1, 'y': starty1}
    # agentCoord2 = {'x': startx2, 'y': starty2}
    # agentCoord3 = {'x': startx3, 'y': starty3}
    # direction1 = UP
    # direction2 = RIGHT
    # direction3 = DOWN

    agentCoord1 = Agent(startx1, starty1, UP)
    agentCoord2 = Agent(startx2, starty2, RIGHT)
    agentCoord3 = Agent(startx3, starty3, DOWN)

    previous_locations1 = []
    previous_locations2 = []
    previous_locations3 = []
    while True: # main game loop
        previous_locations1.append(agentCoord1)
        previous_locations2.append(agentCoord2)
        previous_locations3.append(agentCoord3)
        

        event =  pygame.event.wait() # event handling loop
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                terminate()
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
        
        #check if gold is in same tile as agent
        if mainGrid.tiles[agentCoord1.x][agentCoord1.y].hasGold:
            mainGrid.tiles[agentCoord1.x][agentCoord1.y].hasGold = False
            agentCoord1.hasGold = True

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
        if idx in used or possible_locations[idx] == [0, 19] or possible_locations[idx] == [0, 0] or possible_locations[idx] == [19, 0]:
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
    titleFont = pygame.font.SysFont('sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheadingbolditalicsitkadisplaybolditalicsitkabannerbolditalic', 100)
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
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def showGameOverScreen():
    gameOverFont = pygame.font.SysFont('sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheadingbolditalicsitkadisplaybolditalicsitkabannerbolditalic', 150)
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
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
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
    ycenter = agentCoord['y'] * CELLSIZE+ math.floor(CELLSIZE / 2)
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
    agentDeadFont = pygame.font.SysFont('sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheadingbolditalicsitkadisplaybolditalicsitkabannerbolditalic', 10)
    x = agentCoord['x'] * CELLSIZE
    y = agentCoord['y'] * CELLSIZE
    xcenter = agentCoord['x'] * CELLSIZE + math.floor(CELLSIZE / 2)
    ycenter = agentCoord['y'] * CELLSIZE+ math.floor(CELLSIZE / 2)
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
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
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