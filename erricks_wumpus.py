# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys,math
from pygame.locals import *

FPS = 5
WINDOWWIDTH = 500
WINDOWHEIGHT = 500
CELLSIZE = 100
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
    mainGrid = Grid(5, 5)
    mapElements = getRandomLocations(5)

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

    # Set start point for agent
    startx = 0
    starty = 4
    agentCoord = {'x': startx, 'y': starty}
    direction = RIGHT

    # Start the wumpus, pits, and gold in a random place.
    # wumpusCoord = getRandomLocation()
    # goldCoord = getRandomLocation()
    
    # pitCoords = []
    # breezeCoords = []
    # stenchCoords = []
    
    # pitCoords.append(getRandomLocation())
    # pitCoords.append(getRandomLocation())
    # pitCoords.append(getRandomLocation())
    
    # while (goldCoord['x'] == wumpusCoord['x']) and (goldCoord['y'] == wumpusCoord['y']):
    #     goldCoord = getRandomLocation()

    # while (pitCoords[0]['x'] == goldCoord['x']) and (pitCoords[0]['y'] == goldCoord['y'])\
    #     or (pitCoords[0]['x'] == wumpusCoord['x']) and (pitCoords[0]['y'] == wumpusCoord['y']):
    #     pitCoords[0] = getRandomLocation()

    # while (pitCoords[1]['x'] == pitCoords[0]['x']) and (pitCoords[1]['y'] == pitCoords[0]['y'])\
    #     or (pitCoords[1]['x'] == goldCoord['x']) and (pitCoords[1]['y'] == goldCoord['y'])\
    #     or (pitCoords[1]['x'] == wumpusCoord['x']) and (pitCoords[1]['y'] == wumpusCoord['y']):
    #     pitCoords[1] = getRandomLocation()

    # while (pitCoords[2]['x'] == pitCoords[1]['x']) and (pitCoords[2]['y'] == pitCoords[1]['y'])\
    #     or (pitCoords[2]['x'] == pitCoords[0]['x']) and (pitCoords[2]['y'] == pitCoords[0]['y'])\
    #     or (pitCoords[2]['x'] == goldCoord['x']) and (pitCoords[2]['y'] == goldCoord['y'])\
    #     or (pitCoords[2]['x'] == wumpusCoord['x']) and (pitCoords[2]['y'] == wumpusCoord['y']):
    #     pitCoords[2] = getRandomLocation()
    
    # for coords in pitCoords:
    #     breezeCoords.append({'x': coords['x'], 'y': coords['y'] - 1})
    #     breezeCoords.append({'x': coords['x'], 'y': coords['y'] + 1})
    #     breezeCoords.append({'x': coords['x'] - 1, 'y': coords['y']})
    #     breezeCoords.append({'x': coords['x'] + 1, 'y': coords['y']})

    # stenchCoords.append({'x': wumpusCoord['x'], 'y': wumpusCoord['y'] - 1})
    # stenchCoords.append({'x': wumpusCoord['x'], 'y': wumpusCoord['y'] + 1})
    # stenchCoords.append({'x': wumpusCoord['x'] - 1, 'y': wumpusCoord['y']})
    # stenchCoords.append({'x': wumpusCoord['x'] + 1, 'y': wumpusCoord['y']})

    # while True: # main game loop
    #     for event in pygame.event.get(): # event handling loop
    #         if event.type == QUIT:
    #             terminate()
    #         elif event.type == KEYDOWN:
    #             if event.key == K_ESCAPE:
    #                 terminate()
    #             else:
    #                 return
    previous_locations = []
    while True: # main game loop
        previous_locations.append(agentCoord)
        if len(previous_locations) >= 5:
            previous_locations.pop(0)

        event =  pygame.event.wait() # event handling loop
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                terminate()
            elif event.key == K_DOWN:
                agentCoord = {'x': agentCoord['x'], 'y': min(agentCoord['y'] + 1, 4)}
            elif event.key == K_UP:
                agentCoord = {'x': agentCoord['x'], 'y': max(agentCoord['y'] - 1, 0)}
            elif event.key == K_LEFT:
                agentCoord = {'x': max(agentCoord['x'] - 1, 0), 'y': agentCoord['y']}
            elif event.key == K_RIGHT:
                agentCoord = {'x': min(agentCoord['x'] + 1, 4), 'y': agentCoord['y']}
            elif event.key == K_RETURN:
                pass
            else:
                print(event.key)
                return

            DISPLAYSURF.fill(WHITE)
            drawGrid()
            mainGrid.draw()
            drawAgent(agentCoord)
            # drawWumpus(wumpusCoord)
            # drawGold(goldCoord)
            # drawPit(pitCoords)
            # drawBreeze(breezeCoords)
            # drawStench(stenchCoords)
            agentCoord = moveAgent(agentCoord, [])
            pygame.display.update()
            FPSCLOCK.tick(FPS)

