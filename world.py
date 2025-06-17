import random
import pygame
import constants
from elements import Tree, SmallStone, Flower, Rose, RoseYellow, Grass1, Grass2, Grass3
import os
from pygame import Surface

class WorldChunk:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        chunk_seed = hash(f"{x},{y}")
        old_state = random.getstate()
        random.seed(chunk_seed)
        
        #Yellow Roses
        #Rosas Amarillas
        self.Roses_Yellow = [
            RoseYellow(
            self.x + random.randint(0, width - constants.FLOWER),
            self.y + random.randint(0, width - constants.FLOWER)
            ) for _ in range(10)
        ]
        #Roses
        #Rosas
        self.Roses = [
            Rose(
            self.x + random.randint(0, width - constants.FLOWER),
            self.y + random.randint(0, width - constants.FLOWER)
            ) for _ in range(10)
        ]

        #Flowers
        #Flores
        self.flowers = [
            Flower(
            self.x + random.randint(0, width - constants.FLOWER),
            self.y + random.randint(0, height - constants.FLOWER)
            ) for _ in range(10)
        ]

        #Grass
        #Cesped
        self.grasses1 = [
            Grass1(
                self.x + random.randint(0, width - constants.GRASS_OBJ),
                self.y + random.randint(0, height - constants.GRASS_OBJ)
            ) for _ in range(30)
        ]

        #Grass
        #Cesped
        self.grasses2 = [
            Grass2(
                self.x + random.randint(0, width - constants.GRASS_OBJ),
                self.y + random.randint(0, height - constants.GRASS_OBJ)
            ) for _ in range(30)
        ]

        #Grass
        #Cesped
        self.grasses3 = [
            Grass3(
                self.x + random.randint(0, width - constants.GRASS_OBJ),
                self.y + random.randint(0, height - constants.GRASS_OBJ)
            ) for _ in range(30)
        ]

        #Grass
        #Cesped
        self.trees = [ 
            Tree(
                self.x + random.randint(0, width-constants.TREE),
                self.y + random.randint(0, height-constants.TREE)
            ) for _ in range(10)
        ]

        #Grass
        #Cesped
        self.small_stones = [
        SmallStone(
            self.x + random.randint(0, width-constants.SMALL_STONE),
            self.y + random.randint(0, height-constants.SMALL_STONE)
            ) for _ in range(10)
        ]
            
        random.setstate(old_state)
    
    def draw(self, screen, grass_image, camera_x, camera_y):
    # Dibuja el fondo de césped como un mosaico
    # ...luego dibuja los objetos del mundo como siempre...

        start_x = max(0, (camera_x - self.x - constants.GRASS) // constants.GRASS)
        end_x = min(self.width // constants.GRASS + 1,
                    (camera_x + constants.WIDTH - self.x + constants.GRASS) // constants.GRASS + 1)
        start_y = max(0, (camera_y - self.y - constants.GRASS) // constants.GRASS)
        end_y = min(self.width // constants.GRASS + 1,
                    (camera_y + constants.HEIGHT - self.y + constants.GRASS) // constants.GRASS + 1)
        
        #Generate Elements
        #Generar los elementos
        for y in range(int(start_y), int(end_y)):
            for x in range(int(start_x), int(end_x)):
                screen_x = self.x + x * constants.GRASS - camera_x
                screen_y = self.y + y * constants.GRASS - camera_y
                screen.blit(grass_image, (screen_x, screen_y))

        for stone in self.small_stones:
            stone_screen_x = stone.x - camera_x
            stone_screen_y = stone.y - camera_y
            if (stone_screen_x + stone.size >= 0 and stone_screen_x <= constants.WIDTH and 
                stone_screen_y + stone.size >= 0 and stone_screen_y <= constants.HEIGHT):
                stone.draw(screen, camera_x, camera_y)

        for tree in self.trees:
            tree_screen_x = tree.x - camera_x
            tree_screen_y = tree.y - camera_y
            if (tree_screen_x + tree.size >= 0 and tree_screen_x <= constants.WIDTH and 
                tree_screen_y + tree.size >= 0 and tree_screen_y <= constants.HEIGHT):
                tree.draw(screen, camera_x, camera_y)

        for flower in self.flowers:
            flower_screen_x = flower.x - camera_x
            flower_screen_y = flower.y - camera_y
            if (flower_screen_x + flower.size >= 0 and flower_screen_x <= constants.WIDTH and 
                flower_screen_y + flower.size >= 0 and flower_screen_y <= constants.HEIGHT):
                flower.draw(screen, camera_x, camera_y)

        for flower in self.Roses:
            flower_screen_x = flower.x - camera_x
            flower_screen_y = flower.y - camera_y
            if (flower_screen_x + flower.size >= 0 and flower_screen_x <= constants.WIDTH and 
                flower_screen_y + flower.size >= 0 and flower_screen_y <= constants.HEIGHT):
                flower.draw(screen, camera_x, camera_y)

        for flower in self.Roses_Yellow:
            flower_screen_x = flower.x - camera_x
            flower_screen_y = flower.y - camera_y
            if (flower_screen_x + flower.size >= 0 and flower_screen_x <= constants.WIDTH and 
                flower_screen_y + flower.size >= 0 and flower_screen_y <= constants.HEIGHT):
                flower.draw(screen, camera_x, camera_y)

        for grass in self.grasses1:
            grass_screen_x = grass.x - camera_x
            grass_screen_y = grass.y - camera_y
            if (grass_screen_x + grass.size >= 0 and grass_screen_x <= constants.WIDTH and 
                grass_screen_y + grass.size >= 0 and grass_screen_y <= constants.HEIGHT):
                grass.draw(screen, camera_x, camera_y)

        for grass in self.grasses2:
            grass_screen_x = grass.x - camera_x
            grass_screen_y = grass.y - camera_y
            if (grass_screen_x + grass.size >= 0 and grass_screen_x <= constants.WIDTH and 
                grass_screen_y + grass.size >= 0 and grass_screen_y <= constants.HEIGHT):
                grass.draw(screen, camera_x, camera_y)

        for grass in self.grasses3:
            grass_screen_x = grass.x - camera_x
            grass_screen_y = grass.y - camera_y
            if (grass_screen_x + grass.size >= 0 and grass_screen_x <= constants.WIDTH and 
                grass_screen_y + grass.size >= 0 and grass_screen_y <= constants.HEIGHT):
                grass.draw(screen, camera_x, camera_y)
        
# World class to manage the game world, including trees, stones, flowers
# Clase World para manejar el mundo del juego, incluyendo árboles, piedras y flores
class World:
    def __init__(self, width, height):
        self.chunk_size = constants.WIDTH
        self.active_chunks = {}

        self.view_width = width
        self.view_height = height

        grass_path = os.path.join('assets', 'images', 'objects', 'grass.png')
        self.grass_image = pygame.image.load(grass_path).convert()
        self.grass_rect = pygame.transform.scale(self.grass_image, (constants.GRASS, constants.GRASS))

        #Day and Night Cycle
        #Ciclo de día y noche
        self.current_time = constants.MORNING_TIME
        self.day_overlay = Surface((width, height))
        self.day_overlay.fill(constants.DAY_COLOR)
        self.day_overlay.set_alpha(0)

        self.generate_chunk(0, 0)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                self.generate_chunk(dx, dy)

    def get_chunk_key(self, x, y):
        chunk_x = x // self.chunk_size
        chunk_y = y // self.chunk_size
        return (chunk_x, chunk_y)

    def generate_chunk(self, chunk_x, chunk_y):
        key = (chunk_x, chunk_y)
        if key not in self.active_chunks:
            x = chunk_x * self.chunk_size
            y = chunk_y * self.chunk_size
            self.active_chunks[key] = WorldChunk(x, y, self.chunk_size, self.chunk_size)
    
    def update_chunks(self, player_x, player_y):
        current_chunk = self.get_chunk_key(player_x, player_y)

        # Generate the current chunk if it doesn't exist
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                chunk_x = current_chunk[0] + dx
                chunk_y = current_chunk[1] + dy
                self.generate_chunk(chunk_x, chunk_y)

        #Delete chunks that are too far away
        chunks_to_delete = []
        for chunk_key in self.active_chunks:
            distance_x = abs(chunk_key[0] - current_chunk[0])
            distance_y = abs(chunk_key[1] - current_chunk[1])
            if distance_x > 2 or distance_y > 2:
                chunks_to_delete.append(chunk_key)

        for chunk_key in chunks_to_delete:  
            del self.active_chunks[chunk_key]

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
    def draw(self, screen, camera_x, camera_y):
        for chunk in self.active_chunks.values():
                chunk.draw(screen, self.grass_rect, camera_x, camera_y)
            
        for flower in self.flowers:
            flower.draw(screen, camera_x, camera_y)

        # Draw the day overlay
        # Dibuja la superposición de día/noche
        screen.blit(self.day_overlay, (0, 0))

    # Draw the inventory prompt on the screen
    # Dibuja el mensaje para abrir el inventario en la pantalla
    def draw_inventory(self, screen):
        font = pygame.font.Font(None, 20)
        inventory_text = font.render("Press 'E' to open inventory", True, constants.WHITE)
        screen.blit(inventory_text, (10, 10))

    @property
    def trees(self):
        all_trees=[]
        for chunk in self.active_chunks.values():
            all_trees.extend(chunk.trees)
        return all_trees
    
    @property
    def small_stones(self):
        all_stones = []
        for chunk in self.active_chunks.values():
            all_stones.extend(chunk.small_stones)
        return all_stones
    
    @property
    def flowers(self):
        all_flowers = []
        for chunk in self.active_chunks.values():
            all_flowers.extend(chunk.flowers)
        return all_flowers
    
    @property
    def roses(self):
        all_roses = []
        for chunk in self.active_chunks.values():
            all_roses.extend(chunk.Roses)
        return all_roses
    
    @property
    def roses_yellow(self):
        all_yellow = []
        for chunk in self.active_chunks.values():
            all_yellow.extend(chunk.Roses_Yellow)
        return all_yellow

    @property
    def grasses1(self):
        all_grasses = []
        for chunk in self.active_chunks.values():
            all_grasses.extend(chunk.grasses1)
        return all_grasses

    @property
    def grasses2(self):
        all_grasses = []
        for chunk in self.active_chunks.values():
            all_grasses.extend(chunk.grasses2)
        return all_grasses

    @property
    def grasses3(self):
        all_grasses = []
        for chunk in self.active_chunks.values():
            all_grasses.extend(chunk.grasses3)
        return all_grasses