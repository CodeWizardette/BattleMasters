import pygame
from game_commands import move_villager


# Köylü sınıfı
class Villager(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(color=("red"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_bonus = 0

    def update(self):
        # Köylü hareketi ve diğer güncellemeler burada yapılır
        pass

class Villager(pygame.sprite.Sprite):
    # ...

    def move(self, direction):
        move_villager(self, direction)
