import pygame

# Asker sınıfı
class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_bonus):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(color= "BLACK")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_bonus = speed_bonus

    def update(self):
        # Asker hareketi ve diğer güncellemeler burada yapılır
        pass
