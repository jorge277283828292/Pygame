import pygame
import constants
import os

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = {"wood" : 0, "stone": 0}
        image_path = os.path.join("assets", "images", "character", "Imagen1.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.PLAYER, constants.PLAYER))
        self.size = self.image.get_width()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, dx, dy, world):
        new_x = self.x + dx
        new_y = self.y + dy
        
        for tree in world.trees:
            if self.check_collision(new_x, new_y, tree):
                return
            
        self.x = new_x
        self.y = new_y
        self.x = max(0, min(self.x, constants.WIDTH - self.size))
        self.y = max(0, min(self.y, constants.HEIGHT - self.size))

    def check_collision(self, x, y, obj):
        shrink = 0.25  # Reduce el área de colisión en un 25%
        obj_x = obj.x + obj.size * shrink / 2
        obj_y = obj.y + obj.size * shrink / 2
        obj_size = obj.size * (1 - shrink)
        return (
            x < obj_x + obj_size and
            x + self.size > obj_x and
            y < obj_y + obj_size and
            y + self.size > obj_y
        )

    def is_near(self, obj):
        return (
            abs(self.x - obj.x) <= max(self.size, obj.size) + 5 and
            abs(self.y - obj.y) <= max(self.size, obj.size) + 5
        )
    
    def interact(self, world):
        for tree in world.trees:
            if self.is_near(tree):
                if tree.chop():
                    self.inventory["wood"] += 1
                    if tree.wood == 0:
                        world.trees.remove(tree)
                    return
    
        for stone in world.small_stones:
            if self.is_near(stone):
                if stone.mine():
                    self.inventory["stone"] += 1
                if stone.stone == 0:
                    world.small_stones.remove(stone)
                return

