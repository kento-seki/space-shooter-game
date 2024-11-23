import pygame
from random import randint, uniform
from os.path import join
from os import listdir

class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.originalSurface = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.image = self.originalSurface
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT - 150))
        self.direction = pygame.Vector2()
        self.speed = 300

        # Laser cooldown
        self.canShoot = True
        self.laserShootTime = 0
        self.coolDownDuration = 250

        # Mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        # Update player position according to keyboard input
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        if pygame.key.get_just_pressed()[pygame.K_SPACE] and self.canShoot:
            Laser(laserSurface, self.rect.midtop, (allSprites, laserSprites))
            laserSound.play()
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
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.centery -= self.LASER_SPEED * dt
        # make sure lasers that go off the screen don't occupy memory forever
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    METEOR_LIFETIME = 3000

    def __init__(self, surface, pos, group):
        super().__init__(group)
        self.originalSurface = surface
        self.image = self.originalSurface
        self.rect = self.image.get_frect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.timeCreated = pygame.time.get_ticks()
        self.direction = pygame.Vector2(uniform(-0.5,0.5), 1)
        self.speed = randint(400, 500)
        self.rotation = 0
        self.rotationSpeed = randint(50, 100)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.timeCreated > self.METEOR_LIFETIME:
            self.kill()

        # Continuous rotation
        self.rotation += self.rotationSpeed * dt
        self.image = pygame.transform.rotozoom(self.originalSurface, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)
        # ^ reassign the rect for the rotated surface, giving it the same center
        #   position, to prevent wobbling as surface is rotated

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, group):
        super().__init__(group)
        self.frames = frames
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frameIndex += 30 * dt
        if self.frameIndex < len(self.frames):
            self.image = self.frames[int(self.frameIndex)]
        else:
            self.kill()

def collisions(currScore):
    # Check for player-meteor collisions and laser-meteor collisions
    if pygame.sprite.spritecollide(player, meteorSprites, True, pygame.sprite.collide_mask):
        damageSound.play()
        currScore -= 5
    for laser in laserSprites:
        if pygame.sprite.spritecollide(laser, meteorSprites, True):
            explosionSound.play()
            laser.kill()
            currScore += 1
            # Explosion
            AnimatedExplosion(explosionFrames, laser.rect.midtop, allSprites)
    return currScore

def displayScore(currScore):
    fontColour = (240, 255, 255)
    textSurface = font.render(str(currScore), True, fontColour)
    textRect = textSurface.get_frect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT - 50))
    pygame.draw.rect(displaySurface, fontColour, textRect.inflate(20, 20).move(0, -10), 5, 10)
    displaySurface.blit(textSurface, textRect)

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
explosionFrameFiles = listdir(join('images', 'explosion'))
explosionFrames = [
    pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(0,21)
]

# Import font
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 50)

# Import sounds
laserSound = pygame.mixer.Sound(join('audio', 'laser.wav'))
laserSound.set_volume(0.3)
explosionSound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
explosionSound.set_volume(0.3)
damageSound = pygame.mixer.Sound(join('audio', 'crash.mp3'))
damageSound.set_volume(0.5)
gameMusic = pygame.mixer.Sound(join('audio', 'game_music.wav'))
gameMusic.set_volume(0.2)
gameMusic.play(loops = -1)

# Sprites
allSprites = pygame.sprite.Group()
meteorSprites = pygame.sprite.Group()
laserSprites = pygame.sprite.Group()
for i in range(20):
    star = Star(allSprites, starSurface)
player = Player(allSprites)

# Meteor event which triggers regularly - this can be detected by event loop
meteorEvent = pygame.event.custom_type()
pygame.time.set_timer(meteorEvent, 500)

#
# Loop indefinitely, creating and displaying frames
#
currScore = 0
while running:
    dt = clock.tick(120) / 1000 # returns delta time: time to render frame

    # Event loop - handles all inputs, timers, etc...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteorEvent:
            x, y = randint(0,WINDOW_WIDTH), randint(-200,-100)
            Meteor(meteorSurface, (x,y), (allSprites, meteorSprites))

    # Update game sprites
    allSprites.update(dt)

    currScore = collisions(currScore)

    # Draw the game and sprites
    displaySurface.fill('#3a2e3f')
    allSprites.draw(displaySurface)
    displayScore(currScore)

    pygame.display.update()

pygame.quit()
