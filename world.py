import random
import pygame
import constants
from elements import Tree, SmallStone, Flower, Rose, RoseYellow, Grass1, Grass2, Grass3
import os
from pygame import Surface

# World class to manage the game world, including trees, stones, flowers
# Clase World para manejar el mundo del juego, incluyendo árboles, piedras y flores
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

        grass_path = os.path.join('assets', 'images', 'objects', 'grass.png')
        self.grass_image = pygame.image.load(grass_path).convert()
        self.grass_rect = pygame.transform.scale(self.grass_image, (constants.GRASS, constants.GRASS))

        #Day and Night Cycle
        #Ciclo de día y noche
        self.current_time = constants.MORNING_TIME
        self.day_overlay = Surface((width, height))
        self.day_overlay.fill(constants.DAY_COLOR)
        self.day_overlay.set_alpha(0)

    #Update the time 
    #Actualiza el tiempo (día/noche)
    def update_time(self, dt):
        self.current_time = (self.current_time + dt) % constants.DAY_LENGTH
        hour = (self.current_time / constants.DAY_LENGTH) * 24

        # Amanecer suave (6:00 a 6:30)
        # Transición suave de amanecer
        if 6 <= hour < 6.5:
            progress = (hour - 6) / 0.5
            dawn_color = (255, 220, 120)
            day_color = constants.DAY_COLOR
            r = int(dawn_color[0] + (day_color[0] - dawn_color[0]) * progress)
            g = int(dawn_color[1] + (day_color[1] - dawn_color[1]) * progress)
            b = int(dawn_color[2] + (day_color[2] - dawn_color[2]) * progress)
            self.day_overlay.fill((r, g, b))
            alpha = int(100 * (1 - progress))
            self.day_overlay.set_alpha(alpha)

        #Coomplete day (6:30 a 18:00)
        #Día completo
        elif 6.5 <= hour < constants.NIGHT_START:
            self.day_overlay.fill(constants.DAY_COLOR)
            self.day_overlay.set_alpha(0)

        #Afternoon (18:00 a 18:30)
        #Atardecer (transición a noche)
        elif constants.NIGHT_START <= hour < constants.NIGHT_END:
            progress = (hour - constants.NIGHT_START) / (constants.NIGHT_END - constants.NIGHT_START)
            day_color = constants.DAY_COLOR
            night_color = constants.NIGHT_COLOR
            r = int(day_color[0] + (night_color[0] - day_color[0]) * progress)
            g = int(day_color[1] + (night_color[1] - day_color[1]) * progress)
            b = int(day_color[2] + (night_color[2] - day_color[2]) * progress)
            self.day_overlay.fill((r, g, b))
            alpha = int(constants.MAX_NIGHT_ALPHA * progress)
            self.day_overlay.set_alpha(alpha)

        # Night (18:30 a 6:00)
        #Noche completa
        else:
            self.day_overlay.fill(constants.NIGHT_COLOR)
            self.day_overlay.set_alpha(constants.MAX_NIGHT_ALPHA)

    # Draw the world elements on the screen
    # Dibuja los elementos del mundo en la pantalla
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

        # Draw the day overlay
        # Dibuja la superposición de día/noche
        screen.blit(self.day_overlay, (0, 0))

    # Draw the inventory prompt on the screen
    # Dibuja el mensaje para abrir el inventario en la pantalla
    def draw_inventory(self, screen):
        font = pygame.font.Font(None, 20)
        inventory_text = font.render("Press 'E' to open inventory", True, constants.WHITE)
        screen.blit(inventory_text, (10, 10))