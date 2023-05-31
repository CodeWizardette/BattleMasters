import pygame

def move_villager(villager, direction):
    # Köylüyü belirtilen yöne hareket ettir
    if direction == "up":
        villager.rect.y -= villager.speed_bonus
    elif direction == "down":
        villager.rect.y += villager.speed_bonus
    elif direction == "left":
        villager.rect.x -= villager.speed_bonus
    elif direction == "right":
        villager.rect.x += villager.speed_bonus

def build(builder, building):
    # İnşaatçıyı belirtilen binayı inşa etmeye yönlendir
    # İşlemler...
    pass

def attack(soldier, target):
    # Askeri belirtilen hedefe saldırmaya yönlendir
    # İşlemler...
    pass
