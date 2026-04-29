import pygame
import random
import time
from persistence import DIFFICULTY_PARAMS

BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (255, 0,   0)
YELLOW = (255, 220, 40)
ORANGE = (255, 140, 0)
GREEN  = (80,  200, 80)
CYAN   = (0,   220, 220)
GRAY   = (160, 160, 160)
DARK   = (18,  18,  30)
ACCENT = (255, 200, 0)

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600
ROAD_LEFT     = 40
ROAD_RIGHT    = 360
LANE_COUNT    = 4
LANE_W        = (ROAD_RIGHT - ROAD_LEFT) // LANE_COUNT
LANES         = [ROAD_LEFT + LANE_W * i + LANE_W // 2 for i in range(LANE_COUNT)]

POWERUP_TYPES    = ["nitro", "shield", "repair"]
POWERUP_COLORS   = {"nitro": ORANGE, "shield": CYAN, "repair": GREEN}
POWERUP_DURATION = {"nitro": 4000, "shield": 0, "repair": 0}
POWERUP_LABELS   = {"nitro": "NITRO", "shield": "SHIELD", "repair": "REPAIR"}

OBSTACLE_TYPES = ["oil", "barrier", "pothole"]
OBSTACLE_COLORS = {
    "oil":     (30,  30,  30),
    "barrier": (220, 60,  60),
    "pothole": (80,  50,  20),
}

CAR_IMAGE_MAP = {
    "blue":   "assets/images/Player_bl.png",
    "green":  "assets/images/Player_gr.png",
    "red":    "assets/images/Player_red.png",
    "yellow": "assets/images/Player_yel.png",
}


class Player(pygame.sprite.Sprite):
    def __init__(self, car_color="blue"):
        super().__init__()
        path = CAR_IMAGE_MAP.get(car_color, CAR_IMAGE_MAP["blue"])
        try:
            self.image = pygame.image.load(path).convert_alpha()
        except Exception:
            self.image = pygame.Surface((40, 70), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (80, 120, 255), (0, 0, 40, 70), border_radius=8)
        self.base_image = self.image.copy()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, 520))
        self.shield_active = False
        self.nitro_active  = False
        self.nitro_end     = 0

    def move(self):
        keys = pygame.key.get_pressed()
        speed = 7 if self.nitro_active else 5
        if self.rect.left > ROAD_LEFT and keys[pygame.K_LEFT]:
            self.rect.move_ip(-speed, 0)
        if self.rect.right < ROAD_RIGHT and keys[pygame.K_RIGHT]:
            self.rect.move_ip(speed, 0)

    def update_powerups(self, now):
        if self.nitro_active and now >= self.nitro_end:
            self.nitro_active = False

    def activate_nitro(self, now):
        self.nitro_active = True
        self.nitro_end = now + POWERUP_DURATION["nitro"]

    def activate_shield(self):
        self.shield_active = True

    def draw_shield(self, surf):
        if self.shield_active:
            pygame.draw.ellipse(surf, (*CYAN, 80),
                                self.rect.inflate(20, 20))
            pygame.draw.ellipse(surf, CYAN,
                                self.rect.inflate(20, 20), 2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/images/Enemy.png").convert_alpha()
        except Exception:
            self.image = pygame.Surface((40, 70), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (220, 60, 60), (0, 0, 40, 70), border_radius=8)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.center = (random.choice(LANES), -80)

    def move(self):
        self.rect.move_ip(0, self.speed)

    def respawn(self, speed):
        self.speed = speed
        self.rect.center = (random.choice(LANES), random.randint(-300, -80))


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        try:
            self.original_image = pygame.image.load("assets/images/coin.png").convert_alpha()
        except Exception:
            self.original_image = None
        self.speed = speed
        self.spawn()

    def spawn(self):
        self.weight = random.choice([1, 3, 5])
        size = 20 + self.weight * 5
        if self.original_image:
            self.image = pygame.transform.scale(self.original_image, (size, size))
        else:
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(self.image, YELLOW, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect(center=(random.choice(LANES), -50))

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.speed   = speed
        self.kind    = random.choice(POWERUP_TYPES)
        self.color   = POWERUP_COLORS[self.kind]
        self.image   = pygame.Surface((36, 36), pygame.SRCALPHA)
        self.spawn_time = pygame.time.get_ticks()
        self._draw()
        self.rect    = self.image.get_rect(center=(random.choice(LANES), -60))

    def _draw(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, self.color, (18, 18), 17)
        pygame.draw.circle(self.image, WHITE, (18, 18), 17, 2)
        font = pygame.font.SysFont("Consolas", 9, bold=True)
        lbl = font.render(POWERUP_LABELS[self.kind][:3], True, WHITE)
        self.image.blit(lbl, lbl.get_rect(center=(18, 18)))

    def move(self):
        self.rect.move_ip(0, self.speed)

    def expired(self, now, timeout=8000):
        return now - self.spawn_time > timeout or self.rect.top > SCREEN_HEIGHT


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.kind  = random.choice(OBSTACLE_TYPES)
        self.speed = speed
        if self.kind == "oil":
            self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, (*OBSTACLE_COLORS["oil"], 200), (0, 0, 50, 30))
        elif self.kind == "barrier":
            self.image = pygame.Surface((60, 18), pygame.SRCALPHA)
            pygame.draw.rect(self.image, OBSTACLE_COLORS["barrier"], (0, 0, 60, 18), border_radius=4)
            pygame.draw.rect(self.image, WHITE, (0, 0, 60, 18), 2, border_radius=4)
        else:
            self.image = pygame.Surface((34, 20), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, OBSTACLE_COLORS["pothole"], (0, 0, 34, 20))
        self.rect = self.image.get_rect(center=(random.choice(LANES), -40))

    def move(self):
        self.rect.move_ip(0, self.speed)


class NitroStrip(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.image = pygame.Surface((ROAD_RIGHT - ROAD_LEFT, 14), pygame.SRCALPHA)
        for x in range(0, self.image.get_width(), 20):
            pygame.draw.rect(self.image, (*ORANGE, 180), (x, 0, 14, 14), border_radius=3)
        self.rect = self.image.get_rect(topleft=(ROAD_LEFT, -20))

    def move(self):
        self.rect.move_ip(0, self.speed)


def safe_spawn_x(player_rect):
    choices = [x for x in LANES if abs(x - player_rect.centerx) > 60]
    return random.choice(choices) if choices else random.choice(LANES)


def run_game(surf, clock, username, settings):
    pygame.display.set_caption("Racer Pro")

    diff   = settings.get("difficulty", "normal")
    params = DIFFICULTY_PARAMS[diff]
    SPEED       = params["speed"]
    SPAWN_RATE  = params["spawn_rate"]
    SPEED_STEP  = params["speed_step"]

    sound_on = settings.get("sound", True)
    try:
        if sound_on:
            pygame.mixer.music.load("assets/sounds/background.mp3")
            pygame.mixer.music.play(-1)
        crash_sound = pygame.mixer.Sound("assets/sounds/crash.mp3") if sound_on else None
    except Exception:
        crash_sound = None

    try:
        background = pygame.image.load("assets/images/AnimatedStreet.png").convert()
    except Exception:
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill((50, 50, 50))

    bg_y1, bg_y2 = 0, -SCREEN_HEIGHT

    font_sm  = pygame.font.SysFont("Consolas", 16, bold=True)
    font_med = pygame.font.SysFont("Consolas", 19, bold=True)

    P1 = Player(settings.get("car_color", "blue"))

    enemies   = pygame.sprite.Group()
    coins     = pygame.sprite.Group()
    powerups  = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    strips    = pygame.sprite.Group()

    for _ in range(2):
        e = Enemy(SPEED)
        e.rect.center = (random.choice(LANES), random.randint(-400, -80))
        enemies.add(e)

    coin = Coin(SPEED)
    coins.add(coin)

    SCORE      = 0
    COIN_SCORE = 0
    distance   = 0.0

    TOTAL_DIST    = 3000.0
    spawn_timer   = 0
    powerup_timer = 0
    strip_timer   = 0

    active_powerup      = None
    active_powerup_end  = 0
    active_powerup_kind = None

    INC_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INC_SPEED, 1000)

    running = True
    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if event.type == pygame.K_ESCAPE:
                running = False
            if event.type == INC_SPEED:
                SPEED = round(SPEED + 0.3, 1)

        bg_y1 += SPEED * 0.8
        bg_y2 += SPEED * 0.8
        if bg_y1 >= SCREEN_HEIGHT:
            bg_y1 = -SCREEN_HEIGHT
        if bg_y2 >= SCREEN_HEIGHT:
            bg_y2 = -SCREEN_HEIGHT
        surf.blit(background, (0, int(bg_y1)))
        surf.blit(background, (0, int(bg_y2)))

        distance += SPEED * 0.05

        P1.move()
        P1.update_powerups(now)

        for e in enemies:
            e.move()
            if e.rect.top > SCREEN_HEIGHT:
                SCORE += 1
                e.respawn(SPEED)

        for c in list(coins):
            c.speed = SPEED
            c.move()

        for obs in list(obstacles):
            obs.speed = SPEED
            obs.move()
            if obs.rect.top > SCREEN_HEIGHT:
                obs.kill()

        for pu in list(powerups):
            pu.speed = SPEED
            pu.move()
            if pu.expired(now):
                pu.kill()

        for st in list(strips):
            st.speed = SPEED
            st.move()
            if st.rect.top > SCREEN_HEIGHT:
                st.kill()

        spawn_timer += 1
        if spawn_timer >= SPAWN_RATE:
            spawn_timer = 0
            e = Enemy(SPEED)
            e.rect.centerx = safe_spawn_x(P1.rect)
            e.rect.top = -80
            enemies.add(e)
            if random.random() < 0.6:
                obs = Obstacle(SPEED)
                obs.rect.centerx = safe_spawn_x(P1.rect)
                obs.rect.top = -40
                obstacles.add(obs)

        powerup_timer += 1
        if powerup_timer >= 180:
            powerup_timer = 0
            if random.random() < 0.45 and len(powerups) == 0:
                pu = PowerUp(SPEED)
                pu.rect.centerx = safe_spawn_x(P1.rect)
                powerups.add(pu)

        strip_timer += 1
        if strip_timer >= 300:
            strip_timer = 0
            if random.random() < 0.3:
                strips.add(NitroStrip(SPEED))

        collected = pygame.sprite.spritecollide(P1, coins, False)
        for c in collected:
            old = COIN_SCORE
            COIN_SCORE += c.weight
            if (COIN_SCORE // SPEED_STEP) > (old // SPEED_STEP):
                SPEED = round(SPEED + 0.5, 1)
            c.spawn()

        pu_hit = pygame.sprite.spritecollide(P1, powerups, True)
        for pu in pu_hit:
            active_powerup_kind = pu.kind
            if pu.kind == "nitro":
                P1.activate_nitro(now)
                active_powerup_end = now + POWERUP_DURATION["nitro"]
            elif pu.kind == "shield":
                P1.activate_shield()
                active_powerup_end = now + 999999
            elif pu.kind == "repair":
                active_powerup_end = now + 2000

        strip_hit = pygame.sprite.spritecollide(P1, strips, False)
        if strip_hit and not P1.nitro_active:
            P1.activate_nitro(now)
            active_powerup_kind = "nitro"
            active_powerup_end  = now + 2000

        obs_hit = pygame.sprite.spritecollide(P1, obstacles, False)
        if obs_hit:
            if P1.shield_active:
                P1.shield_active = False
                active_powerup_kind = None
                for o in obs_hit:
                    o.kill()
            else:
                running = False

        enemy_hit = pygame.sprite.spritecollide(P1, enemies, False)
        if enemy_hit:
            if P1.shield_active:
                P1.shield_active = False
                active_powerup_kind = None
                for e in enemy_hit:
                    e.respawn(SPEED)
            else:
                running = False

        if not running:
            break

        surf.blit(P1.image, P1.rect)
        P1.draw_shield(surf)

        for e in enemies:
            surf.blit(e.image, e.rect)
        for c in coins:
            surf.blit(c.image, c.rect)
        for obs in obstacles:
            surf.blit(obs.image, obs.rect)
        for pu in powerups:
            surf.blit(pu.image, pu.rect)
        for st in strips:
            surf.blit(st.image, st.rect)

        hud_bg = pygame.Surface((SCREEN_WIDTH, 58), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 160))
        surf.blit(hud_bg, (0, 0))

        surf.blit(font_sm.render(f"Score:  {SCORE}", True, WHITE),           (8,  4))
        surf.blit(font_sm.render(f"Coins:  {COIN_SCORE}", True, YELLOW),     (8, 22))
        surf.blit(font_sm.render(f"Speed:  {SPEED:.1f}", True, ACCENT),      (8, 40))
        surf.blit(font_sm.render(f"Dist: {int(distance)}/{int(TOTAL_DIST)}m", True, GRAY), (220, 4))
        surf.blit(font_sm.render(f"Player: {username}", True, GRAY),         (220, 22))

        bar_w = int((distance / TOTAL_DIST) * 150)
        pygame.draw.rect(surf, DARK, (220, 42, 150, 10), border_radius=4)
        pygame.draw.rect(surf, GREEN, (220, 42, bar_w, 10), border_radius=4)

        if active_powerup_kind:
            remaining = max(0, active_powerup_end - now)
            if active_powerup_kind == "nitro" and remaining > 0:
                label = f"NITRO {remaining//1000+1}s"
                col   = ORANGE
            elif active_powerup_kind == "shield" and P1.shield_active:
                label = "SHIELD"
                col   = CYAN
            elif active_powerup_kind == "repair" and remaining > 0:
                label = "REPAIR!"
                col   = GREEN
            else:
                label = None
                col   = WHITE

            if label:
                pw_surf = pygame.Surface((120, 26), pygame.SRCALPHA)
                pw_surf.fill((0, 0, 0, 140))
                surf.blit(pw_surf, (140, 60))
                pw_lbl = font_med.render(label, True, col)
                surf.blit(pw_lbl, pw_lbl.get_rect(center=(200, 73)))

        pygame.display.flip()
        clock.tick(60)

    if crash_sound:
        crash_sound.play()
    pygame.mixer.music.stop()

    final_score = SCORE * 10 + COIN_SCORE * 5 + int(distance)
    return final_score, distance, COIN_SCORE