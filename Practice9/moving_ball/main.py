import pygame
import sys
from ball import Ball

def main():
    pygame.init()
    
    # Настройки экрана
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball Game")
    
    # Создаем объект шара в центре экрана
    # Радиус 25 (итого 50x50 пикселей)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 25, WIDTH, HEIGHT)
    
    clock = pygame.time.Clock()

    while True:
        screen.fill((255, 255, 255)) # Белый фон
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Обработка нажатий клавиш-стрелок
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    ball.move(0, 1)
                elif event.key == pygame.K_LEFT:
                    ball.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    ball.move(1, 0)

        # Отрисовка
        ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()