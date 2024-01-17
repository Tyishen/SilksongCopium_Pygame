import pygame
import sys

windowHeight = 900
windowWidth = 900

def drawWorld():
    gameDisplay.fill((255, 255, 255))

    gameDisplay.blit(debugBlock, (0, 0))
    pygame.draw.circle(gameDisplay, "blue", playerCoords, 10)

    outputScreen.blit(pygame.transform.scale(gameDisplay, outputScreen.get_size()), (0, 0))
    

pygame.init()
outputScreen = pygame.display.set_mode((windowWidth, windowHeight))
gameDisplay = pygame.Surface((300, 300))

clock = pygame.time.Clock()
dt = 0

# Objects
playerCoords = pygame.Vector2(int(gameDisplay.get_width() / 2), int(gameDisplay.get_height() / 2))
debugBlock = pygame.image.load("pixil-frame-0.png").convert_alpha()

mapFile = open("map.txt", "r")
mapData = []

i = 0
for row in mapFile.read().split("\n"):
    rowArray = []
    print(row)
    for char in row:
        rowArray.append(int(char))

    mapData.insert(i, rowArray)
    i+=1
print(mapData)

enumerate()

running = True
while running:
    keyDown = pygame.key.get_pressed()
    
    if keyDown[pygame.K_w]:
        playerCoords.y -= 300 * dt
    if keyDown[pygame.K_a]:
        playerCoords.x -= 300 * dt
    if keyDown[pygame.K_s]:
        playerCoords.y += 300 * dt
    if keyDown[pygame.K_d]:
        playerCoords.x += 300 * dt
    
    
    
    dt = clock.tick(60)/1000

    # flip() the display to put your work on screen
    drawWorld() 
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("AAA")
            running = False
    
pygame.quit()
sys.exit()

def worldViewport(cartVect):
    pass
    

def ViewportWorld(x, y):
    pass