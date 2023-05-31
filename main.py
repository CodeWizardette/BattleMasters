import pygame
import os
import random
import math
import time
import sys

from Villager import Villager
from builder import Builder 
from soldier import Soldier 
from game_commands import attack,build


# Klasörleri oku
game_folder = os.path.dirname(__file__)
game_image = os.path.join(game_folder, "img")
sound_folder = os.path.join(game_folder, "sound")
font_folder = os.path.join(game_folder, "font")
map_folder = os.path.join(game_folder, "map")
game_matrix_folder = os.path.join(game_folder, "game_matrix.txt")

# Ekranı otomatik algıla
pygame.init()


info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

# Entry Screen
class EntryScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen_surface = pygame.Surface((self.width, self.height))
        self.frame = pygame.Rect(200, 200, self.width - 400, self.height - 400) # Giriş ekranı çerçevesi
        self.tutorial_message = ["Welcome to BattleMasters!", "This is a real-time strategy game", "You can control villagers, builders, and soldiers", "Select one of these characters and set their destination", "Click on the screens to view them", "Press any key to continue"]

    def draw(self, surface):
        surface.fill((0, 0, 0))
        pygame.draw.rect(surface, (255, 255, 255), self.frame, 2)
        font = pygame.font.Font('freesansbold.ttf', 32)
        y_offset = 50
        for message in self.tutorial_message:
            text = font.render(message, True, WHITE)
            text_rect = text.get_rect(center=(self.width/2, self.height/2 + y_offset))
            surface.blit(text, text_rect)
            y_offset += 50

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            return False
        return True
       
# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)


# Oyun döngüsü
def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("BatteMasters")

    all_sprites = pygame.sprite.Group()

    # Köylülerin başlangıç pozisyonları
    villager1 = Villager(100, 100)
    villager2 = Villager(200, 200)

    all_sprites.add(villager1)
    all_sprites.add(villager2)

    builders = pygame.sprite.Group()
    soldiers = pygame.sprite.Group()

    # İnşaatçıların başlangıç pozisyonları
    builder1 = Builder(150, 150, speed_bonus=5)
    builder2 = Builder(250, 250, speed_bonus=15)

    builders.add(builder1)
    builders.add(builder2)

    # Askerlerin başlangıç pozisyonları
    soldier1 = Soldier(200, 200, speed_bonus=5)
    soldier2 = Soldier(300, 300, speed_bonus=15)

    soldiers.add(soldier1)
    soldiers.add(soldier2)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Arka planı temizle
        window.fill(BLACK)

        # Oyuncu etkileşimi
        handle_input()

        # Oyun mantığı
        update_game(all_sprites, builders, soldiers)

        # Oyuncu geri bildirimi
        render_game(window, all_sprites)

        pygame.display.update()

        # FPS ayarla
        clock.tick(60)

    pygame.quit()


def handle_input(all_sprites):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Köylülerin tıklanıp tıklanmadığını kontrol et
            for villager in all_sprites:
                villager_move = villager
                if isinstance(villager, Villager) and villager.rect.collidepoint(mouse_pos):
                    # Köylüye tıklandıysa
                    if villager.selected:
                        # Eğer köylü zaten seçiliyse, yeni hedef konumu belirleyerek ona gönder
                        villager_move(villager, mouse_pos)
                        # Eğer köylönçözési sözdekilere tıklandıysa, yeni hedef konumu belirleyerek ona gönder
                        if villager.rect.collidepoint(mouse_pos):
                            villager_move(villager, mouse_pos)
                        else:
                            # Eğer köylü seçili değilse, seçili hale getir
                            villager.selected = True
                            villager.select_color = GREEN
                    # Köylüye tıklanmadıysa, tüm köylülerin seçimini kaldır
                    if isinstance(villager, Villager):
                        villager.selected = False
                        villager.select_color = RED

            # İnşaatçıların tıklanıp tıklanmadığını kontrol et
            for builder in all_sprites:
                if isinstance(builder, Builder) and builder.rect.collidepoint(mouse_pos):
                    # İnşaatçıya tıklandıysa
                    if builder.selected:
                        # Eğer inşaatçı zaten seçiliyse, yeni hedef konumu belirleyerek ona gönder
                        build(builder, mouse_pos)
                    else:
                        # Eğer inşaatçı seçili değilse, seçili hale getir
                        builder.selected = True
                        builder.select_color = GREEN

                else:
                    # İnşaatçıya tıklanmadıysa, tüm inşaatçıların seçimini kaldır
                    if isinstance(builder, Builder):
                        builder.selected = False
                        builder.select_color = WHITE

            # Askerlerin tıklanıp tıklanmadığını kontrol et
            for soldier in all_sprites:
                if isinstance(soldier, Soldier) and soldier.rect.collidepoint(mouse_pos):
                    # Askerlere tıklandıysa
                    if soldier.selected:
                        # Eğer asker zaten seçiliyse, yeni hedef konumu belirleyerek ona gönder
                        attack(soldier, mouse_pos)
                    else:
                        # Eğer asker seçili değilse, seçili hale getir
                        soldier.selected = True
                        soldier.select_color = GREEN

                else:
                    # Askerlere tıklanmadıysa, tüm askerlerin seçimini kaldır
                    if isinstance(soldier, Soldier):
                        soldier.selected = False
                        soldier.select_color = BLACK



