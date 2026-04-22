import pygame

class Ball:
    def __init__(self, x, y, radius, screen_width, screen_height):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (255, 0, 0) # Красный
        self.speed = 20
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self, dx, dy):
        # Вычисляем новую позицию
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # Проверка границ: центр +/- радиус не должны выходить за 0 и width/height
        if self.radius <= new_x <= self.screen_width - self.radius:
            self.x = new_x
        
        if self.radius <= new_y <= self.screen_height - self.radius:
            self.y = new_y

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)