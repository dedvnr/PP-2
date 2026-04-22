import pygame

class ClockHand:
    def __init__(self, image_path, center_pos, scale_size=None):
        self.center_pos = center_pos
        
        # Загружаем изображение руки
        hand_img = pygame.image.load(image_path).convert_alpha()
        
        if scale_size:
            hand_img = pygame.transform.scale(hand_img, scale_size)
        
        # Создаем прозрачный квадратный холст (высота х 2), 
        # чтобы плечо (низ картинки) оказалось в центре этого квадрата.
        w, h = hand_img.get_size()
        canvas_size = h * 2
        
        self.original_image = pygame.Surface((canvas_size, canvas_size), pygame.SRCALPHA)
        
        # Рисуем руку в верхней части квадрата
        # Теперь центр холста — это точка вращения (плечо)
        self.original_image.blit(hand_img, (canvas_size // 2 - w // 2, 25))
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=center_pos)

    def update(self, time_value):
        # 6 градусов на одну единицу времени
        angle = time_value * 6
        
        # Вращаем вокруг центра холста
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=self.center_pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)