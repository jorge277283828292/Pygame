import random
import pygame
import constants
from elements import Tree, SmallStone, Flower, Rose, RoseYellow, House, Grass1, Grass2, Grass3
import os

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.trees = [Tree(random.randint(0, width-constants.TREE),
                           random.randint(0, height-constants.TREE)) for _ in range(20)]
        
        self.small_stones = [SmallStone(random.randint(0, width - constants.SMALL_STONE),
                           random.randint(0, height - constants.SMALL_STONE)) for _ in range(20)]
        
        self.flowers = (
            [Flower(random.randint(0, width - constants.FLOWER), random.randint(0, height - constants.FLOWER)) for _ in range(15)] +
            [Rose(random.randint(0, width - constants.FLOWER), random.randint(0, height - constants.FLOWER)) for _ in range(5)] +
            [RoseYellow(random.randint(0, width - constants.FLOWER), random.randint(0, height - constants.FLOWER)) for _ in range(5)] +
            [Grass1(random.randint(0, width - constants.GRASS_OBJ), random.randint(0, height - constants.GRASS_OBJ)) for _ in range(20)] +
            [Grass2(random.randint(0, width - constants.GRASS_OBJ), random.randint(0, height - constants.GRASS_OBJ)) for _ in range(20)] +
            [Grass3(random.randint(0, width - constants.GRASS_OBJ), random.randint(0, height - constants.GRASS_OBJ)) for _ in range(20)]
        )
        
        self.house = [House(
        self.width - constants.HOUSE,                # posición x: borde derecho menos el ancho de la casa
        self.height // 2 - constants.HOUSE // 2      # posición y: centro vertical
    )
]
        
        grass_path = os.path.join('assets', 'images', 'objects', 'grass.png')
        self.grass_image = pygame.image.load(grass_path).convert()
        self.grass_rect = pygame.transform.scale(self.grass_image, (constants.GRASS, constants.GRASS))

    def draw(self, screen):
        for y in range(0, self.height, constants.GRASS):
            for x in range(0, self.width, constants.GRASS):
                screen.blit(self.grass_rect, (x, y))
            
        for flower in self.flowers:
            flower.draw(screen)

        for stone in self.small_stones:
            stone.draw(screen)

        for tree in self.trees:
            tree.draw(screen)

        for house in self.house:
            house.draw(screen)

    def draw_inventory(self, screen):
        font = pygame.font.Font(None, 20)
        inventory_text = font.render("Press 'E' to open inventory", True, constants.WHITE)
        screen.blit(inventory_text, (10, 10))