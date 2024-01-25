
import pygame
import sys
import numpy
import random

def drawWorld():
    global blockTileList

    gameDisplay.fill((255, 255, 255))
    playerDisplay.fill((255, 255, 255))

    offsetVector = pygame.Vector2.normalize(pygame.Vector2(0.5, -0.5)) * 0.5

    playerTile = tileCoords(playerCoords - pygame.Vector3(offsetVector.x, offsetVector.y, 0))
    sortingList = []

    tempList = []

    for y, row in enumerate(mapData):
        for x, tile in enumerate(row):
            if tile == True:
                sortingList.append(pygame.Vector3(x, y + 1, 0))
                blockTileList.append(pygame.Vector3(x, y + 1, 0))
                blockTileList.append(randomizeBocks())

    for i in range(len(sortingList)):

        if sortingList[i].x <= playerTile.x + 1 and sortingList[i].y <= playerTile.y + 1:
            BlockCheck1 = sortingList[i].x == playerTile.x + 1 and sortingList[i].y == playerTile.y + 1
            
            if playerCoords.z < 0 and BlockCheck1:
                tempList.append(sortingList[i])
                tempList.append(sortingList[i])
            gameDisplay.blit(tileBlock(sortingList[i]), worldScreen(sortingList[i]))
        else:
            tempList.append(sortingList[i])
            tempList.append(sortingList[i])

    sortingList = tempList

    #Bliting le player
    gameDisplay.blit(kornetFrame(), worldScreen(playerCoords) - pygame.Vector2(10, 10))

    for i in range(len(tempList)):
        gameDisplay.blit(tileBlock(tempList[i]), worldScreen(tempList[i]))

    outputScreen.blit(pygame.transform.scale(gameDisplay, outputScreen.get_size()), (0, 0))

# Conversions from screen space to world space and vice versa

def worldScreen(inputCoords):
    offsetCoords = inputCoords + viewTransform

    iChat = pygame.Vector2(0.5 * tileX, 0.25 * tileY)
    jChat = pygame.Vector2(-0.5 * tileX, 0.25 * tileY)

    isometricCoordinates = pygame.Vector2(iChat * offsetCoords.x) + (jChat * offsetCoords.y)
    isometricCoordinates.y -= tileY * inputCoords.z
    return isometricCoordinates
    
def screenWorld(inputCoords):

    iChat = pygame.Vector2(0.5 * tileX, 0.25 * tileY)
    jChat = pygame.Vector2(-0.5 * tileX, 0.25 * tileY)

    returnCoords = pygame.Vector2(jChat.y, -(iChat.y)) * inputCoords.x + pygame.Vector2(-(jChat.x), iChat.x) * inputCoords.y
    return pygame.Vector3(returnCoords.x, returnCoords.y, 0)

def tileCoords(inputCoords):
    return pygame.Vector2(numpy.floor(inputCoords.x), numpy.floor(inputCoords.y))

def playerPhysicx():
    global playerCoords, dt

    gravity = 4.9

    tile = tileCoords(playerCoords)

    if tile.x < 0 or tile.y < 0 or tile.x > len(mapData) - 1  or tile.y > len(mapData) - 1:
        playerCoords.z -= gravity * dt
    else:
        if mapData[int(tile.y)][int(tile.x)] == 1:
            if playerCoords.z > 0.0001 or playerCoords.z < -0.5: # hackerman
                playerCoords.z -= gravity * dt
            else:
                playerCoords.z = 0.000001
        else:
            
            playerCoords.z -= gravity * dt

def kornetFrame():
    global currentTime, frame, lastUpd
    cornet = cornetIDLE
 
    if True in keyDown:
        currentTime = pygame.time.get_ticks()
        if currentTime - lastUpd >= animationTick:
            frame += 1
            lastUpd = currentTime
            if frame >= len(cornetAni):
                frame = 0

        cornet = cornetAni[frame]

    if playerCoords.z <= -0.5:
        cornet = cornetFALL

    if facing == "right":
        cornet = pygame.transform.flip(cornet, True, False)

    return cornet

def randomizeBocks():
    # tileBlock = random.choice([mossCobble, mossCobble2, mossCobble3, cobble])

    return random.choice([mossCobble, mossCobble2, mossCobble3, cobble])

