import pygame

# İnşaatçı sınıfı
class Builder(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_bonus):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_bonus = speed_bonus

    def update(self):
        # İnşaatçı hareketi ve diğer güncellemeler burada yapılır
        pass
