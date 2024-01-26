
import pygame
import sys
import numpy
import random

def drawWorld():
    global blockTileList, kornet

    gameDisplay.fill((255, 255, 255))
    gameDisplay.blit(backgroundImg, (0, 0))

    offsetVector = pygame.Vector2.normalize(pygame.Vector2(0.5, -0.5)) * 0.5

    playerTile = tileCoords(kornet.coordinates - pygame.Vector3(offsetVector.x, offsetVector.y, 0))
    sortingList = []

    tempList = []

    # tile coords from the map file.
    for y, row in enumerate(mapData):
        for x, tile in enumerate(row):
            if tile == 1:
                sortingList.append(pygame.Vector3(x, y + 1, 0))
                blockTileList.append(pygame.Vector3(x, y + 1, 0))
                blockTileList.append(randomizeBocks())

    # layering blocks in such a way that some are behind and some are in front of the player
    # Mostly matters when the player falls in holes in the map

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
    kornet.playerSounds()

    for i in range(len(tempList)):
        gameDisplay.blit(tileBlock(tempList[i]), worldScreen(tempList[i]))

    kornet.attack() # attack and swing will end up on top of everything no matter what but it's barely an issue
    kornet.drawSwing()

    outputScreen.blit(pygame.transform.scale(gameDisplay, outputScreen.get_size()), (0, 0))

# Conversions from screen space (x, y) to world space (x, y, z) and vice versa

def worldScreen(inputCoords):
    offsetCoords = inputCoords - viewTransform  + screenWorld(pygame.Vector2(gameDisplay.get_width() / 2, gameDisplay.get_height() / 2))

    # print(pygame.Vector2(gameDisplay.get_width(), gameDisplay.get_height()))
    # print(screenWorld(pygame.Vector2(gameDisplay.get_width(), gameDisplay.get_height())))

    iChat = pygame.Vector2(0.5 * tileX, 0.25 * tileY)
    jChat = pygame.Vector2(-0.5 * tileX, 0.25 * tileY)

    # We love matrix math!

    isometricCoordinates = pygame.Vector2(iChat * offsetCoords.x) + (jChat * offsetCoords.y)
    isometricCoordinates.y -= tileY * inputCoords.z

    return isometricCoordinates

def screenWorld(inputCoords):
    iChat = pygame.Vector2(0.5 * tileX, 0.25 * tileY)
    jChat = pygame.Vector2(-0.5 * tileX, 0.25 * tileY)

    iChat_Inv = pygame.Vector2(jChat.y, -(iChat.y))
    jChat_Inv = pygame.Vector2(-(jChat.x), iChat.x)

    # woah, inverse matrix math          

    determinant = (iChat_Inv.x*jChat_Inv.y) - (iChat_Inv.y*jChat_Inv.x)
    iChat_Inv /= determinant
    jChat_Inv /= determinant

    returnCoords = iChat_Inv * inputCoords.x + jChat_Inv * inputCoords.y
    return pygame.Vector3(returnCoords.x, returnCoords.y, 0)

# Determines which tile the player is on (technically a completely seperate system)
def tileCoords(inputCoords):
    return pygame.Vector2(numpy.floor(inputCoords.x), numpy.floor(inputCoords.y))

# Player Movement 

"""
All movement functions moved inside of the Hornet class


# def playerPhysicx():
#     global playerCoords, dt, cornetYVelo, cornetJump

#     gravity = 4.9

#     tile = tileCoords(playerCoords)

#     if tile.x < 0 or tile.y < 0 or tile.x > len(mapData) - 1  or tile.y > len(mapData) - 1:
#         playerCoords.z -= gravity * dt
#     else:
#         if mapData[int(tile.y)][int(tile.x)] == 1:
#             if playerCoords.z > 0.0001 or playerCoords.z < -0.5: # hackerman
#                 playerCoords.z -= gravity * dt
#             else:
#                 playerCoords.z = 0.000001
#         else:
            
#             playerCoords.z -= gravity * dt

# def kornetFrame(player):
#     global currentTime, frame, lastUpd
#     cornet = cornetIDLE
 
#     if True in keyDown:
#         currentTime = pygame.time.get_ticks()
#         if currentTime - lastUpd >= animationTick:
#             frame += 1
#             lastUpd = currentTime
#             if frame >= len(cornetAni):
#                 frame = 0

#         cornet = cornetAni[frame]

#     if player.coordinates.z <= -0.5:
#         cornet = cornetFALL

#     if facing == "right":
#         cornet = pygame.transform.flip(cornet, True, False)

#     return cornet

"""