def tileBlock(inputTile):
    
    for i in range(int(len(blockTileList) / 2)):
        if inputTile == blockTileList[i * 2]:
            return blockTileList[(i * 2) + 1]

pygame.init()
pygame.time.Clock()

# Begin the variables!

windowHeight = 900
windowWidth = 900

dt = 0

tileX = 32
tileY = 32

unitHeight = 10

viewTransform = pygame.Vector3(10, 0, 0);

outputScreen = pygame.display.set_mode((windowWidth, windowHeight))
gameDisplay = pygame.Surface((300, 300))
playerDisplay = pygame.Surface((300, 230))

clock = pygame.time.Clock()
dt = 0

# Objects
playerCoords = pygame.Vector3(5, 5, 3)
debugBlock = pygame.image.load("pixil-frame-2.png").convert_alpha()

mossCobble = pygame.image.load("mossCobble.png").convert_alpha()
mossCobble2 = pygame.image.load("mossCobble2.png").convert_alpha()
mossCobble3 = pygame.image.load("mossCobble3.png").convert_alpha()
cobble = pygame.image.load("cobble.png").convert_alpha()

blockTileList = []

# There's probably a faster way of getting all these.. oh well

cornetIDLE = pygame.image.load("Cornet Idle.png").convert_alpha()
cornetFALL = pygame.image.load("KornetFall.png").convert_alpha()
cornetATTACK = pygame.image.load("Kornet Walk 2.png").convert_alpha()

cornet1 = pygame.image.load("cornet1.png").convert_alpha()
cornet2 = pygame.image.load("Kornet Walk 1.png").convert_alpha()
cornet3 = pygame.image.load("Kornet Walk 3.png").convert_alpha()

cornetAni = [cornet1, cornet2, cornet3]

facing = "left"

frame = 0
lastUpd = pygame.time.get_ticks()
animationTick = 200
currentTime = pygame.time.get_ticks()

mapFile = open("solidMap.txt", "r")
mapData = []

i = 0
for row in mapFile.read().split("\n"):
    rowArray = []
    print(row)
    for char in row:
        rowArray.append(int(char))

    mapData.insert(i, rowArray)
    i += 1

running = True
while running:
    keyDown = pygame.key.get_pressed()

    # This is the movement code for non-isometric movement
    # if keyDown[pygame.K_w]:
    #     playerCoords -= screenWorld(pygame.Vector3(0, 0.2 * dt, 0))
    # if keyDown[pygame.K_a]:
    #     playerCoords -= screenWorld(pygame.Vector3(0.2 * dt, 0, 0))
    #     facing = "left"
    # if keyDown[pygame.K_s]:
    #     playerCoords += screenWorld(pygame.Vector3(0, 0.2 * dt, 0))
    # if keyDown[pygame.K_d]:
    #     playerCoords += screenWorld(pygame.Vector3(0.2 * dt, 0, 0))
    #     facing = "right"
    
    # This is the movement code for movement using the ingame grid system (isometric)

    if keyDown[pygame.K_w]:
        playerCoords.y -= 2 * dt
        facing = "right"
    if keyDown[pygame.K_a]:
        playerCoords.x -= 2 * dt
        facing = "left"
    if keyDown[pygame.K_s]:
        playerCoords.y += 2 * dt
        facing = "left"
    if keyDown[pygame.K_d]:
        playerCoords.x += 2 * dt
        facing = "right"

    if keyDown[pygame.K_RIGHT]:
        viewTransform -= screenWorld(pygame.Vector3(1 * dt, 0, 0))
    if keyDown[pygame.K_LEFT]:
        viewTransform += screenWorld(pygame.Vector3(1 * dt, 0, 0))
    if keyDown[pygame.K_UP]:
        viewTransform += screenWorld(pygame.Vector3(0, 1 * dt, 0))
    if keyDown[pygame.K_DOWN]:
        viewTransform -= screenWorld(pygame.Vector3(0, 1 * dt, 0))
        
    dt = clock.tick(60)/1000

    playerPhysicx()

    # flip() the display to put your work on screen
    drawWorld() 
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
pygame.quit()
sys.exit()
