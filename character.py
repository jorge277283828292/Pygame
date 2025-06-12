import pygame
import constants
import os
from elements import Flower, Rose, RoseYellow

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = {"wood" : 0, 
                          "stone": 0,
                          "flower": 0,
                          "rose": 0,
                          "rose_yellow": 0
                          }
        
        image_path = os.path.join("assets", "images", "character", "Imagen1.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.PLAYER, constants.PLAYER))
        self.size = self.image.get_width()

        self.item_images = {
            "wood": self.load_item_images("wood.png"),
            "stone": self.load_item_images("stone.png"),
            "flower": self.load_item_images("flowers.png"), 
            "rose": self.load_item_images("rose.png"),
            "rose_yellow": self.load_item_images("rose-yellow.png")
        }
        
        self.energy = constants.MAX_ENERGY
        self.food = constants.MAX_FOOD
        self.thirst = constants.MAX_THIRST

    def load_item_images(self, filename):
        path = os.path.join("assets", "images", "objects", filename)
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (24, 24))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.draw_status_bars(screen)

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

        #Whhen he moves, he loses energy
        self.update_energy(-0.1)

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

        #Trees
        for tree in world.trees:
            if self.is_near(tree):
                if tree.chop():
                    self.inventory["wood"] += 1
                    if tree.wood == 0:
                        world.trees.remove(tree)
                    return
        #Stones
        for stone in world.small_stones:
            if self.is_near(stone):
                if stone.mine():
                    self.inventory["stone"] += 1
                if stone.stone == 0:
                    world.small_stones.remove(stone)
                return
        
        #Flowers
        for flower in world.flowers:
            if self.is_near(flower):
                if isinstance(flower, Flower):
                    if flower.collect():
                        self.inventory["flower"] += 1
                    if flower.flower == 0:
                        world.flowers.remove(flower)
                    return
                elif isinstance(flower, Rose):
                    if flower.collect():
                        self.inventory["rose"] += 1
                    if flower.rose == 0:
                        world.flowers.remove(flower)
                    return
                elif isinstance(flower, RoseYellow):
                    if flower.collect():
                        self.inventory["rose_yellow"] += 1
                    if flower.rose_yellow == 0:
                        world.flowers.remove(flower)
                    return
            
    def draw_inventory(self, screen):
        background = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
        background.fill((0, 0, 0, 128))
        screen.blit(background, (0, 0))  # Fondo semitransparente

        font = pygame.font.Font(None, 36)
        title = font.render("Inventory", True, constants.WHITE) 
        screen.blit(title, (constants.WIDTH // 2 - title.get_width() // 2, 20))

        item_font = pygame.font.Font(None, 24)
        y_offset = 80
        for item, quantity in self.inventory.items():
            if quantity > 0:
                screen.blit(self.item_images[item], (constants.WIDTH // 2 - 60, y_offset))
                text = item_font.render(f"{item.capitalize()}: {quantity}", True, constants.WHITE)
                screen.blit(text, (constants.WIDTH // 2 - 20, y_offset + 10)) 
                y_offset += 40
        
        close_text = font.render("Press 'E' to close inventory", True, constants.WHITE)

        screen.blit(close_text, (constants.WIDTH // 2 - close_text.get_width() // 2, constants.HEIGHT - 40))    

    def update_energy(self, amount):
        self.energy = max(0, min(self.energy + amount, constants.MAX_ENERGY))

    def update_food(self, amount):
        self.food = max(0, min(self.food + amount, constants.MAX_FOOD))
    
    def update_thirst(self, amount):
        self.thirst = max(0, min(self.thirst + amount, constants.MAX_THIRST))

    def draw_status_bars(self, screen):
        bar_width = 100
        bar_height = 10
        x_offset = 10
        y_offset = 10

        # ENERGY BAR
        pygame.draw.rect(screen, constants.BAR_BACKGROUND_COLOR, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constants.ENERGY_COLOR, (x_offset, y_offset, bar_width * (self.energy / constants.MAX_ENERGY), bar_height))
        y_offset += bar_height + 5

        # THIRST BAR
        pygame.draw.rect(screen, constants.BAR_BACKGROUND_COLOR, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constants.THIRST_COLOR, (x_offset, y_offset, bar_width * (self.thirst / constants.MAX_THIRST), bar_height))
        y_offset += bar_height + 5

        # FOOD BAR
        pygame.draw.rect(screen, constants.BAR_BACKGROUND_COLOR, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constants.FOOD_COLOR, (x_offset, y_offset, bar_width * (self.food / constants.MAX_FOOD), bar_height))

    def update_status(self):
        self.update_energy(-0.01)  # Reduce energía con el tiempo
        self.update_food(-0.02)

        if self.food < constants.MAX_FOOD * 0.2 or self.thirst < constants.MAX_THIRST * 0.2:
            self.update_energy(-0.05)	
        else:
            self.update_energy(0.01)
