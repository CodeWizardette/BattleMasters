import os
import random

class GameMatrix:
    def __init__(self):
        self.matrix = []

    def create_game_matrix(self, num_villagers, num_builders, num_soldiers):
        self.matrix = []

        # Köylülerin pozisyonları
        for _ in range(num_villagers):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            self.matrix.append({"type": "villager", "x": x, "y": y})

        # İnşaatçıların pozisyonları
        for _ in range(num_builders):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            self.matrix.append({"type": "builder", "x": x, "y": y})

        # Askerlerin pozisyonları
        for _ in range(num_soldiers):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            self.matrix.append({"type": "soldier", "x": x, "y": y})

    def print_game_matrix(self):
        for item in self.matrix:
            print(f"Type: {item['type']}, X: {item['x']}, Y: {item['y']}")

    def save_game_matrix(self, filename):
        with open(filename, "w") as file:
            for item in self.matrix:
                file.write(f"{item['type']},{item['x']},{item['y']}\n")

    def load_game_matrix(self, filename):
        self.matrix = []
        with open(filename, "r") as file:
            for line in file:
                item = line.strip().split(",")
                self.matrix.append({"type": item[0], "x": int(item[1]), "y": int(item[2])})
