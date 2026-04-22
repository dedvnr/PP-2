import pygame
import sys
from datetime import datetime
from clock import ClockHand

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey's Clock - Separated Layers")
    clock = pygame.time.Clock()

    center = (WIDTH // 2, HEIGHT // 2)

    # 1. Загрузка слоев фона
    try:
        # Слой 1: Циферблат (clock.jpg)
        face_img = pygame.image.load(r"images\clock.png").convert_alpha()
        face_img = pygame.transform.scale(face_img, (600, 600))
        face_rect = face_img.get_rect(center=center)

        # Слой 2: Сам Микки (mikkey.png)
        mickey_img = pygame.image.load(r"images\mikkey.png").convert_alpha()
        # Подберем размер Микки, чтобы он вписался в центр (например, 350x350)
        mickey_img = pygame.transform.scale(mickey_img, (350, 450))
        mickey_rect = mickey_img.get_rect(center=center)
        
    except FileNotFoundError as e:
        print(f"Ошибка: Не найден файл изображения! {e}")
        sys.exit()

    # 2. Загрузка рук (используем твои названия файлов)
    # scale_size=(ширина ладони, длина всей руки)
    minute_hand = ClockHand(r"images\left_hand.png", center, scale_size=(70, 210))
    second_hand = ClockHand(r"images\right_hand.png", center, scale_size=(100, 240))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = datetime.now()
        
        # Обновляем руки
        minute_hand.update(now.minute + now.second / 60.0)
        second_hand.update(now.second)

        # 3. Отрисовка по слоям
        screen.fill((255, 255, 255))
        
        screen.blit(face_img, face_rect)   # Сначала пустой циферблат
        screen.blit(mickey_img, mickey_rect) # Затем Микки в центр
        
        minute_hand.draw(screen) # Минутная рука
        second_hand.draw(screen) # Секундная рука
        
        # Черный пин в самом центре
        pygame.draw.circle(screen, (0, 0, 0), center, 10)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()