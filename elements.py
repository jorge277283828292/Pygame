import pygame
import constants
import os
import math
import random

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

class FarmLand:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_watered = False
        self.growth_stage = 0  # 0 = tierra arada, 5 = listo para cosechar
        self.last_update_time = pygame.time.get_ticks()
        self.size = constants.GRASS
        self.images = self._load_images()

    def _load_images(self):
        images = {}
        for i in range(1, 7):
            try:
                path = os.path.join('assets', 'images', 'objects', 'Farm', f'Farmland {i}.png')
                img = pygame.image.load(path).convert_alpha()
                images[i] = pygame.transform.scale(img, (self.size, self.size))
            except:
                # Crear imagen de placeholder si no existe
                surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                color = (139, 69, 19) if i == 1 else (0, 100 + i*20, 0)
                surf.fill(color)
                images[i] = surf
        return images

    def water(self):
        if not self.is_watered:
            self.is_watered = True
            self.last_update_time = pygame.time.get_ticks()
            return True
        return False

    def update(self, current_time):
        if self.is_watered and self.growth_stage < 5:
            if current_time - self.last_update_time > constants.FARM_GROWTH_TIME:
                self.growth_stage += 1
                self.last_update_time = current_time
                # El agua se evapora después del último crecimiento
                if self.growth_stage >= 5:
                    self.is_watered = False

    def harvest(self):
        if self.growth_stage == 5:
            self.growth_stage = 0
            self.is_watered = False
            return True
        return False

    def draw(self, screen, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Dibujar la etapa actual
        image_key = min(6, max(1, self.growth_stage + 1))
        screen.blit(self.images[image_key], (screen_x, screen_y))
        
    def water(self):
        if not self.is_watered:
            self.is_watered = True
            self.last_update_time= pygame.time.get_ticks()
            return True
        
    def update(self, current_time):
        if self.is_watered and self.growth_stage < 5:
            if self.growth_stage == 0:
                self.growth_stage = 1   
            if current_time - self.last_update_time > 10000:
                self.growth_stage = min(5, self.growth_stage + 1)
                self.last_update_time = current_time

    def harvest(self):
        if self.growth_stage >= 5:
            self.growth_stage= 0
            self.is_watered = False
            return True
        return False

class Water:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = constants.GRASS
        self.time = 0

    def update(self, dt):
        self.time += dt * 0.002

    def draw(self, screen, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        if (screen_x + self.size >= 0 and screen_x <= constants.WIDTH and
                screen_y + self.size >= 0 and screen_y <= constants.HEIGHT):
            water_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            water_surface.fill((*constants.WATER_COLOR, 180))
            
            wave_offset = int(math.sin(self.time) * 1.5)
            screen.blit(water_surface, (screen_x, screen_y + wave_offset))