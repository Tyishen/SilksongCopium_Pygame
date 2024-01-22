import pygame
import sys
import numpy

windowHeight = 900
windowWidth = 900

tileX = 32
tileY = 32

unitHeight = 10

viewTransform = pygame.Vector3(10, 0, 0);

def drawWorld():
    gameDisplay.fill((255, 255, 255))

    for y, row in enumerate(mapData):
        for x, tile in enumerate(row):
            if tile == True:
                gameDisplay.blit(debugBlock, worldScreen(pygame.Vector3(x, y, 0)))

    pygame.draw.circle(gameDisplay, "blue", worldScreen(playerCoords), 10)

    outputScreen.blit(pygame.transform.scale(gameDisplay, outputScreen.get_size()), (0, 0))

def worldScreen(inputCoords):
    offsetCoords = inputCoords + viewTransform

    iChat = pygame.Vector2(0.5 * tileX, 0.25 * tileY)
    jChat = pygame.Vector2(-0.5 * tileX, 0.25 * tileY)

    isometricCoordinates = pygame.Vector2(iChat * offsetCoords.x) + (jChat * offsetCoords.y)
    # isometricCoordinates.y += 32 * inputCoords.z
    return isometricCoordinates
    
def screenWorld(inputCoords):

    iChat = pygame.Vector2(0.5 * tileX, 0.25 * tileY)
    jChat = pygame.Vector2(-0.5 * tileX, 0.25 * tileY)

    returnCoords = pygame.Vector2(jChat.y, -(iChat.y)) * inputCoords.x + pygame.Vector2(-(jChat.x), iChat.x) * inputCoords.y
    return pygame.Vector3(returnCoords.x, returnCoords.y, 0)

def tileCoords(inputCoords):
    return pygame.Vector2(numpy.floor(inputCoords.x), numpy.floor(inputCoords.y))

def playerOpticsYay():
    global playerCoords

    tile = tileCoords(playerCoords)

    if mapData[tile.x][tile.y] == 1:
        return True
    else:
        return False

# 1 / ((iChat.x * jChat.y) - (jChat.x * iChat.y))) this is the determinant??

# def viewportWorld(inputCoords, spriteW, spriteH):
#     iChat = pygame.Vector2(0.5 * spriteW, 0.25 * spriteH)
#     jChat = pygame.Vector2(-0.5 * spriteW, 0.25 * spriteH)

#     returnCoords = (1 / ((iChat.x * jChat.y) - (jChat.x * iChat.y))) * (pygame.Vector2(jChat.y, -(iChat.y)) * pygame.Vector2(-(jChat.x), iChat.x))




pygame.init()
outputScreen = pygame.display.set_mode((windowWidth, windowHeight))
gameDisplay = pygame.Surface((300, 300))

clock = pygame.time.Clock()
dt = 0

# Objects
playerCoords = pygame.Vector3(0, 0, 0)
debugBlock = pygame.image.load("pixil-frame-2.png").convert_alpha()

mapFile = open("map.txt", "r")
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
    
    if keyDown[pygame.K_w]:
        playerCoords -= screenWorld(pygame.Vector3(0, 1 * dt, 0))
    if keyDown[pygame.K_a]:
        playerCoords -= screenWorld(pygame.Vector3(1 * dt, 0, 0))
    if keyDown[pygame.K_s]:
        playerCoords += screenWorld(pygame.Vector3(0, 1 * dt, 0))
    if keyDown[pygame.K_d]:
        playerCoords += screenWorld(pygame.Vector3(1 * dt, 0, 0))
    
    if keyDown[pygame.K_RIGHT]:
        viewTransform -= screenWorld(pygame.Vector3(1 * dt, 0, 0))
    if keyDown[pygame.K_LEFT]:
        viewTransform += screenWorld(pygame.Vector3(1 * dt, 0, 0))
    if keyDown[pygame.K_UP]:
        viewTransform += screenWorld(pygame.Vector3(0, 1 * dt, 0))
    if keyDown[pygame.K_DOWN]:
        viewTransform -= screenWorld(pygame.Vector3(0, 1 * dt, 0))
        
    dt = clock.tick(60)/1000

    # flip() the display to put your work on screen
    drawWorld() 
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
pygame.quit()
sys.exit()
