import pygame
from random import randint
from os.path import join

#
# General setup
#
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True

playerSurface = pygame.image.load(join('images', 'player.png')).convert_alpha()
playerRect = playerSurface.get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT - 150))
playerDirection = 1

starSurface = pygame.image.load(join('images', 'star.png')).convert_alpha()
starPositions = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for _ in range(20)]

meteorSurface = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteorRect = meteorSurface.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

laserSurface = pygame.image.load(join('images', 'laser.png'))
laserRect = laserSurface.get_frect(bottomleft=(WINDOW_WIDTH-20, WINDOW_HEIGHT-20))

#
# Loop indefinitely, creating and displaying frames
#
while running:
    # event loop - handles all keyboard inputs, timers, etc...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    displaySurface.fill('darkgray') # draw the game

    #
    # Attach all surfaces to display surface
    #
    for i in range(20):
        displaySurface.blit(starSurface, starPositions[i])

    playerRect.left += playerDirection * 0.5
    if playerRect.right >= WINDOW_WIDTH or playerRect.left < 0:
        playerDirection *= -1

    displaySurface.blit(meteorSurface, meteorRect)
    displaySurface.blit(laserSurface, laserRect)
    displaySurface.blit(playerSurface, playerRect)

    pygame.display.update()

pygame.quit()
