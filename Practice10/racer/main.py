import pygame, sys
from pygame.locals import *
import random, time

# Инициализация
pygame.init()

# Настройка FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

# Параметры экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SCORE = 0

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Загрузка изображений
# Убедись, что AnimatedStreet.png лежит в корне папки racer
background = pygame.image.load("images\AnimatedStreet.png")

# Создание окна
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Pro")

# --- Секция звуков ---
# Загружаем звуки с проверкой, чтобы код не ломался без файлов
try:
    crash_sound = pygame.mixer.Sound('sounds\crash.wav')
    pygame.mixer.music.load('sounds\background.mp3')
    pygame.mixer.music.play(-1) 
except:
    crash_sound = None
    print("Звуковые файлы не найдены, играем без звука")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("images\Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images\coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        self.rect.center = (random.randint(30, SCREEN_WIDTH-30), -50)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            self.spawn()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("images\Player.png")
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

# Группировка объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Таймер ускорения
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Главный цикл
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5      
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отрисовка мира
    DISPLAYSURF.blit(background, (0,0))
    
    # Счетчики
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_txt = font_small.render(f"Coins: {COIN_SCORE}", True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(coin_txt, (SCREEN_WIDTH - 110, 10))

    # Обновление всех спрайтов
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Логика сбора монет
    if pygame.sprite.spritecollideany(P1, coins):
        COIN_SCORE += 1
        # Можно добавить звук подбора монеты, если есть файл:
        # pygame.mixer.Sound('coin_collect.wav').play()
        C1.spawn()

    # Логика столкновения с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        if crash_sound:
            crash_sound.play() # Запуск звука аварии
        
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))
        pygame.display.update()
        
        for entity in all_sprites:
            entity.kill() 
            
        time.sleep(2)
        pygame.quit()
        sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)