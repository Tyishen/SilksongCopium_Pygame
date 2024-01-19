import pygame
import sys
import numpy

windowHeight = 900
windowWidth = 900

unitHeight = 10

viewTransform = pygame.Vector3(10, 0, 0);

def drawWorld():
    gameDisplay.fill((255, 255, 255))

    for y, row in enumerate(mapData):
        for x, tile in enumerate(row):
            if tile == True:
                gameDisplay.blit(debugBlock, objectViewTransform(pygame.Vector3(x, y, 0), debugBlock))

    pygame.draw.circle(gameDisplay, "blue", worldViewport(playerCoords, pygame.Vector3(20, 20, 0)), 10)

    outputScreen.blit(pygame.transform.scale(gameDisplay, outputScreen.get_size()), (0, 0))
    
def objectViewTransform(inputCoords, inputObj):
    return worldViewport(inputCoords, pygame.Vector2(inputObj.get_width(), inputObj.get_height()))

def worldViewport(inputCoords, scaling):
    offsetCoords = inputCoords + viewTransform

    spriteW = scaling.x
    spriteH = scaling.y

    iChat = pygame.Vector2(0.5 * spriteW, 0.25 * spriteH)
    jChat = pygame.Vector2(-0.5 * spriteW, 0.25 * spriteH)

    isometricCoordinates = pygame.Vector2(iChat * offsetCoords.x) + (jChat * offsetCoords.y)
    # isometricCoordinates.y += 32 * inputCoords.z
    return isometricCoordinates
    
def viewportWorld(inputCoords):

    inputCoords

    iChat = pygame.Vector2(0.5 * 32, 0.25 * 32)
    jChat = pygame.Vector2(-0.5 * 32, 0.25 * 32)

    returnCoords = (pygame.Vector2(jChat.y, -(iChat.y)) * pygame.Vector2(-(jChat.x), iChat.x))
    return returnCoords

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
        playerCoords.y -= 2 * dt
    if keyDown[pygame.K_a]:
        playerCoords.x -= 2 * dt
    if keyDown[pygame.K_s]:
        playerCoords.y += 2 * dt
    if keyDown[pygame.K_d]:
        playerCoords.x += 2 * dt
    
    if keyDown[pygame.K_RIGHT]:
        viewTransform.x += 5 * dt
    if keyDown[pygame.K_LEFT]:
        viewTransform.x -= 5 * dt
    if keyDown[pygame.K_UP]:
        viewTransform.y += 5 * dt
    if keyDown[pygame.K_DOWN]:
        viewTransform.y -= 5 * dt
        
    dt = clock.tick(60)/1000

    # flip() the display to put your work on screen
    drawWorld() 
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
pygame.quit()
sys.exit()
