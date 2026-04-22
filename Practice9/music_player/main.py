import pygame
import sys
from player import MusicPlayer

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("KBD Music Player")
    font = pygame.font.SysFont("Arial", 24)
    big_font = pygame.font.SysFont("Arial", 32, bold=True)
    
    # Укажи путь к твоей папке с музыкой
    player = MusicPlayer("music") 
    
    clock = pygame.time.Clock()

    while True:
        screen.fill((30, 30, 30)) # Темный фон
        
        # 1. Обработка событий клавиатуры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: # Play
                    player.play()
                elif event.key == pygame.K_s: # Stop
                    player.stop()
                elif event.key == pygame.K_n: # Next
                    player.next_track()
                elif event.key == pygame.K_b: # Back/Prev
                    player.prev_track()
                elif event.key == pygame.K_q: # Quit
                    pygame.quit()
                    sys.exit()

        # 2. Отрисовка интерфейса
        # Заголовок
        title = big_font.render("Music Player", True, (255, 255, 255))
        screen.blit(title, (50, 50))
        
        # Инфо о треке
        status = "Playing" if player.is_playing else "Stopped"
        track_info = font.render(f"Track: {player.get_current_track_name()}", True, (0, 255, 0))
        status_info = font.render(f"Status: {status}", True, (200, 200, 200))
        
        screen.blit(track_info, (50, 150))
        screen.blit(status_info, (50, 200))
        
        # Инструкция
        hint = font.render("P: Play | S: Stop | N: Next | B: Prev | Q: Quit", True, (150, 150, 150))
        screen.blit(hint, (50, 320))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()