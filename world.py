import random
import pygame
import constants
from elements import Tree, SmallStone, Flower, Rose, RoseYellow, Grass1, Grass2, Grass3, FarmLand, Water
import os
from pygame import Surface

class WorldChunk:
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.farmland_tiles = {}
        self.water_tiles = {}

        chunk_seed = hash(f"{x},{y}")
        old_state = random.getstate()
        random.seed(chunk_seed)
        
        # Lista para llevar registro de todos los objetos generados
        all_objects = []
        
        # Generar árboles primero (son los objetos más grandes)
        self.trees = []
        for _ in range(10):
            attempts = 0
            while attempts < 20:  # Intentar hasta 20 veces encontrar posición válida
                tree_x = self.x + random.randint(0, width - constants.TREE)
                tree_y = self.y + random.randint(0, height - constants.TREE)
                if self._is_position_valid(tree_x, tree_y, constants.TREE, all_objects):
                    tree = Tree(tree_x, tree_y)
                    self.trees.append(tree)
                    all_objects.append(tree)
                    break
                attempts += 1
        
        # Generar piedras
        self.small_stones = []
        for _ in range(10):
            attempts = 0
            while attempts < 20:
                stone_x = self.x + random.randint(0, width - constants.SMALL_STONE)
                stone_y = self.y + random.randint(0, height - constants.SMALL_STONE)
                if self._is_position_valid(stone_x, stone_y, constants.SMALL_STONE, all_objects):
                    stone = SmallStone(stone_x, stone_y)
                    self.small_stones.append(stone)
                    all_objects.append(stone)
                    break
                attempts += 1
        
        # Generar rosas amarillas
        self.Roses_Yellow = []
        for _ in range(10):
            attempts = 0
            while attempts < 20:
                rose_x = self.x + random.randint(0, width - constants.FLOWER)
                rose_y = self.y + random.randint(0, width - constants.FLOWER)
                if self._is_position_valid(rose_x, rose_y, constants.FLOWER, all_objects):
                    rose = RoseYellow(rose_x, rose_y)
                    self.Roses_Yellow.append(rose)
                    all_objects.append(rose)
                    break
                attempts += 1
        
        # Generar rosas
        self.Roses = []
        for _ in range(10):
            attempts = 0
            while attempts < 20:
                rose_x = self.x + random.randint(0, width - constants.FLOWER)
                rose_y = self.y + random.randint(0, width - constants.FLOWER)
                if self._is_position_valid(rose_x, rose_y, constants.FLOWER, all_objects):
                    rose = Rose(rose_x, rose_y)
                    self.Roses.append(rose)
                    all_objects.append(rose)
                    break
                attempts += 1
        
        # Generar flores
        self.flowers = []
        for _ in range(10):
            attempts = 0
            while attempts < 20:
                flower_x = self.x + random.randint(0, width - constants.FLOWER)
                flower_y = self.y + random.randint(0, height - constants.FLOWER)
                if self._is_position_valid(flower_x, flower_y, constants.FLOWER, all_objects):
                    flower = Flower(flower_x, flower_y)
                    self.flowers.append(flower)
                    all_objects.append(flower)
                    break
                attempts += 1

        self.grasses1 = []
        for _ in range(10):
            attempts = 0
            while attempts < 20:
                grass1_x = self.x + random.randint(0, width - constants.GRASS_OBJ)
                grass1_y = self.y + random.randint(0, height - constants.GRASS_OBJ)
                if self._is_position_valid(grass1_x, grass1_y, constants.GRASS_OBJ, all_objects):
                    grasss1 = Grass1(grass1_x, grass1_y)
                    self.grasses1.append(grasss1)
                    all_objects.append(grasss1)
                    break
                attempts += 1

        self.grasses2 = []
        for _ in range(10):
            attempts = 0
            while attempts < 20:
                grass2_x = self.x + random.randint(0, width - constants.GRASS_OBJ)
                grass2_y = self.y + random.randint(0, height - constants.GRASS_OBJ)
                if self._is_position_valid(grass2_x, grass2_y, constants.GRASS_OBJ, all_objects):
                    grasss2 = Grass2(grass1_x, grass1_y)
                    self.grasses2.append(grasss2)
                    all_objects.append(grasss2)
                    break
                attempts += 1

        self.grasses3 = []
        for _ in range(10):
            attempts = 0
            while attempts < 20:
                grass3_x = self.x + random.randint(0, width - constants.GRASS_OBJ)
                grass3_y = self.y + random.randint(0, height - constants.GRASS_OBJ)
                if self._is_position_valid(grass3_x, grass3_y, constants.GRASS_OBJ, all_objects):
                    grasss3 = Grass3(grass3_x, grass3_y)
                    self.grasses3.append(grasss3)
                    all_objects.append(grasss3)
                    break
                attempts += 1

        # Generar agua (lagos pequeños)
        if random.random() < constants.WATER_GENERATION_PROBABILITY:
            center_x = self.x + random.randint(0, width)
            center_y = self.y + random.randint(0, height)
            radius = random.randint(3, 8) * constants.GRASS

            # Crear tiles de agua en un patrón circular
            for y_offset in range(-int(radius), int(radius) + 1, constants.GRASS):
                for x_offset in range(-int(radius), int(radius) + 1, constants.GRASS):
                    if (x_offset ** 2 + y_offset ** 2) <= radius ** 2:
                        tile_x = center_x + x_offset
                        tile_y = center_y + y_offset
                        
                        # Verificar que esté dentro del chunk
                        if (self.x <= tile_x < self.x + width and
                            self.y <= tile_y < self.y + height):
                            
                            grid_x = (tile_x // constants.GRASS) * constants.GRASS
                            grid_y = (tile_y // constants.GRASS) * constants.GRASS
                            tile_key = (grid_x, grid_y)
                            
                            # Verificar que no haya objetos importantes en esta posición
                            valid_position = True
                            for obj in all_objects:
                                obj_rect = pygame.Rect(obj.x, obj.y, obj.size, obj.size)
                                water_rect = pygame.Rect(grid_x, grid_y, constants.GRASS, constants.GRASS)
                                if obj_rect.colliderect(water_rect):
                                    valid_position = False
                                    break
                            
                            if valid_position:
                                self.water_tiles[tile_key] = Water(grid_x, grid_y)

        random.setstate(old_state)
    def _is_position_valid(self, x, y, size, existing_objects):
        new_rect = pygame.Rect(x, y, size, size)
        
        for obj in existing_objects:
            obj_rect = pygame.Rect(obj.x, obj.y, obj.size, obj.size)
            if new_rect.colliderect(obj_rect):
                return False
        
        # Verificar colisión con agua
        grid_x = (x // constants.GRASS) * constants.GRASS
        grid_y = (y // constants.GRASS) * constants.GRASS
        if (grid_x, grid_y) in self.water_tiles:
            return False
            
        return True

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
                tile_x = self.x + x * constants.GRASS
                tile_y = self.y + y * constants.GRASS
                screen_x = tile_x - camera_x
                screen_y = tile_y - camera_y

                tile_key = (tile_x, tile_y)
                if tile_key not in self.water_tiles:
                    if tile_key in self.farmland_tiles:
                        self.farmland_tiles[tile_key].draw(screen, camera_x, camera_y)
                    else:
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

        for tile_key, water in self.water_tiles.items():
            water.draw(screen, camera_x, camera_y)
        
    def update(self, dt):
        for water in self.water_tiles.values():
            water.update(dt)

# World class to manage the game world, including trees, stones, flowers
# Clase World para manejar el mundo del juego, incluyendo árboles, piedras y flores
class World:
    def __init__(self, width, height):
        self.chunk_size = constants.WIDTH
        self.active_chunks = {}
        self.inactive_chunks = {}

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
        
        # Activar chunks cercanos (3x3 alrededor del jugador)
        for dx in [-1, 0, 1]:  # Cambiado de [-2,-1,0,1,2] a [-1,0,1] para un área más manejable
            for dy in [-1, 0, 1]:
                chunk_x = current_chunk[0] + dx
                chunk_y = current_chunk[1] + dy
                key = (chunk_x, chunk_y)
                
                if key not in self.active_chunks:
                    # Verificar si el chunk existe en inactive_chunks
                    if key in self.inactive_chunks:
                        # Recuperar el chunk inactivo manteniendo sus cambios
                        self.active_chunks[key] = self.inactive_chunks[key]
                        del self.inactive_chunks[key]
                    else:
                        # Crear un nuevo chunk si no existe
                        x = chunk_x * self.chunk_size
                        y = chunk_y * self.chunk_size
                        self.active_chunks[key] = WorldChunk(x, y, self.chunk_size, self.chunk_size)

        # Desactivar chunks lejanos (fuera del área 3x3)
        chunks_to_move = []
        for chunk_key in list(self.active_chunks.keys()):  # Usamos list() para evitar modificar durante iteración
            distance_x = abs(chunk_key[0] - current_chunk[0])
            distance_y = abs(chunk_key[1] - current_chunk[1])
            if distance_x > 1 or distance_y > 1:  # Cambiado de >2 a >1 para coincidir con el área 3x3
                chunks_to_move.append(chunk_key)

        for chunk_key in chunks_to_move:
            self.inactive_chunks[chunk_key] = self.active_chunks[chunk_key]
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
        
        for chunk in self.active_chunks.values():
            chunk.update(dt)

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
    
    @property
    def water_tiles(self):
        all_water = {}
        for chunk in self.active_chunks.values():
            all_water.update(chunk.water_tiles)
        return all_water

    def add_farmland(self, x, y):
        grid_x = (x // constants.GRASS) * constants.GRASS
        grid_y = (y // constants.GRASS) * constants.GRASS
    
        chunk_key = self.get_chunk_key(x, y)
        chunk = self.active_chunks.get(chunk_key)

        if chunk:   
            for obj in [*chunk.trees, *chunk.small_stones, *chunk.Roses, *chunk.Roses_Yellow]:
                if (grid_x < obj.x + obj.size and grid_x + constants.GRASS > obj.x and
                    grid_y < obj.y + obj.size and grid_y + constants.GRASS > obj.y):
                    return False           

            tile_key = (grid_x, grid_y)
            if tile_key in chunk.water.tiles:
                return False

            if tile_key not in chunk.farmland_tiles:
                chunk.farmland_tiles[tile_key] = FarmLand(grid_x, grid_y)
                return True
        return False
    
    def is_water_at(self, x, y):
        chunk_key = self.get_chunk_key(x, y)
        chunk = self.active_chunks.get(chunk_key)

        if chunk:
            grid_x = (x // constants.GRASS) * constants.GRASS
            grid_y = (y // constants.GRASS) * constants.GRASS

            tile_key = (grid_x, grid_y)
            return tile_key in chunk.water_tiles

        return False

                
        