# Randomizing the Map Look

def randomizeBocks(): # randomizing the look of the ground
    return random.choice([mossCobble, mossCobble, mossCobble2, mossCobble2, mossCobble3, mossCobble3, mossCobble4, mossCobble5, mossCobble5, cobble, cobble2, cobble3])

def tileBlock(inputTile): # retrieving what type of ground each tile is between frames.
    
    for i in range(int(len(blockTileList) / 2)):
        if inputTile == blockTileList[i * 2]:
            return blockTileList[(i * 2) + 1]

def playSound(channel, sound):
    if channel.get_busy():
        return
    else:
        channel = sound.play()

# Ok we gonna try some object-oriented programming, first time!
class Hornet():

    def __init__(self, coords, speed, up, left, down, right, iso, attack, jump):
        self.coordinates = coords
        self.jumpState = "grounded"
        self.yVelocity = 0
        self.speed = speed
        self.pixelSpeed = worldScreen(pygame.Vector3(speed - 2, 0, 0)).length()

        self.facing = "left"
        self.isoMovement = iso
        self.frameNum = 0
        self.frame = cornetIDLE
        self.currentFrame = cornetIDLE
        self.lastUpdate = pygame.time.get_ticks()

        self.attacking = False
        self.attackFrameNum = 0
        self.attackFrame = attack1
        self.attackLastUpdate = pygame.time.get_ticks()
        self.currentAttackFrame = attack1

        # each player can get their own set of controls

        self.up = up
        self.left = left
        self.down = down
        self.right = right
        self.attackKey = attack
        self.jumpkey = jump

    def draw(self):
        gameDisplay.blit(self.frame, worldScreen(self.coordinates) - pygame.Vector2(10, 10))

    def drawSwing(self):
        if self.attacking == True: # This is a seperate image
            if self.facing == "right":
                self.attackFrame = pygame.transform.flip(self.currentAttackFrame, True, False)
                gameDisplay.blit(self.attackFrame, worldScreen(self.coordinates) - pygame.Vector2(10, 16))
            else:
                self.attackFrame = self.currentAttackFrame
                gameDisplay.blit(self.attackFrame, worldScreen(self.coordinates) - pygame.Vector2(24, 14))

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

    def jump(self):
        if self.jumpState == "grounded": # jump states are handeled here, gravity and movement is handled in physics
            if keyDown[self.jumpkey]:
                # print("Jump State: " + str(self.jumpState))
                self.yVelocity = 6

        if self.yVelocity >= 4:
            self.jumpState = "takeoff"
        if self.yVelocity < 4 and self.yVelocity > 1:
            self.jumpState = "peak"    
        if self.yVelocity <= 1:
            self.jumpState = "airborne"
        if self.yVelocity <= 1 and self.coordinates.z < 1:
            self.jumpState = "landing"  
        if self.yVelocity == 0 and self.coordinates.z < 0.05:
            self.jumpState = "grounded"

    def attack(self): # currently this is entirely visual, there's no hitbox or interaction

        if self.attacking == False:
            if keyDown[self.attackKey]:
                self.attacking = True
        
        if self.attacking == True:
            
            currentTime = pygame.time.get_ticks() # running the attack animations here as it's technically a seperate object
            if currentTime - self.attackLastUpdate >= attackAnimationTick:
                self.attackFrameNum += 1
                self.attackLastUpdate = currentTime

                if self.attackFrameNum >= len(attackAni):
                    self.attackFrameNum = 0
                    self.attacking = False
                    
                
                self.currentAttackFrame = attackAni[self.attackFrameNum]
            else:
                return
        
    def physics(self): # gravity and vertical movement is done here

        tile = tileCoords(self.coordinates)

        self.yVelocity += gravity * dt

        if tile.x < 0 or tile.y < 0 or tile.x > len(mapData) - 1  or tile.y > len(mapData) - 1: # checking if player is within map bounds
            self.yVelocity += gravity * dt
        else:
            if mapData[int(tile.y)][int(tile.x)] == 1: # checking if player is on a solid tile
                if self.coordinates.z > 0.00001 or self.coordinates.z < -0.25: # hackerman
                    self.yVelocity += gravity * dt
                else:
                    if not(self.jumpState == "takeoff"):
                        self.yVelocity = 0
                        self.coordinates.z = 0.000001
            else:
                
                self.yVelocity += gravity * dt
            
        self.coordinates.z += self.yVelocity * dt

        if self.coordinates.z <= -6:
            self.coordinates = pygame.Vector3(5, 5, 1)
            self.yVelocity = 4

    def updateFrame(self): # all PLAYER animations are handled here. animation updates would be independant per player (if I had more)
        global currentTime, animationTick
        
        currentTime = pygame.time.get_ticks()

        if keyDown[self.up] or keyDown[self.left] or keyDown[self.down] or keyDown[self.right]:
            currentTime = pygame.time.get_ticks()
            
            if currentTime - self.lastUpdate >= animationTick:
                self.frameNum += 1
                self.lastUpdate = currentTime
                if self.frameNum >= len(cornetAni):
                    self.frameNum = 0

                self.currentFrame = cornetAni[self.frameNum] # seems useless but it helps fix a visual issue with flipping
        else:
            self.currentFrame = cornetIDLE

        if self.jumpState == "takeoff":
            self.currentFrame = cornetSTANCE

        if self.jumpState == "peak" or self.jumpState == "landing":
            self.currentFrame = cornetFALLPEAK

        if self.jumpState == "airborne":
            self.currentFrame = cornetFALL

        if self.facing == "right":
                self.frame = pygame.transform.flip(self.currentFrame, True, False)
                # self.frame = pygame.transform.flip(self.frame, True, False)
        else:
            self.frame = self.currentFrame
        
    def playerSounds(self): # all player sounds (incl. attack) are handled here.
        global playerJumpChannel, playerAttackChannel

        tile = tileCoords(self.coordinates)

        if self.jumpState == "grounded": # Walking works a bit differently from the other sounds, just a walking loop playing and unpaused at times.
            if keyDown[self.up] or keyDown[self.left] or keyDown[self.down] or keyDown[self.right]:
                playerWalk.unpause()
            else:
                playerWalk.pause()
        else:
            playerWalk.pause()
        

        if tile.x < 0 or tile.y < 0 or tile.x > len(mapData) - 1  or tile.y > len(mapData) - 1:
            pass

        else:
            if mapData[int(tile.y)][int(tile.x)] == 1:
                if self.jumpState == "landing" and self.coordinates.z >= 0.01 and self.yVelocity < 0:
                    playSound(playerJumpChannel, playerLand)
        
        if self.jumpState == "takeoff":
            playSound(playerJumpChannel, playerJump)
        
        if self.attacking:
            playSound(playerAttackChannel, defaultSwing)

                
