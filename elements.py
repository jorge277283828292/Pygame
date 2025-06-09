import pygame
import constants
import os

class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wood = 5

        tree_path = os.path.join('assets', 'images', 'objects', 'tree.png')
        self.image = pygame.image.load(tree_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.TREE, constants.TREE))
        self.size = self.image.get_width()


    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class SmallStone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stone = 1

        tree_path = os.path.join('assets', 'images', 'objects', 'stone.png')
        self.image = pygame.image.load(tree_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.SMALL_STONE, constants.SMALL_STONE))
        self.size = self.image.get_width()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))