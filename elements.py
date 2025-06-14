import pygame
import constants
import os

#Master Class
#Clase base para los elementos del juego
class GameElement:
    def __init__(self, x, y, image_path, size):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.size = self.image.get_width()

    def draw(self, screen, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        # Solo dibuja si está en pantalla
        if (screen_x + self.size >= 0 and screen_x <= constants.WIDTH and
                screen_y + self.size >= 0 and screen_y <= constants.HEIGHT):
            screen.blit(self.image, (screen_x, screen_y))

#Tree
#Árbol
class Tree(GameElement):
    def __init__(self, x, y):
        tree_path = os.path.join('assets', 'images', 'objects', 'tree.png')
        super().__init__(x, y, tree_path, constants.TREE)
        self.wood = 5

    def chop(self):
        if self.wood > 0:
            self.wood -= 1
            return True    
        return False

#Stones
#Piedras pequeñas
class SmallStone(GameElement):
    def __init__(self, x, y):
        stone_path = os.path.join('assets', 'images', 'objects', 'stone.png')
        super().__init__(x, y, stone_path, constants.SMALL_STONE)
        self.stone = 10

    def mine(self):
        if self.stone > 0:
            self.stone -= 1
            return True
        return False
    
#Flower
#Flor
class Flower(GameElement):
    def __init__(self, x, y):
        flower_path = os.path.join('assets', 'images', 'objects', 'flowers.png')
        super().__init__(x, y, flower_path, constants.FLOWER)
        self.flower = 1

    def collect(self):
        if self.flower > 0:
            self.flower -= 1
            return True
        return False
    
#Rose
#Rosa
class Rose(GameElement):
    def __init__(self, x, y):
        rose_path = os.path.join('assets', 'images', 'objects', 'rose.png')
        super().__init__(x, y, rose_path, constants.FLOWER)
        self.rose = 1

    def collect(self):
        if self.rose > 0:
            self.rose -= 1
            return True
        return False
    
#Rose Yellow 
#Rosa amarilla
class RoseYellow(GameElement):
    def __init__(self, x, y):
        rose_path = os.path.join('assets', 'images', 'objects', 'rose-yellow.png')
        super().__init__(x, y, rose_path, constants.FLOWER)
        self.rose_yellow = 1

    def collect(self):
        if self.rose_yellow > 0:
            self.rose_yellow -= 1
            return True
        return False

#Grass
#Pasto 1
class Grass1(GameElement):
    def __init__(self, x, y):
        grass_path = os.path.join('assets', 'images', 'objects', 'grass1.png')
        super().__init__(x, y, grass_path, constants.GRASS_OBJ)

#Grass
#Pasto 2
class Grass2(GameElement):
    def __init__(self, x, y):
        grass_path = os.path.join('assets', 'images', 'objects', 'grass2.png')
        super().__init__(x, y, grass_path, constants.GRASS_OBJ)

#Grass
#Pasto 3
class Grass3(GameElement):
    def __init__(self, x, y):
        grass_path = os.path.join('assets', 'images', 'objects', 'grass3.png')
        super().__init__(x, y, grass_path, constants.GRASS_OBJ)
