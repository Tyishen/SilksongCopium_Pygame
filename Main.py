
import pygame
import sys
import numpy
import random

def drawWorld():
    global blockTileList, kornet

    gameDisplay.fill((255, 255, 255))

    offsetVector = pygame.Vector2.normalize(pygame.Vector2(0.5, -0.5)) * 0.5

    playerTile = tileCoords(kornet.coordinates - pygame.Vector3(offsetVector.x, offsetVector.y, 0))
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
            
            if kornet.coordinates.z < 0 and BlockCheck1:
                tempList.append(sortingList[i])
                tempList.append(sortingList[i])
            gameDisplay.blit(tileBlock(sortingList[i]), worldScreen(sortingList[i]))
        else:
            tempList.append(sortingList[i])
            tempList.append(sortingList[i])

    sortingList = tempList

    #Bliting le player
    kornet.updateFrame()
    kornet.draw()

    for i in range(len(tempList)):
        gameDisplay.blit(tileBlock(tempList[i]), worldScreen(tempList[i]))

    outputScreen.blit(pygame.transform.scale(gameDisplay, outputScreen.get_size()), (0, 0))

# Conversions from screen space to world space and vice versa

def worldScreen(inputCoords):
    offsetCoords = inputCoords - viewTransform  + screenWorld(pygame.Vector2(gameDisplay.get_width() / 2, gameDisplay.get_height() / 2))

    # print(pygame.Vector2(gameDisplay.get_width(), gameDisplay.get_height()))
    # print(screenWorld(pygame.Vector2(gameDisplay.get_width(), gameDisplay.get_height())))

    iChat = pygame.Vector2(0.5 * tileX, 0.25 * tileY)
    jChat = pygame.Vector2(-0.5 * tileX, 0.25 * tileY)

    isometricCoordinates = pygame.Vector2(iChat * offsetCoords.x) + (jChat * offsetCoords.y)
    isometricCoordinates.y -= tileY * inputCoords.z

    return isometricCoordinates

def screenWorld(inputCoords):
    iChat = pygame.Vector2(0.5 * tileX, 0.25 * tileY)
    jChat = pygame.Vector2(-0.5 * tileX, 0.25 * tileY)

    iChat_Inv = pygame.Vector2(jChat.y, -(iChat.y))
    jChat_Inv = pygame.Vector2(-(jChat.x), iChat.x)
                               

    determinant = (iChat_Inv.x*jChat_Inv.y) - (iChat_Inv.y*jChat_Inv.x)
    iChat_Inv /= determinant
    jChat_Inv /= determinant

    returnCoords = iChat_Inv * inputCoords.x + jChat_Inv * inputCoords.y
    return pygame.Vector3(returnCoords.x, returnCoords.y, 0)

def tileCoords(inputCoords):
    return pygame.Vector2(numpy.floor(inputCoords.x), numpy.floor(inputCoords.y))

# Player Movement

def playerPhysicx():
    global playerCoords, dt, cornetYVelo, cornetJump

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

def kornetFrame(player):
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

    if player.coordinates.z <= -0.5:
        cornet = cornetFALL

    if facing == "right":
        cornet = pygame.transform.flip(cornet, True, False)

    return cornet

# Randomizing the Map Look

def randomizeBocks():
    # tileBlock = random.choice([mossCobble, mossCobble2, mossCobble3, cobble])

    return random.choice([mossCobble, mossCobble2, mossCobble3, cobble])

def tileBlock(inputTile):
    
    for i in range(int(len(blockTileList) / 2)):
        if inputTile == blockTileList[i * 2]:
            return blockTileList[(i * 2) + 1]

