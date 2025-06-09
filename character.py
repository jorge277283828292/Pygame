import pygame
import constants
import os

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = {"wood" : 0 }
        image_path = os.path.join("assets", "images", "character", "Imagen1.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.PLAYER, constants.PLAYER))
        self.size = self.image.get_width()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, dx, dy):
        self.y += dy
        self.x += dx