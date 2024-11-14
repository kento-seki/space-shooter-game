import pygame
from random import randint
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT - 150))
        self.direction = pygame.Vector2()
        self.speed = 300

    def update(self, dt):
        # Update player position according to keyboard input
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            print('fire laser!')

class Star(pygame.sprite.Sprite):
    def __init__(self, group, surface):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_frect(
            center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
        )

    def update(self, dt):
        pass

#
# General setup
#
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

allSprites = pygame.sprite.Group()
starSurface = pygame.image.load(join('images', 'star.png')).convert_alpha()
for i in range(20):
    star = Star(allSprites, starSurface)
player = Player(allSprites)

#
# Load images as surfaces
#

meteorSurface = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteorRect = meteorSurface.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

laserSurface = pygame.image.load(join('images', 'laser.png'))
laserRect = laserSurface.get_frect(bottomleft=(WINDOW_WIDTH-20, WINDOW_HEIGHT-20))

#
# Loop indefinitely, creating and displaying frames
#
while running:
    dt = clock.tick(120) / 1000 # returns delta time: time to render frame

    # Event loop - handles all inputs, timers, etc...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #
        # Handling inputs via the event loop - possible, but not recommended
        #
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
        #     print('1 was pressed')
        # if event.type == pygame.MOUSEMOTION:
        #     playerRect.center = event.pos

    # Update game sprites
    allSprites.update(dt)

    # Draw the game and sprites
    displaySurface.fill('darkgray')
    allSprites.draw(displaySurface)

    pygame.display.update()

pygame.quit()
