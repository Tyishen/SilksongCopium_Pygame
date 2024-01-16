import pygame
import sys

def drawWorld():
    pygame.draw.circle(screen, "blue", playerCoords, 10)
    blockDisplay.blit(debugBlock, (0, 0))
    screen.blit(pygame.transform.scale(blockDisplay, screen.get_size()), (0, 0))

pygame.init()
screen = pygame.display.set_mode((900, 900))
blockDisplay = pygame.Surface((300, 300))

clock = pygame.time.Clock()
dt = 0

# Objects
playerCoords = pygame.Vector2(int(screen.get_width() / 2), int(screen.get_height() / 2))
debugBlock = pygame.image.load("pixil-frame-0.png").convert_alpha()



running = True
while running:
    
    screen.fill("white")
    blockDisplay.fill((255, 255, 255))

    drawWorld()

    keyDown = pygame.key.get_pressed()
    
    if keyDown[pygame.K_w]:
        playerCoords.y -= 1200 * dt
    if keyDown[pygame.K_a]:
        playerCoords.x -= 1200 * dt
    if keyDown[pygame.K_s]:
        playerCoords.y += 1200 * dt
    if keyDown[pygame.K_d]:
        playerCoords.x += 1200 * dt
    
    
    
    dt = 0.001
    #clock.tick(60)/1000
    
    screen.blit(pygame.transform.scale(blockDisplay, screen.get_size()), (0, 0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("AAA")
            running = False
    
pygame.quit()
sys.exit()




def carIso(cartVect):
    
    isoVect

def isoCar(x, y):
    pass