def getRandomLocations(num):
    possible_locations = []
    for i in range(5):
        for j in range(5):
            possible_locations.append([i, j])

    used = set()
    locations = []
    i = 0
    while i < num:
        idx = random.randint(1, len(possible_locations) - 1)
        if idx in used or possible_locations[idx] == [0, 4]:
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
        valid_moves.append({'x': x, 'y': y-1})
    if y + 1 < 5:
        valid_moves.append({'x': x, 'y': y+1})
    if x - 1 > 0:
        valid_moves.append({'x': x -  1, 'y': y})
    if x + 1 < 5:
        valid_moves.append({'x': x + 1, 'y': y})
    return valid_moves

def addStenches(coords, grid):
    x = coords[0]
    y = coords[1]
    if y - 1 >= 0:
        grid.tiles[x][y - 1].hasStench = True
    if y + 1 < 5:
         grid.tiles[x][y + 1].hasStench = True
    if x - 1 >= 0:
         grid.tiles[x - 1][y].hasStench = True
    if x + 1 < 5:
         grid.tiles[x + 1][y].hasStench = True


def addBreezes(coords, grid):
    x = coords[0]
    y = coords[1]
    if y - 1 >= 0:
        grid.tiles[x][y - 1].hasBreeze = True
    if y + 1 < 5:
         grid.tiles[x][y + 1].hasBreeze = True
    if x - 1 >= 0:
         grid.tiles[x - 1][y].hasBreeze = True
    if x + 1 < 5:
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
    titleSurf1 = titleFont.render('Errick\'s', True, LAKER_PURPLE, LAKER_BLACK)
    titleSurf2 = titleFont.render('Project 2', True, LAKER_GOLD)

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


def getRandomLocation():
    return {'x': random.randint(1, 4), 'y': random.randint(0, 3)}


def showGameOverScreen():
    gameOverFont = pygame.font.SysFont('sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheadingbolditalicsitkadisplaybolditalicsitkabannerbolditalic', 150)
    gameSurf = gameOverFont.render('Game', True, RED)
    overSurf = gameOverFont.render('Over', True, RED)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (math.floor(WINDOWWIDTH / 2), 10)
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

def drawAgent(agentCoord):
    x = agentCoord['x'] * CELLSIZE
    y = agentCoord['y'] * CELLSIZE
    xcenter = agentCoord['x'] * CELLSIZE + math.floor(CELLSIZE / 2)
    ycenter = agentCoord['y'] * CELLSIZE+ math.floor(CELLSIZE / 2)
    pygame.draw.circle(DISPLAYSURF, LAKER_BLACK, (xcenter, ycenter), RADIUS / 2)

def drawWumpus(wumpusCoord):
    x = wumpusCoord['x'] * CELLSIZE
    y = wumpusCoord['y'] * CELLSIZE
    wormInnerSegmentRect = pygame.Rect(x + 20, y + 20, CELLSIZE - 40, CELLSIZE - 40)
    pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormInnerSegmentRect)


def drawPit(coords):
    x = coords['x'] * CELLSIZE
    y = coords['y'] * CELLSIZE
    xcenter = coords['x'] * CELLSIZE + math.floor(CELLSIZE / 2)
    ycenter = coords['y'] * CELLSIZE + math.floor(CELLSIZE / 2)
    pygame.draw.circle(DISPLAYSURF, LAKER_PURPLE, (xcenter, ycenter), RADIUS)

def drawGold(goldCoord):
    x = goldCoord['x'] * CELLSIZE
    y = goldCoord['y'] * CELLSIZE
    pygame.draw.circle(DISPLAYSURF, LAKER_GOLD, (x + 11, y + 89), RADIUS / 5)

def drawBreeze(coords):
    x = coords['x'] * CELLSIZE
    y = coords['y'] * CELLSIZE
    pygame.draw.circle(DISPLAYSURF, LIGHTBLUE, (x + 89, y + 11), RADIUS / 5)

def drawStench(coords):
    x = coords['x'] * CELLSIZE
    y = coords['y'] * CELLSIZE
    pygame.draw.circle(DISPLAYSURF, GREEN, (x + 11, y + 11), RADIUS / 5)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hasStench = False
        self.hasBreeze = False
        self.hasWumpus = False
        self.hasPit = False
        self.hasGold = False

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