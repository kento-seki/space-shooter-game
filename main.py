import pygame
from random import randint, uniform
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT - 150))
        self.direction = pygame.Vector2()
        self.speed = 300
        # Laser cooldown
        self.canShoot = True
        self.laserShootTime = 0
        self.coolDownDuration = 400

    def update(self, dt):
        # Update player position according to keyboard input
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        if pygame.key.get_just_pressed()[pygame.K_SPACE] and self.canShoot:
            Laser(laserSurface, self.rect.midtop, allSprites)
            self.canShoot = False
            self.laserShootTime = pygame.time.get_ticks()

        self.laserTimer()

    def laserTimer(self):
        if not self.canShoot:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.laserShootTime >= self.coolDownDuration:
                self.canShoot = True

class Star(pygame.sprite.Sprite):
    def __init__(self, group, surface):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_frect(
            center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
        )

    def update(self, dt):
        pass

class Laser(pygame.sprite.Sprite):

    LASER_SPEED = 400

    def __init__(self, surface, pos, group):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_frect(midbottom=pos)

    def update(self, dt):
        self.rect.centery -= self.LASER_SPEED * dt
        # make sure lasers that go off the screen don't occupy memory forever
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    METEOR_LIFETIME = 3000

    def __init__(self, surface, pos, group):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_frect(center=pos)
        self.timeCreated = pygame.time.get_ticks()
        self.direction = pygame.Vector2(uniform(-0.5,0.5), 1)
        self.speed = randint(400, 500)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.timeCreated > self.METEOR_LIFETIME:
            self.kill()

# General setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

# Import images as surfaces
starSurface = pygame.image.load(join('images', 'star.png')).convert_alpha()
meteorSurface = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laserSurface = pygame.image.load(join('images', 'laser.png'))

# Sprites
allSprites = pygame.sprite.Group()
for i in range(20):
    star = Star(allSprites, starSurface)
player = Player(allSprites)

# Meteor event which triggers regularly - this can be detected by event loop
meteorEvent = pygame.event.custom_type()
pygame.time.set_timer(meteorEvent, 500)

#
# Loop indefinitely, creating and displaying frames
#
while running:
    dt = clock.tick(120) / 1000 # returns delta time: time to render frame

    # Event loop - handles all inputs, timers, etc...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteorEvent:
            x, y = randint(0,WINDOW_WIDTH), randint(-200,-100)
            Meteor(meteorSurface, (x,y), allSprites)
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
