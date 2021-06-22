# Wumpus World

import math
import pygame
import random
import sys

from pygame.locals import *
from cave import Cave
from agent import Agent
from room import Room


directions = [[-1,0], [1,0], [0,1], [0,-1]]

FPS = 5
WINDOWWIDTH = 750
WINDOWHEIGHT = 750
CELLSIZE = 150
RADIUS = math.floor(CELLSIZE / 2.5)
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#Inner Grid: Each Cell will have an inner grid that will 

#             R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
YELLOW = (255, 255, 0)
ORANGE = (255,165,0)
BLUE = (0,0,205)
BGCOLOR = BLACK

gameDisplay = pygame.display.set_mode((CELLSIZE, CELLSIZE))

wumpusImage = pygame.image.load(r'wumpus.jpeg')
agentImage = pygame.image.load(r'agent.jpeg')
pitImage = pygame.image.load(r'pit.jpeg')
goldImage = pygame.image.load(r'gold.jpeg')
stenchImage = pygame.image.load(r'stench.jpeg')
breezeImage = pygame.image.load(r'breeze.jpeg')

wumpusImage = pygame.transform.scale(wumpusImage, (50, 50))
agentImage = pygame.transform.scale(agentImage, (50, 50))
pitImage = pygame.transform.scale(pitImage, (50, 50))
goldImage = pygame.transform.scale(goldImage, (50, 50))
stenchImage = pygame.transform.scale(stenchImage, (50, 50))
breezeImage = pygame.transform.scale(breezeImage, (50, 50))


UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

CAVE = None

HEAD = 0  # syntactic sugar: index of the worm's head


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wumpus World')

    showStartScreen()
    while True:
        runGame()
        CAVE = Cave()
        CAVE.setup()
        showGameOverScreen()


def runGame():
    # Set a start point.
    agentCoords = [{'x': 0, 'y': 0}]
    direction = RIGHT

    # Start the pits in a random place.
    pitCoords = []
    pitCoords1 = getRandomPitLocation(pitCoords)
    pitCoords.append(pitCoords1)

    pitCoords2 = getRandomPitLocation(pitCoords)
    pitCoords.append(pitCoords2)

    pitCoords3 = getRandomPitLocation(pitCoords)
    pitCoords.append(pitCoords3)

    # Start the Gold in a random place.
    goldCoords = []
    gold = getRandomGoldLocation(pitCoords)
    goldCoords.append(gold)

    # Start the Wumpus in a random place.
    wumpusCoords = []
    wumpus = getRandomWumpusLocation(pitCoords, goldCoords)
    wumpusCoords.append(wumpus)

    # Shine Coords for Gold
    shineCoords = goldCoords

    # Get Breeze Coords
    breezeCoords = []
    for pit in pitCoords:
        x = pit['x']
        y = pit['y']
        for di in directions:
            xD = x + di[0]
            yD = y + di[1]

            if xD in range(0,5) and yD in range(0,5):
                breezeCoords.append({'x': xD, 'y': yD})

    # Get Stench Coords
    stenchCoords = []
    for wumpus in wumpusCoords:
        x = wumpus['x']
        y = wumpus['y']
        for di in directions:
            xD = x + di[0]
            yD = y + di[1]

            if xD in range(0,5) and yD in range(0,5):
                stenchCoords.append({'x': xD, 'y': yD})

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN) and direction != UP:
                    direction = DOWN
                elif (event.key == K_a) and direction2 != RIGHT:
                    direction2 = LEFT
                elif (event.key == K_d) and direction2 != LEFT:
                    direction2 = RIGHT
                elif (event.key == K_w) and direction2 != DOWN:
                    direction2 = UP
                elif (event.key == K_s) and direction2 != UP:
                    direction2 = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
        
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()

        wumpus_coords = CAVE.get_all_wumpus_coords()
        treasure_coords = CAVE.get_all_treasure_coords()
        pit_coords = CAVE.get_all_pit_coords()
        stench_coords = CAVE.get_all_stench_coords()
        breeze_coords = CAVE.get_all_breeze_coords()
        agent_coords = CAVE.get_all_agent_coords()

        drawWumpus(wumpus_coords)
        drawAgent(agent_coords)
        drawPit(pit_coords)
        drawGold(treasure_coords)
        drawStench(stench_coords)
        drawBreeze(breeze_coords)
            
        #drawWumpus(wumpusCoords)
        #drawAgent(agentCoords, direction)
        #drawPit(pitCoords)
        #drawGold(goldCoords)
        #drawStench(stenchCoords)
        #drawBreeze(breezeCoords)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to watch your Agent play.', True, YELLOW)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 400, WINDOWHEIGHT - 30)
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
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('World', True, WHITE, ORANGE)
    titleSurf2 = titleFont.render('Wumpus', True, BLUE)

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


def getRandomPitLocation(pitCoords):
    loc = {'x': 0, 'y': 0}
    while loc == {'x': 0, 'y': 0} or loc in pitCoords:
        loc = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
    return loc

def getRandomGoldLocation(pitCoords):
    loc = {'x': 0, 'y': 0}
    while loc == {'x': 0, 'y': 0} or loc in pitCoords:
        loc = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
    return loc

def getRandomWumpusLocation(pitCoords, goldCoords):
    loc = {'x': 0, 'y': 0}
    while loc == {'x': 0, 'y': 0} or loc in goldCoords or loc in pitCoords :
        loc = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
    return loc

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (math.floor(WINDOWWIDTH / 2), 10)
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
    scoreSurf = BASICFONT.render('P1 Score: %s' % (score), True, GREEN)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (10, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawGold(goldCoords):
    for coord in goldCoords:
        x = coord['x'] * CELLSIZE + 100
        y = coord['y'] * CELLSIZE
        gameDisplay.blit(goldImage, (x,y))

def drawWumpus(wumpusCoords):
    for coord in wumpusCoords:
        x = coord['x'] * CELLSIZE + 50
        y = coord['y'] * CELLSIZE
        gameDisplay.blit(wumpusImage, (x,y))

def drawStench(stenchCoords):
    for coord in stenchCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE + 50
    
        gameDisplay.blit(stenchImage, (x,y))

def drawBreeze(breezeCoords):
    for coord in breezeCoords:
        x = coord['x'] * CELLSIZE+ 100
        y = coord['y'] * CELLSIZE + 50
    
        gameDisplay.blit(breezeImage, (x,y))

def drawPit(pitCoords):
    for coord in pitCoords:
        x = coord['x'] * CELLSIZE + 50
        y = coord['y'] * CELLSIZE + 50
        gameDisplay.blit(pitImage, (x,y))


def drawAgent(agentCoords, direction):
    for coord in agentCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        # xcenter = coord['x'] * CELLSIZE + math.floor(CELLSIZE / 2)
        # ycenter = coord['y'] * CELLSIZE + math.floor(CELLSIZE / 2)
        if direction == 'right':
            gameDisplay.blit(pygame.transform.rotate(agentImage, 90), (x,y))
        elif direction == 'left':
            gameDisplay.blit(pygame.transform.rotate(agentImage, -90), (x,y))
        elif direction == 'up':
            gameDisplay.blit(pygame.transform.rotate(agentImage, 180), (x,y))
        else:
            gameDisplay.blit(agentImage, (x,y))

def drawGrid():

    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