pygame.init()
pygame.mixer.init()
pygame.time.Clock()

""" Begin the variable spam! """

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
gravity = -4.9

debugBlock = pygame.image.load("Assets\World\pixil-frame-2.png").convert_alpha()

mossCobble = pygame.image.load("Assets\World\mossCobble.png").convert_alpha()
mossCobble2 = pygame.image.load("Assets\World\mossCobble2.png").convert_alpha()
mossCobble3 = pygame.image.load("Assets\World\mossCobble3.png").convert_alpha()
mossCobble4 = pygame.image.load("Assets\World\mossCobble4.png").convert_alpha()
mossCobble5 = pygame.image.load("Assets\World\mossCobble5.png").convert_alpha()
cobble = pygame.image.load("Assets\World\cobble.png").convert_alpha()
cobble2 = pygame.image.load("Assets\World\cobble2.png").convert_alpha()
cobble3 = pygame.image.load("Assets\World\cobble3.png").convert_alpha()

blockTileList = []

backgroundImg = pygame.image.load("Assets\World\MossBackground.png").convert_alpha()

# There's probably a faster way of getting all these.. oh well
# Probably should've consolidated this all into a spritesheet but idk how

cornetIDLE = pygame.image.load("Assets\Kornet\Cornet Idle.png").convert_alpha()
cornetFALL = pygame.image.load("Assets\Kornet\KornetFall.png").convert_alpha()
cornetFALLPEAK = pygame.image.load("Assets\Kornet\KornetFallPeak.png").convert_alpha()
cornetSTANCE = pygame.image.load("Assets\Kornet\Kornet Walk 2.png").convert_alpha()

