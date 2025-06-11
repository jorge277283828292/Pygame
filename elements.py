import pygame
import constants
import os

#Master Class
class GameElement:
    def __init__(self, x, y, image_path, size):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.size = self.image.get_width()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

#Tree
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

#House
class House(GameElement):
    def __init__(self, x, y):
        house_path = os.path.join('assets', 'images', 'objects', 'house.png')
        super().__init__(x, y, house_path, constants.HOUSE)

#Grass
class Grass1(GameElement):
    def __init__(self, x, y):
        grass_path = os.path.join('assets', 'images', 'objects', 'grass1.png')
        super().__init__(x, y, grass_path, constants.GRASS_OBJ)

#Grass
class Grass2(GameElement):
    def __init__(self, x, y):
        grass_path = os.path.join('assets', 'images', 'objects', 'grass2.png')
        super().__init__(x, y, grass_path, constants.GRASS_OBJ)

#Grass
class Grass3(GameElement):
    def __init__(self, x, y):
        grass_path = os.path.join('assets', 'images', 'objects', 'grass3.png')
        super().__init__(x, y, grass_path, constants.GRASS_OBJ)