# Ok we gonna try some object-oriented programming
class Hornet():

    def __init__(self, coords, speed, up, left, down, right, iso):
        self.coordinates = coords
        self.jumpState = "grounded"
        self.speed = speed
        self.pixelSpeed = worldScreen(pygame.Vector3(speed - 2, 0, 0)).length()

        self.facing = "left"
        self.isoMovement = iso
        self.frameNum = 0
        self.frame = cornetIDLE
        self.currentFrame = cornetIDLE
        self.lastUpdate = pygame.time.get_ticks()

        self.up = up
        self.left = left
        self.down = down
        self.right = right

    def draw(self):
        gameDisplay.blit(self.frame, worldScreen(self.coordinates) - pygame.Vector2(10, 10))

    def move(self):
        global keyDown

        if self.isoMovement == True:
         # This is the movement code for movement using the ingame grid system (isometric)
        
            if keyDown[self.up]:
                self.coordinates.y -= self.speed * dt
                self.facing = "right"
            if keyDown[self.left]:
                self.coordinates.x -= self.speed * dt
                self.facing = "left"
            if keyDown[self.down]:
                self.coordinates.y += self.speed * dt
                self.facing = "left"
            if keyDown[self.right]:
                self.coordinates.x += self.speed * dt
                self.facing = "right"
        else:
        # This is the movement code for non-isometric movement

            if keyDown[self.up]:
                self.coordinates -= screenWorld(pygame.Vector3(0, self.pixelSpeed * dt, 0))
            if keyDown[self.left]:
                self.coordinates -= screenWorld(pygame.Vector3(self.pixelSpeed * dt, 0, 0))
                self.facing = "left"
            if keyDown[self.down]:
                self.coordinates += screenWorld(pygame.Vector3(0, self.pixelSpeed * dt, 0))
            if keyDown[self.right]:
                self.coordinates += screenWorld(pygame.Vector3(self.pixelSpeed * dt, 0, 0))
                self.facing = "right"

    def physics(self):

        tile = tileCoords(self.coordinates)

        if tile.x < 0 or tile.y < 0 or tile.x > len(mapData) - 1  or tile.y > len(mapData) - 1:
            self.coordinates.z -= gravity * dt
        else:
            if mapData[int(tile.y)][int(tile.x)] == 1:
                if self.coordinates.z > 0.0001 or self.coordinates.z < -0.5: # hackerman
                    self.coordinates.z -= gravity * dt
                else:
                    self.coordinates.z = 0.000001
            else:
                
                self.coordinates.z -= gravity * dt
            
        if self.coordinates.z <= -5:
            self.coordinates = pygame.Vector3(5, 5, 2)

    def updateFrame(self):
        global currentTime, animationTick
        
        currentTime = pygame.time.get_ticks()

        if keyDown[self.up] or keyDown[self.left] or keyDown[self.down] or keyDown[self.right]:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.lastUpdate >= animationTick:
                self.frameNum += 1
                self.lastUpdate = currentTime
                if self.frameNum >= len(cornetAni):
                    self.frameNum = 0
                
                self.frame = cornetAni[self.frameNum]
                self.currentFrame = cornetAni[self.frameNum] # seems useless but it helps fix a visual issue with flipping
        
        if self.jumpState == "takeoff":
            self.frame = cornetATTACK

        if self.jumpState == "airborne":
            self.frame = cornetFALL

        if self.facing == "right":
                self.frame = pygame.transform.flip(self.currentFrame, True, False)
                # self.frame = pygame.transform.flip(self.frame, True, False)\
        else:
            self.frame = self.currentFrame
                    
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

clock = pygame.time.Clock()
dt = 0

# Objects, moving most of this to class
# playerCoords = pygame.Vector3(4.5, 4.5, 3)
# isometricMovement = True
# movementSpeed = 3
# pixelMovement = worldScreen(pygame.Vector3(2, 0, 0)).length()
gravity = 4.9

debugBlock = pygame.image.load("pixil-frame-2.png").convert_alpha()

mossCobble = pygame.image.load("mossCobble.png").convert_alpha()
mossCobble2 = pygame.image.load("mossCobble2.png").convert_alpha()
mossCobble3 = pygame.image.load("mossCobble3.png").convert_alpha()
cobble = pygame.image.load("cobble.png").convert_alpha()

blockTileList = []

# There's probably a faster way of getting all these.. oh well
# Probably should've consolidated this all into a spritesheet but idk how

cornetIDLE = pygame.image.load("Cornet Idle.png").convert_alpha()
cornetFALL = pygame.image.load("KornetFall.png").convert_alpha()
cornetATTACK = pygame.image.load("Kornet Walk 2.png").convert_alpha()

cornet1 = pygame.image.load("cornet1.png").convert_alpha()
cornet2 = pygame.image.load("Kornet Walk 1.png").convert_alpha()
cornet3 = pygame.image.load("Kornet Walk 3.png").convert_alpha()
cornet4 = pygame.image.load("Kornet Walk 4.png").convert_alpha()

cornetAni = [cornet1, cornet2, cornet4, cornet3]

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

kornet = Hornet(pygame.Vector3(4.5, 4.5, 3), 3, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, False)
# One player while I figure out how the layering works
# cornet = Hornet(pygame.Vector3(5, 5, 3), 3, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, False)

running = True
while running:
    keyDown = pygame.key.get_pressed()

    kornet.move()

    # Original camera movement code, now it's centered on the player
    # if keyDown[pygame.K_RIGHT]:
    #     viewTransform -= screenWorld(pygame.Vector3(1 * dt, 0, 0))
    # if keyDown[pygame.K_LEFT]:
    #     viewTransform += screenWorld(pygame.Vector3(1 * dt, 0, 0))
    # if keyDown[pygame.K_UP]:
    #     viewTransform += screenWorld(pygame.Vector3(0, 1 * dt, 0))
    # if keyDown[pygame.K_DOWN]:
    #     viewTransform -= screenWorld(pygame.Vector3(0, 1 * dt, 0))
        
    viewTransform = kornet.coordinates

    dt = clock.tick(60)/1000

    kornet.physics()
    #playerPhysicx()

    # flip() the display to put your work on screen
    drawWorld() 
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
pygame.quit()
sys.exit()
