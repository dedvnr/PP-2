import pygame
import random
import time

# Инициализация
pygame.init()

# Константы
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Pro: Levels Edition")
clock = pygame.time.Clock()

# Шрифты
font = pygame.font.SysFont("Arial", 25)
level_font = pygame.font.SysFont("Arial", 50, bold=True)

class SnakeGame:
    def __init__(self):
        # Начальное положение змейки (голова и два сегмента тела)
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.direction = "RIGHT"
        self.score = 0
        self.level = 1
        self.speed = 10  # Начальная скорость (FPS)
        self.food = self.spawn_food()

    def spawn_food(self):
        """Генерирует еду так, чтобы она не попала на тело змейки."""
        while True:
            # Рандомные координаты, кратные BLOCK_SIZE
            pos = [
                random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE
            ]
            # Проверяем, не занято ли это место змейкой
            if pos not in self.snake:
                return pos

    def update(self):
        """Обновление логики игры на каждом шаге."""
        head = list(self.snake[0])

        # Движение головы
        if self.direction == "UP": head[1] -= BLOCK_SIZE
        elif self.direction == "DOWN": head[1] += BLOCK_SIZE
        elif self.direction == "LEFT": head[0] -= BLOCK_SIZE
        elif self.direction == "RIGHT": head[0] += BLOCK_SIZE

        # 1. Проверка столкновения со стенами (выход за границы)
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return False

        # 2. Проверка столкновения с собственным телом
        if head in self.snake:
            return False

        # Добавляем новую голову в начало списка
        self.snake.insert(0, head)

        # 3. Проверка поедания фрукта
        if head == self.food:
            self.score += 1
            self.food = self.spawn_food()
            
            # ЛОГИКА УРОВНЕЙ: Повышаем уровень каждые 3 съеденных фрукта
            if self.score % 3 == 0:
                self.level += 1
                self.speed += 3 # Увеличиваем скорость (FPS) на 3
                self.flash_level_up() # Визуальный эффект
        else:
            # Убираем хвост, если ничего не съели
            self.snake.pop()
        
        return True

    def flash_level_up(self):
        """Короткое уведомление о повышении уровня."""
        text = level_font.render(f"LEVEL {self.level}!", True, (255, 255, 0))
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        pygame.display.flip()
        time.sleep(0.5)

def main():
    game = SnakeGame()
    running = True

    while running:
        screen.fill(BLACK)
        
        # Обработка клавиш
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game.direction != "DOWN":
                    game.direction = "UP"
                elif event.key == pygame.K_DOWN and game.direction != "UP":
                    game.direction = "DOWN"
                elif event.key == pygame.K_LEFT and game.direction != "RIGHT":
                    game.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and game.direction != "LEFT":
                    game.direction = "RIGHT"

        # Обновление состояния игры
        if not game.update():
            # Если проиграли — показываем Game Over
            msg = level_font.render("GAME OVER", True, RED)
            screen.blit(msg, (WIDTH // 2 - 120, HEIGHT // 2 - 30))
            pygame.display.flip()
            time.sleep(2)
            running = False

        # Отрисовка змейки
        for block in game.snake:
            pygame.draw.rect(screen, GREEN, (block[0], block[1], BLOCK_SIZE - 2, BLOCK_SIZE - 2))
        
        # Отрисовка еды
        pygame.draw.rect(screen, RED, (game.food[0], game.food[1], BLOCK_SIZE, BLOCK_SIZE))

        # Отрисовка интерфейса (Счет и Уровень)
        score_text = font.render(f"Score: {game.score}", True, WHITE)
        level_text = font.render(f"Level: {game.level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (WIDTH - 100, 10))

        pygame.display.flip()
        
        # Скорость игры зависит от текущего уровня
        clock.tick(game.speed)

    pygame.quit()

if __name__ == "__main__":
    main()