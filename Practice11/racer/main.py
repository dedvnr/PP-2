import pygame, sys
from pygame.locals import *
import random, time

# Initialization
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GOLD  = (255, 223, 0)

# Screen dimensions and Game Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5          # Base speed of the enemy
SCORE = 0          # Number of enemies passed
COIN_SCORE = 0     # Total weight of coins collected
SPEED_STEP = 10    # Increase speed every 10 "coin points"

# Fonts
font_small = pygame.font.SysFont("Verdana", 20)
font_large = pygame.font.SysFont("Verdana", 60)
game_over_text = font_large.render("Game Over", True, BLACK)

# Load Images
background = pygame.image.load("images/AnimatedStreet.png")

# Window Setup
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Pro - Weighted Edition")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("images/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        # Enemy moves down based on the global SPEED
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("images/coin.png")
        self.spawn()

    def spawn(self):
        # Randomly generate coins with different weights
        self.weight = random.choice([1, 3, 5]) # 1=Small, 3=Medium, 5=Large/Rare
        
        # Scale the image based on weight (heavier = bigger)
        size = 20 + (self.weight * 5) 
        self.image = pygame.transform.scale(self.original_image, (size, size))
        
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH-30), -50)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            self.spawn()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# Object creation
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Background
    DISPLAYSURF.blit(background, (0,0))
    
    # UI Text
    scores = font_small.render(f"Enemies Passed: {SCORE}", True, BLACK)
    coin_txt = font_small.render(f"Coin Points: {COIN_SCORE}", True, BLACK)
    speed_txt = font_small.render(f"Speed: {SPEED}", True, BLACK)
    
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(coin_txt, (SCREEN_WIDTH - 160, 10))
    DISPLAYSURF.blit(speed_txt, (10, 35))

    # Move and Draw all Sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Logic for weighted coins
    if pygame.sprite.spritecollideany(P1, coins):
        old_coin_score = COIN_SCORE
        COIN_SCORE += C1.weight # Add the specific weight (1, 3, or 5)
        
        # TIncrease speed of Enemy when player earns N coins
        # Check if the new score crossed a multiple of SPEED_STEP
        if (COIN_SCORE // SPEED_STEP) > (old_coin_score // SPEED_STEP):
            SPEED += 1 
            
        C1.spawn() # Reset coin position and weight

    # Collision with Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over_text, (30,250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)