cornet1 = pygame.image.load("Assets\Kornet\cornet1.png").convert_alpha()
cornet2 = pygame.image.load("Assets\Kornet\Kornet Walk 1.png").convert_alpha()
cornet3 = pygame.image.load("Assets\Kornet\Kornet Walk 3.png").convert_alpha()
cornet4 = pygame.image.load("Assets\Kornet\Kornet Walk 4.png").convert_alpha()

cornetAni = [cornet1, cornet2, cornet4, cornet3]

attack1 = pygame.image.load("Assets\Attacks\Attack1.png").convert_alpha()
attack2 = pygame.image.load("Assets\Attacks\Attack2.png").convert_alpha()
attack3 = pygame.image.load("Assets\Attacks\Attack3.png").convert_alpha()
attack4 = pygame.image.load("Assets\Attacks\Attack4.png").convert_alpha()

attackAni = [attack1, attack2, attack3, attack4]

animationTick = 100
attackAnimationTick = 60
currentTime = pygame.time.get_ticks()

grassStep = pygame.mixer.Sound("Sounds\hero_run_footsteps_grass.wav")
playerLand = pygame.mixer.Sound("Sounds\hero_land_soft.wav")
playerJump = pygame.mixer.Sound("Sounds\hero_jump.wav")

defaultSwing = pygame.mixer.Sound("Sounds\sword_3.wav")
# Didn't use the list cause it added some static... not sure why, but I can't fix it
# swingSounds = [pygame.mixer.Sound("sword_1.wav"), pygame.mixer.Sound("sword_2.wav"), pygame.mixer.Sound("sword_3.wav"), pygame.mixer.Sound("sword_4.wav"), pygame.mixer.Sound("sword_5.wav")]

mapFile = open("Assets\World\solidMap.txt", "r")
mapData = []

i = 0
for row in mapFile.read().split("\n"):
    rowArray = []
    print(row)
    for char in row:
        rowArray.append(int(char))

    mapData.insert(i, rowArray)
    i += 1

kornet = Hornet(pygame.Vector3(4.5, 4.5, 3), 3, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, False, pygame.K_x, pygame.K_z)
# though multiple players are THEORETICALLY easy with the class, I'm not sure how to make it work with the layer rendering

# Just what the window is actually called
pygame.display.set_caption("Silksong?!")
pygame.display.set_icon(cornetFALL)

# Music and channels

pygame.mixer.music.load("Sounds\Greenpath.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.25)

playerWalk = grassStep.play(-1)
playerWalk.pause()

playerJumpChannel = pygame.mixer.Channel(1)
playerAttackChannel = pygame.mixer.Channel(2)

running = True
while running:

    pygame.event.get()
    keyDown = pygame.key.get_pressed()
    mouseDown = pygame.mouse.get_pressed()

    kornet.move()
    kornet.jump()

    """    
    # Original camera movement code, now it's centered on the player
    # if keyDown[pygame.K_RIGHT]:
    #     viewTransform -= screenWorld(pygame.Vector3(1 * dt, 0, 0))
    # if keyDown[pygame.K_LEFT]:
    #     viewTransform += screenWorld(pygame.Vector3(1 * dt, 0, 0))
    # if keyDown[pygame.K_UP]:
    #     viewTransform += screenWorld(pygame.Vector3(0, 1 * dt, 0))
    # if keyDown[pygame.K_DOWN]:
    #     viewTransform -= screenWorld(pygame.Vector3(0, 1 * dt, 0))
    """
        
    viewTransform = kornet.coordinates

    dt = clock.tick(60)/1000

    kornet.physics()
    #playerPhysicx() moved into player class

    # flip() the display to put your work on screen
    drawWorld() 
    pygame.display.flip()

    for event in pygame.event.get(): # actually closing the window when you click the X
        if event.type == pygame.QUIT:
            running = False
    
pygame.quit()
sys.exit()