def update_game(all_sprites, builders, soldiers):
    # Köylülerin, inşaatçıların ve askerlerin hareketi ve diğer güncellemeleri yap
    all_sprites.update()
    builders.update()
    soldiers.update()


def render_game(window, all_sprites):
    # Oyuncu geri bildirimini ekrana çiz
    all_sprites.draw(window)

# Ana Harita
class MainMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map_surface = pygame.Surface((self.width, self.height))
        self.background_image = pygame.image.load("game_image/background.png") # Arka plan resmi
        self.frame = pygame.Rect(100, 100, self.width - 200, self.height - 200) # Ana çerçeve

    def draw(self, surface):
        surface.blit(self.background_image, (0, 0))
        pygame.draw.rect(surface, (255, 255, 255), self.frame, 2)

# Giriş Ekranı
class EntryScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen_surface = pygame.Surface((self.width, self.height))
        self.frame = pygame.Rect(200, 200, self.width - 400, self.height - 400) # Giriş ekranı çerçevesi

    def draw(self, surface):
        surface.fill((0, 0, 0))
        pygame.draw.rect(surface, (255, 255, 255), self.frame, 2)

# Savaş Ekranı
class BattleScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen_surface = pygame.Surface((self.width, self.height))
        self.frame = pygame.Rect(50, 50, self.width - 100, self.height - 100) # Savaş ekranı çerçevesi

    def draw(self, surface):
        surface.fill((255, 0, 0))
        pygame.draw.rect(surface, (255, 255, 255), self.frame, 2)

# Köy Ekranı
class VillageScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen_surface = pygame.Surface((self.width, self.height))
        self.frame = pygame.Rect(150, 150, self.width - 300, self.height - 300) # Köy ekranı çerçevesi

    def draw(self, surface):
        surface.fill((0, 255, 0))
        pygame.draw.rect(surface, (255, 255, 255), self.frame, 2)

# Kaynak Toplama Ekranı
class ResourceCollectionScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen_surface = pygame.Surface((self.width, self.height))
        self.frame = pygame.Rect(100, 100, self.width - 200, self.height - 200) # Kaynak toplama ekranı çerçevesi

    def draw(self, surface):
        surface.fill((0, 0, 255))
        pygame.draw.rect(surface, (255, 255, 255), self.frame, 2)

def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Pencereli Oyun Yüzeyi
    width = 800
    height = 600
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("My Game")

    # Haritaların Oluşturulması
    main_map = MainMap(3000, 5000)
    entry_screen = EntryScreen(width, height)
    battle_screen = BattleScreen(width, height)
    village_screen = VillageScreen(width, height)
    resource_collection_screen = ResourceCollectionScreen(width, height)

    # Oyun Döngüsü
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Giriş ekranında tıklama kontrolü
                if entry_screen.frame.collidepoint(event.pos):
                    entry_screen.draw(window)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    entry_screen_visible = False
                # Savaş ekranında tıklama kontrolö
                elif battle_screen.frame.collidepoint(event.pos):
                    battle_screen.draw(window)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    battle_screen_visible = True
                    
                # Köy ekranında tıklama kontrolü
                elif village_screen.frame.collidepoint(event.pos):
                    village_screen.draw(window)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    village_screen_visible = False
                # Kaynak toplama ekranında tıklama kontrolü
                elif resource_collection_screen.frame.collidepoint(event.pos):
                    resource_collection_screen.draw(window)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    resource_collection_screen_visible = False

        # Ana Harita Çizimi
        main_map.draw(window)

        # Ekranların Çizimi
        if entry_screen_visible:
            entry_screen.draw(window)
        if battle_screen_visible:
            battle_screen.draw(window)
        if village_screen_visible:
            village_screen.draw(window)
        if resource_collection_screen_visible:
            resource_collection_screen.draw(window)

        pygame.display.update()

        # FPS Ayarı
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
