import random
import pygame
import constants
from elements import Tree, SmallStone, Flower, Rose, RoseYellow, Grass1, Grass2, Grass3, FarmLand, Water
import os
from pygame import Surface

# WorldChunk class to manage elements within a portion of the world
# Clase WorldChunk para manejar los elementos dentro de un trozo del mundo
class WorldChunk:
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.farmland_tiles = {}
        self.water_tiles = {}
        # Set to store the coordinates of forbidden zones (like water)
        # Conjunto para almacenar las coordenadas de las zonas prohibidas (como el agua)
        self.forbidden_zones = set() 

        # Seed the random number generator based on chunk coordinates
        # Semilla del generador de números aleatorios basada en las coordenadas del chunk
        chunk_seed = hash(f"{x},{y}")
        # Save the current state of the generator to restore it later
        # Guarda el estado actual del generador para restaurarlo después
        old_state = random.getstate()
        random.seed(chunk_seed)
        
        # First, we generate water and mark forbidden zones
        # Primero generamos el agua y marcamos las zonas prohibidas
        self._generate_water(width, height)
    
        # Then we generate the objects, avoiding the marked water zones.
        # This part was repeated in the original code and has been streamlined.
        # Luego generamos los objetos, evitando las zonas de agua marcadas.
        # Esta parte estaba repetida en el código original y ha sido simplificada.
        self._generate_objects(width, height)

        # Restore the original state of the random number generator
        # Restaura el estado original del generador de números aleatorios
        random.setstate(old_state)
        
        # The object generation block that was here was repetitive and has been moved to _generate_objects
        # and the call to _generate_objects already handles it.
        # El bloque de generación de objetos que estaba aquí era repetitivo y ha sido movido a _generate_objects
        # y la llamada a _generate_objects ya lo maneja.

    def clear_objects_in_water(self):
        """Removes small objects that ended up inside the generated water"""
        """Elimina objetos pequeños que quedaron dentro del agua generada"""
        objects_to_remove = []
        
        # Iterate over copies of the lists to avoid issues when modifying the list during iteration
        # Iterar sobre copias de las listas para evitar problemas al modificar la lista durante la iteración
        for tree in self.trees[:]:
            grid_x = (tree.x // constants.GRASS) * constants.GRASS
            grid_y = (tree.y // constants.GRASS) * constants.GRASS
            # If the tree's center is in a water tile, mark it for removal
            # Si el centro del árbol está en una casilla de agua, marcar para eliminar
            if (grid_x, grid_y) in self.water_tiles:
                objects_to_remove.append(tree)
        
        for stone in self.small_stones[:]:
            grid_x = (stone.x // constants.GRASS) * constants.GRASS
            grid_y = (stone.y // constants.GRASS) * constants.GRASS
            # If the stone's center is in a water tile, mark it for removal
            # Si el centro de la piedra está en una casilla de agua, marcar para eliminar
            if (grid_x, grid_y) in self.water_tiles:
                objects_to_remove.append(stone)
        
        # Remove the marked objects from their respective lists
        # Eliminar los objetos marcados de sus respectivas listas
        for obj in objects_to_remove:
            if obj in self.trees:
                self.trees.remove(obj)
            elif obj in self.small_stones:
                self.small_stones.remove(obj)
            elif obj in self.flowers:
                self.flowers.remove(obj)
            elif obj in self.Roses:
                self.Roses.remove(obj)
            elif obj in self.Roses_Yellow:
                self.Roses_Yellow.remove(obj)
        # Note: 'grasses' would also need to be handled here if they should be removed from water
        # Nota: Las "grasses" también deberían manejarse aquí si deben ser removidas del agua.

    def _is_position_valid(self, x, y, size, existing_objects):
        # Check collision with forbidden zones (water)
        # Verificar colisión con zonas prohibidas (agua)
        grid_x = (x // constants.GRASS) * constants.GRASS
        grid_y = (y // constants.GRASS) * constants.GRASS
        # If the position coincides with a forbidden zone, it's not valid
        # Si la posición coincide con una zona prohibida, no es válida
        if (grid_x, grid_y) in self.forbidden_zones:
            return False
        
        # Check collision with other existing objects
        # Verificar colisión con otros objetos ya existentes
        new_rect = pygame.Rect(x, y, size, size)
        for obj in existing_objects:
            obj_rect = pygame.Rect(obj.x, obj.y, obj.size, obj.size)
            # If the new object collides with an existing one, it's not valid
            # Si el nuevo objeto colisiona con uno existente, no es válida
            if new_rect.colliderect(obj_rect):
                return False
                
        return True

    def draw(self, screen, grass_image, camera_x, camera_y):
        # Draw the grass background as a tile
        # Dibuja el fondo de césped como un mosaico
        # Calculate the range of visible tiles on the screen to optimize drawing
        # Calcula el rango de tiles visibles en la pantalla para optimizar el dibujo
        start_x = max(0, (camera_x - self.x - constants.GRASS) // constants.GRASS)
        end_x = min(self.width // constants.GRASS + 1,
                            (camera_x + constants.WIDTH - self.x + constants.GRASS) // constants.GRASS + 1)
        start_y = max(0, (camera_y - self.y - constants.GRASS) // constants.GRASS)
        end_y = min(self.width // constants.GRASS + 1,
                            (camera_y + constants.HEIGHT - self.y + constants.GRASS) // constants.GRASS + 1)
        
        # Generate terrain elements (grass and farmland)
        # Generar elementos del terreno (césped y tierra de cultivo)
        for y in range(int(start_y), int(end_y)):
            for x in range(int(start_x), int(end_x)):
                tile_x = self.x + x * constants.GRASS
                tile_y = self.y + y * constants.GRASS
                screen_x = tile_x - camera_x
                screen_y = tile_y - camera_y

                tile_key = (tile_x, tile_y)
                # If the tile is not water
                # Si la casilla no es de agua
                if tile_key not in self.water_tiles:
                    # If the tile is farmland, draw the farmland
                    # Si la casilla es de tierra de cultivo, dibuja la tierra de cultivo
                    if tile_key in self.farmland_tiles:
                        self.farmland_tiles[tile_key].draw(screen, camera_x, camera_y)
                    # Otherwise, draw grass
                    # Si no, dibuja el césped
                    else:
                        screen.blit(grass_image, (screen_x, screen_y))

        # Draw stones
        # Dibujar piedras
        for stone in self.small_stones:
            stone_screen_x = stone.x - camera_x
            stone_screen_y = stone.y - camera_y
            # Draw the stone only if it's visible on screen
            # Dibuja la piedra solo si está visible en pantalla
            if (stone_screen_x + stone.size >= 0 and stone_screen_x <= constants.WIDTH and 
                stone_screen_y + stone.size >= 0 and stone_screen_y <= constants.HEIGHT):
                stone.draw(screen, camera_x, camera_y)

        # Draw trees
        # Dibujar árboles
        for tree in self.trees:
            tree_screen_x = tree.x - camera_x
            tree_screen_y = tree.y - camera_y
            # Draw the tree only if it's visible on screen
            # Dibuja el árbol solo si está visible en pantalla
            if (tree_screen_x + tree.size >= 0 and tree_screen_x <= constants.WIDTH and 
                tree_screen_y + tree.size >= 0 and tree_screen_y <= constants.HEIGHT):
                tree.draw(screen, camera_x, camera_y)

        # Draw flowers
        # Dibujar flores
        for flower in self.flowers:
            flower_screen_x = flower.x - camera_x
            flower_screen_y = flower.y - camera_y
            # Draw the flower only if it's visible on screen
            # Dibuja la flor solo si está visible en pantalla
            if (flower_screen_x + flower.size >= 0 and flower_screen_x <= constants.WIDTH and 
                flower_screen_y + flower.size >= 0 and flower_screen_y <= constants.HEIGHT):
                flower.draw(screen, camera_x, camera_y)

        # Draw roses
        # Dibujar rosas
        for rose_obj in self.Roses: # Renamed variable to avoid confusion with general 'flower'
            rose_screen_x = rose_obj.x - camera_x
            rose_screen_y = rose_obj.y - camera_y
            # Draw the rose only if it's visible on screen
            # Dibuja la rosa solo si está visible en pantalla
            if (rose_screen_x + rose_obj.size >= 0 and rose_screen_x <= constants.WIDTH and 
                rose_screen_y + rose_obj.size >= 0 and rose_screen_y <= constants.HEIGHT):
                rose_obj.draw(screen, camera_x, camera_y)

        # Draw yellow roses
        # Dibujar rosas amarillas
        for yellow_rose_obj in self.Roses_Yellow: # Renamed variable for clarity
            yellow_rose_screen_x = yellow_rose_obj.x - camera_x
            yellow_rose_screen_y = yellow_rose_obj.y - camera_y
            # Draw the yellow rose only if it's visible on screen
            # Dibuja la rosa amarilla solo si está visible en pantalla
            if (yellow_rose_screen_x + yellow_rose_obj.size >= 0 and yellow_rose_screen_x <= constants.WIDTH and 
                yellow_rose_screen_y + yellow_rose_obj.size >= 0 and yellow_rose_screen_y <= constants.HEIGHT):
                yellow_rose_obj.draw(screen, camera_x, camera_y)

        # Draw grass type 1
        # Dibujar hierba tipo 1
        for grass in self.grasses1:
            grass_screen_x = grass.x - camera_x
            grass_screen_y = grass.y - camera_y
            # Draw the grass only if it's visible on screen
            # Dibuja la hierba solo si está visible en pantalla
            if (grass_screen_x + grass.size >= 0 and grass_screen_x <= constants.WIDTH and 
                grass_screen_y + grass.size >= 0 and grass_screen_y <= constants.HEIGHT):
                grass.draw(screen, camera_x, camera_y)

        # Draw grass type 2
        # Dibujar hierba tipo 2
        for grass in self.grasses2:
            grass_screen_x = grass.x - camera_x
            grass_screen_y = grass.y - camera_y
            # Draw the grass only if it's visible on screen
            # Dibuja la hierba solo si está visible en pantalla
            if (grass_screen_x + grass.size >= 0 and grass_screen_x <= constants.WIDTH and 
                grass_screen_y + grass.size >= 0 and grass_screen_y <= constants.HEIGHT):
                grass.draw(screen, camera_x, camera_y)

        # Draw grass type 3
        # Dibujar hierba tipo 3
        for grass in self.grasses3:
            grass_screen_x = grass.x - camera_x
            grass_screen_y = grass.y - camera_y
            # Draw the grass only if it's visible on screen
            # Dibuja la hierba solo si está visible en pantalla
            if (grass_screen_x + grass.size >= 0 and grass_screen_x <= constants.WIDTH and 
                grass_screen_y + grass.size >= 0 and grass_screen_y <= constants.HEIGHT):
                grass.draw(screen, camera_x, camera_y)

        # Draw water tiles
        # Dibujar los tiles de agua
        for tile_key, water in self.water_tiles.items():
            water.draw(screen, camera_x, camera_y)
        
    def update(self, dt):
        # Update the state of water tiles (e.g., animation)
        # Actualiza el estado de los tiles de agua (ej. animación)
        for water in self.water_tiles.values():
            water.update(dt)

    def _generate_water(self, width, height):
        # Probability of generating a lake in this chunk
        # Probabilidad de generar un lago en este chunk
        if random.random() < constants.WATER_GENERATION_PROBABILITY:
            lake_type = random.choice(['small', 'medium', 'large'])
            
            # Define radius and number of lakes based on type
            # Definir el radio y el número de lagos según el tipo
            if lake_type == 'small':
                radius = random.randint(2, 4) * constants.GRASS
                num_lakes = random.randint(1, 3)
            elif lake_type == 'medium':
                radius = random.randint(4, 6) * constants.GRASS
                num_lakes = random.randint(1, 2)
            else:  # large
                radius = random.randint(6, 10) * constants.GRASS
                num_lakes = 1

            # Generate each lake
            # Generar cada lago
            for _ in range(num_lakes):
                # Calculate the lake's center within the chunk
                # Calcular el centro del lago dentro del chunk
                center_x = self.x + random.randint(radius, width - radius)
                center_y = self.y + random.randint(radius, height - radius)
                
                # Generate organic lake shape using a circle algorithm with variations
                # Generar forma orgánica del lago usando un algoritmo de círculo con variaciones
                for dy in range(-radius, radius + constants.GRASS, constants.GRASS):
                    for dx in range(-radius, radius + constants.GRASS, constants.GRASS):
                        distance = (dx**2 + dy**2)**0.5
                        # Apply a random variation to the edge for a more irregular shape
                        # Aplicar una variación aleatoria al borde para una forma más irregular
                        if distance <= radius * (0.7 + random.random() * 0.6):  
                            tile_x = center_x + dx
                            tile_y = center_y + dy
                            
                            # Ensure the water tile is within the chunk's boundaries
                            # Asegurarse de que el tile de agua está dentro de los límites del chunk
                            if (self.x <= tile_x < self.x + width and
                                self.y <= tile_y < self.y + height):
                                
                                grid_x = (tile_x // constants.GRASS) * constants.GRASS
                                grid_y = (tile_y // constants.GRASS) * constants.GRASS
                                tile_key = (grid_x, grid_y)
                                
                                # Mark this zone as forbidden for the generation of other objects
                                # Marcar esta zona como prohibida para la generación de otros objetos
                                self.forbidden_zones.add((grid_x, grid_y))
                                # Add the water tile to the chunk's water tiles dictionary
                                # Añadir el tile de agua al diccionario de tiles de agua del chunk
                                self.water_tiles[tile_key] = Water(grid_x, grid_y)
    
    def _generate_objects(self, width, height):
        # List to keep track of generated objects in this chunk to prevent overlaps
        # Lista para mantener un registro de los objetos generados en este chunk para evitar solapamientos
        all_objects = []
        
        # Generate trees
        # Generar árboles
        self.trees = []
        for _ in range(10):  # Try to generate 10 trees
            attempts = 0
            while attempts < 20: # Limit attempts to avoid infinite loops
                # Calculate a random position for the tree within the chunk
                # Calcular una posición aleatoria para el árbol dentro del chunk
                tree_x = self.x + random.randint(0, width - constants.TREE)
                tree_y = self.y + random.randint(0, height - constants.TREE)
                
                # Check that the position is not in a forbidden zone (water) and does not collide with other objects
                # Verificar que la posición no esté en una zona prohibida (agua) y que no colisione con otros objetos
                grid_x = (tree_x // constants.GRASS) * constants.GRASS
                grid_y = (tree_y // constants.GRASS) * constants.GRASS
                if (grid_x, grid_y) not in self.forbidden_zones and \
                   self._is_position_valid(tree_x, tree_y, constants.TREE, all_objects):
                    tree = Tree(tree_x, tree_y)
                    self.trees.append(tree)
                    all_objects.append(tree) # Add the tree to the list of generated objects
                    break # Exit the attempts loop once a valid position is found
                attempts += 1 # Increment attempts if the position is not valid
        
        # Generate stones (follows the same pattern as trees)
        # Generar piedras (sigue el mismo patrón que los árboles)
        self.small_stones = []
        for _ in range(10):
            attempts = 0
            while attempts < 20:
                stone_x = self.x + random.randint(0, width - constants.SMALL_STONE)
                stone_y = self.y + random.randint(0, height - constants.SMALL_STONE)
                grid_x = (stone_x // constants.GRASS) * constants.GRASS
                grid_y = (stone_y // constants.GRASS) * constants.GRASS
                if (grid_x, grid_y) not in self.forbidden_zones and \
                   self._is_position_valid(stone_x, stone_y, constants.SMALL_STONE, all_objects):
                    stone = SmallStone(stone_x, stone_y)
                    self.small_stones.append(stone)
                    all_objects.append(stone)
                    break
                attempts += 1
        
        # Generate flowers (follows the same pattern)
        # Generar flores (sigue el mismo patrón)
        self.flowers = []
        for _ in range(10):
            attempts = 0
            while attempts < 20:
                flower_x = self.x + random.randint(0, width - constants.FLOWER)
                flower_y = self.y + random.randint(0, height - constants.FLOWER)
                grid_x = (flower_x // constants.GRASS) * constants.GRASS
                grid_y = (flower_y // constants.GRASS) * constants.GRASS
                if (grid_x, grid_y) not in self.forbidden_zones and \
                   self._is_position_valid(flower_x, flower_y, constants.FLOWER, all_objects):
                    flower = Flower(flower_x, flower_y)
                    self.flowers.append(flower)
                    all_objects.append(flower)
                    break
                attempts += 1

        # Generate yellow roses (follows the same pattern)
        # Generar rosas amarillas (sigue el mismo patrón)
        self.Roses_Yellow = []
        for _ in range(10):
            attempts = 0
            while attempts < 20:
                rose_x = self.x + random.randint(0, width - constants.FLOWER) # Assumes rose size is equal to flower size
                rose_y = self.y + random.randint(0, height - constants.FLOWER)
                grid_x = (rose_x // constants.GRASS) * constants.GRASS
                grid_y = (rose_y // constants.GRASS) * constants.GRASS
                if (grid_x, grid_y) not in self.forbidden_zones and \
                   self._is_position_valid(rose_x, rose_y, constants.FLOWER, all_objects):
                    rose = RoseYellow(rose_x, rose_y)
                    self.Roses_Yellow.append(rose)
                    all_objects.append(rose)
                    break
                attempts += 1
        
        # Generate roses (follows the same pattern)
        # Generar rosas (sigue el mismo patrón)
        self.Roses = []
        for _ in range(10):
            attempts = 0
            while attempts < 20:
                rose_x = self.x + random.randint(0, width - constants.FLOWER)
                rose_y = self.y + random.randint(0, height - constants.FLOWER)
                grid_x = (rose_x // constants.GRASS) * constants.GRASS
                grid_y = (rose_y // constants.GRASS) * constants.GRASS
                if (grid_x, grid_y) not in self.forbidden_zones and \
                   self._is_position_valid(rose_x, rose_y, constants.FLOWER, all_objects):
                    rose = Rose(rose_x, rose_y)
                    self.Roses.append(rose)
                    all_objects.append(rose)
                    break
                attempts += 1
        
        # Generate grass type 1 (follows the same pattern)
        # Generar hierba tipo 1 (sigue el mismo patrón)
        self.grasses1 = []
        for _ in range(10):
            attempts = 0
            while attempts < 20:
                grass1_x = self.x + random.randint(0, width - constants.GRASS_OBJ)
                grass1_y = self.y + random.randint(0, height - constants.GRASS_OBJ)
                grid_x = (grass1_x // constants.GRASS) * constants.GRASS
                grid_y = (grass1_y // constants.GRASS) * constants.GRASS
                if (grid_x, grid_y) not in self.forbidden_zones and \
                   self._is_position_valid(grass1_x, grass1_y, constants.GRASS_OBJ, all_objects):
                    grasss1 = Grass1(grass1_x, grass1_y)
                    self.grasses1.append(grasss1)
                    all_objects.append(grasss1)
                    break
                attempts += 1

        # Generate grass type 2 (follows the same pattern)
        # Generar hierba tipo 2 (sigue el mismo patrón)
        self.grasses2 = []
        for _ in range(10):
            attempts = 0
            while attempts < 20:
                grass2_x = self.x + random.randint(0, width - constants.GRASS_OBJ)
                grass2_y = self.y + random.randint(0, height - constants.GRASS_OBJ)
                grid_x = (grass2_x // constants.GRASS) * constants.GRASS
                grid_y = (grass2_y // constants.GRASS) * constants.GRASS
                if (grid_x, grid_y) not in self.forbidden_zones and \
                   self._is_position_valid(grass2_x, grass2_y, constants.GRASS_OBJ, all_objects):
                    grasss2 = Grass2(grass2_x, grass2_y) 
                    self.grasses2.append(grasss2)
                    all_objects.append(grasss2)
                    break
                attempts += 1

        # Generate grass type 3 (follows the same pattern)
        # Generar hierba tipo 3 (sigue el mismo patrón)
        self.grasses3 = []
        for _ in range(10):
            attempts = 0
            while attempts < 20:
                grass3_x = self.x + random.randint(0, width - constants.GRASS_OBJ)
                grass3_y = self.y + random.randint(0, height - constants.GRASS_OBJ)
                grid_x = (grass3_x // constants.GRASS) * constants.GRASS
                grid_y = (grass3_y // constants.GRASS) * constants.GRASS
                if (grid_x, grid_y) not in self.forbidden_zones and \
                   self._is_position_valid(grass3_x, grass3_y, constants.GRASS_OBJ, all_objects):
                    grasss3 = Grass3(grass3_x, grass3_y)
                    self.grasses3.append(grasss3)
                    all_objects.append(grasss3)
                    break
                attempts += 1

# World class to manage the game world, including trees, stones, flowers
# Clase World para manejar el mundo del juego, incluyendo árboles, piedras y flores
class World:
    def __init__(self, width, height):
        self.chunk_size = constants.WIDTH # Size of each world chunk
        self.active_chunks = {} # Chunks currently active (in the visible area around the player)
        self.inactive_chunks = {} # Inactive chunks (outside the visible area, for reuse)

        self.view_width = width # Width of the display window
        self.view_height = height # Height of the display window

        # Load and scale the grass image for the background
        # Carga y escala la imagen del césped para el fondo
        grass_path = os.path.join('assets', 'images', 'objects', 'grass.png')
        self.grass_image = pygame.image.load(grass_path).convert()
        self.grass_rect = pygame.transform.scale(self.grass_image, (constants.GRASS, constants.GRASS))

        # Day and Night Cycle
        # Ciclo de día y noche
        self.current_time = constants.MORNING_TIME # Current game time
        self.day_overlay = Surface((width, height)) # Surface for day/night overlay
        self.day_overlay.fill(constants.DAY_COLOR) # Initial color (day)
        self.day_overlay.set_alpha(0) # Initial transparency

        # Generate the initial chunk and neighboring chunks
        # Genera el chunk inicial y los chunks vecinos
        self.generate_chunk(0, 0)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                self.generate_chunk(dx, dy)

    def get_chunk_key(self, x, y):
        # Calculates the chunk key (grid coordinates of chunks) for a given position
        # Calcula la clave del chunk (coordenadas de la cuadrícula de chunks) para una posición dada
        chunk_x = x // self.chunk_size
        chunk_y = y // self.chunk_size
        return (chunk_x, chunk_y)

    def generate_chunk(self, chunk_x, chunk_y):
        # Generates a chunk if it's not already active
        # Genera un chunk si no está ya activo
        key = (chunk_x, chunk_y)
        if key not in self.active_chunks:
            x = chunk_x * self.chunk_size
            y = chunk_y * self.chunk_size
            # Create a new WorldChunk instance
            # Crea una nueva instancia de WorldChunk
            self.active_chunks[key] = WorldChunk(x, y, self.chunk_size, self.chunk_size)
    
    def update_chunks(self, player_x, player_y):
        # Updates active chunks based on the player's position
        # Actualiza los chunks activos basándose en la posición del jugador
        current_chunk = self.get_chunk_key(player_x, player_y)
        
        # Activate nearby chunks (3x3 area around the player)
        # Activa los chunks cercanos (área 3x3 alrededor del jugador)
        for dx in [-1, 0, 1]:  # Loop for neighboring X chunks
            for dy in [-1, 0, 1]: # Loop for neighboring Y chunks
                chunk_x = current_chunk[0] + dx
                chunk_y = current_chunk[1] + dy
                key = (chunk_x, chunk_y)
                
                # If the chunk is not active
                # Si el chunk no está activo
                if key not in self.active_chunks:
                    # Check if the chunk exists in inactive_chunks (for reuse)
                    # Verificar si el chunk existe en inactive_chunks (para reutilizarlo)
                    if key in self.inactive_chunks:
                        # Retrieve the inactive chunk and move it to active chunks
                        # Recuperar el chunk inactivo y moverlo a los chunks activos
                        self.active_chunks[key] = self.inactive_chunks[key]
                        del self.inactive_chunks[key]
                    else:
                        # If it doesn't exist anywhere, create a new chunk
                        # Si no existe en ningún lado, crear un nuevo chunk
                        x = chunk_x * self.chunk_size
                        y = chunk_y * self.chunk_size
                        self.active_chunks[key] = WorldChunk(x, y, self.chunk_size, self.chunk_size)

        # Deactivate distant chunks (outside the 3x3 area)
        # Desactivar chunks lejanos (fuera del área 3x3)
        chunks_to_move = []
        for chunk_key in list(self.active_chunks.keys()):  # Iterate over a copy of the keys
            distance_x = abs(chunk_key[0] - current_chunk[0])
            distance_y = abs(chunk_key[1] - current_chunk[1])
            # If the chunk is more than 1 unit away in X or Y, it's marked to move to inactive
            # Si el chunk está a más de 1 unidad de distancia en X o Y, se marca para mover a inactivos
            if distance_x > 1 or distance_y > 1:
                chunks_to_move.append(chunk_key)

        for chunk_key in chunks_to_move:
            # Move the chunk from active to inactive
            # Mover el chunk de activos a inactivos
            self.inactive_chunks[chunk_key] = self.active_chunks[chunk_key]
            del self.active_chunks[chunk_key]

    # Update the time (day/night)
    # Actualiza el tiempo (día/noche)
    def update_time(self, dt):
        self.current_time = (self.current_time + dt) % constants.DAY_LENGTH # Update time and keep it within the day cycle
        # Actualiza el tiempo y lo mantiene dentro del ciclo de día
        hour = (self.current_time / constants.DAY_LENGTH) * 24 # Convert time to hours (0-24)
        # Convierte el tiempo a horas (0-24)

        # Smooth sunrise (6:00 to 6:30)
        # Amanecer suave (6:00 a 6:30)
        # Smooth sunrise transition, alpha decreases to make the screen brighter
        # Transición suave de amanecer, el alfa disminuye para hacer la pantalla más clara
        if 6 <= hour < 6.5:
            progress = (hour - 6) / 0.5 # Transition progress (0 to 1)
            # Progreso de la transición (0 a 1)
            dawn_color = (255, 220, 120) # Dawn color
            # Color de amanecer
            day_color = constants.DAY_COLOR # Day color
            # Color de día
            # Interpolate RGB color components
            # Interpola los componentes de color RGB
            r = int(dawn_color[0] + (day_color[0] - dawn_color[0]) * progress)
            g = int(dawn_color[1] + (day_color[1] - dawn_color[1]) * progress)
            b = int(dawn_color[2] + (day_color[2] - dawn_color[2]) * progress)
            self.day_overlay.fill((r, g, b))
            alpha = int(100 * (1 - progress)) # Alpha decreases from 100 to 0
            # Alfa disminuye de 100 a 0
            self.day_overlay.set_alpha(alpha)

        # Full day (6:30 to 18:00)
        # Día completo (6:30 a 18:00)
        # The screen is completely bright
        # La pantalla está completamente brillante
        elif 6.5 <= hour < constants.NIGHT_START:
            self.day_overlay.fill(constants.DAY_COLOR)
            self.day_overlay.set_alpha(0) # Completely transparent
            # Completamente transparente

        # Sunset (18:00 to 18:30)
        # Atardecer (18:00 a 18:30)
        # Transition to night, alpha increases to darken the screen
        # Transición a la noche, el alfa aumenta para oscurecer la pantalla
        elif constants.NIGHT_START <= hour < constants.NIGHT_END:
            progress = (hour - constants.NIGHT_START) / (constants.NIGHT_END - constants.NIGHT_START)
            day_color = constants.DAY_COLOR
            night_color = constants.NIGHT_COLOR
            # Interpolate RGB color components
            # Interpola los componentes de color RGB
            r = int(day_color[0] + (night_color[0] - day_color[0]) * progress)
            g = int(day_color[1] + (night_color[1] - day_color[1]) * progress)
            b = int(day_color[2] + (night_color[2] - day_color[2]) * progress)
            self.day_overlay.fill((r, g, b))
            alpha = int(constants.MAX_NIGHT_ALPHA * progress) # Alpha increases from 0 to MAX_NIGHT_ALPHA
            # Alfa aumenta de 0 a MAX_NIGHT_ALPHA
            self.day_overlay.set_alpha(alpha)

        # Full night (18:30 to 6:00)
        # Noche completa (18:30 a 6:00)
        # The screen is completely dark
        # La pantalla está completamente oscura
        else:
            self.day_overlay.fill(constants.NIGHT_COLOR)
            self.day_overlay.set_alpha(constants.MAX_NIGHT_ALPHA)
        
        # Update all active chunks
        # Actualiza todos los chunks activos
        for chunk in self.active_chunks.values():
            chunk.update(dt)

    # Draw the world elements on the screen
    # Dibuja los elementos del mundo en la pantalla
    def draw(self, screen, camera_x, camera_y):
        # Draw each active chunk
        # Dibuja cada chunk activo
        for chunk in self.active_chunks.values():
            chunk.draw(screen, self.grass_rect, camera_x, camera_y)
            
        # Note: There was a 'for flower in self.flowers:' loop here that was likely redundant.
        # Objects are already drawn within chunk.draw(). If 'self.flowers' is a property
        # that consolidates flowers from all chunks, drawing them here would duplicate them.
        # It's commented out for now, assuming objects are drawn in the WorldChunk's draw method.
        # Nota: Había un bucle 'for flower in self.flowers:' aquí que probablemente era redundante.
        # Los objetos ya se dibujan dentro de chunk.draw(). Si 'self.flowers' es una propiedad
        # que consolida flores de todos los chunks, dibujarlas aquí las duplicaría.
        # Se ha comentado por ahora, asumiendo que los objetos se dibujan en el método draw de WorldChunk.
        # for flower in self.flowers:
        #     flower.draw(screen, camera_x, camera_y)

        # Draw the day/night overlay
        # Dibuja la superposición de día/noche
        screen.blit(self.day_overlay, (0, 0))

    # Draw the inventory prompt on the screen
    # Dibuja el mensaje para abrir el inventario en la pantalla
    def draw_inventory(self, screen):
        font = pygame.font.Font(None, 20) # Font for the text
        # Fuente para el texto
        inventory_text = font.render("Press 'E' to open inventory", True, constants.WHITE) # Render the text
        # Renderiza el texto
        screen.blit(inventory_text, (10, 10)) # Draw the text in the top-left corner
        # Dibuja el texto en la esquina superior izquierda

    # Property to get a consolidated list of all trees in active chunks
    # Propiedad para obtener una lista consolidada de todos los árboles en los chunks activos
    @property
    def trees(self):
        all_trees=[]
        for chunk in self.active_chunks.values():
            all_trees.extend(chunk.trees) # Extend the list with trees from each chunk
            # Extiende la lista con los árboles de cada chunk
        return all_trees
    
    # Property to get a consolidated list of all small stones in active chunks
    # Propiedad para obtener una lista consolidada de todas las piedras pequeñas en los chunks activos
    @property
    def small_stones(self):
        all_stones = []
        for chunk in self.active_chunks.values():
            all_stones.extend(chunk.small_stones)
        return all_stones
    
    # Property to get a consolidated list of all flowers in active chunks
    # Propiedad para obtener una lista consolidada de todas las flores en los chunks activos
    @property
    def flowers(self):
        all_flowers = []
        for chunk in self.active_chunks.values():
            all_flowers.extend(chunk.flowers)
        return all_flowers
    
    # Property to get a consolidated list of all roses in active chunks
    # Propiedad para obtener una lista consolidada de todas las rosas en los chunks activos
    @property
    def roses(self):
        all_roses = []
        for chunk in self.active_chunks.values():
            all_roses.extend(chunk.Roses)
        return all_roses
    
    # Property to get a consolidated list of all yellow roses in active chunks
    # Propiedad para obtener una lista consolidada de todas las rosas amarillas en los chunks activos
    @property
    def roses_yellow(self):
        all_yellow = []
        for chunk in self.active_chunks.values():
            all_yellow.extend(chunk.Roses_Yellow)
        return all_yellow

    # Property to get a consolidated list of all grass type 1 in active chunks
    # Propiedad para obtener una lista consolidada de toda la hierba tipo 1 en los chunks activos
    @property
    def grasses1(self):
        all_grasses = []
        for chunk in self.active_chunks.values():
            all_grasses.extend(chunk.grasses1)
        return all_grasses

    # Property to get a consolidated list of all grass type 2 in active chunks
    # Propiedad para obtener una lista consolidada de toda la hierba tipo 2 en los chunks activos
    @property
    def grasses2(self):
        all_grasses = []
        for chunk in self.active_chunks.values():
            all_grasses.extend(chunk.grasses2)
        return all_grasses

    # Property to get a consolidated list of all grass type 3 in active chunks
    # Propiedad para obtener una lista consolidada de toda la hierba tipo 3 en los chunks activos
    @property
    def grasses3(self):
        all_grasses = []
        for chunk in self.active_chunks.values():
            all_grasses.extend(chunk.grasses3)
        return all_grasses
    
    # Property to get a consolidated dictionary of all water tiles in active chunks
    # Propiedad para obtener un diccionario consolidado de todos los tiles de agua en los chunks activos
    @property
    def water_tiles(self):
        all_water = {}
        for chunk in self.active_chunks.values():
            all_water.update(chunk.water_tiles) # Combine water dictionaries from each chunk
            # Combina los diccionarios de agua de cada chunk
        return all_water

    def add_farmland(self, x, y):
        # Normalize coordinates to the tile grid
        # Normaliza las coordenadas a la cuadrícula de tiles
        grid_x = (x // constants.GRASS) * constants.GRASS
        grid_y = (y // constants.GRASS) * constants.GRASS
<<<<<<< HEAD
    
        # Get the chunk to which the position belongs
        # Obtiene el chunk al que pertenece la posición
        chunk_key = self.get_chunk_key(x, y)
        chunk = self.active_chunks.get(chunk_key)

        if chunk:  
            # Check for collision with existing objects (trees, stones, roses)
            # The use of *chunk.trees, etc. unpacks the lists into a single one for iteration.
            # Comprueba si hay colisión con objetos existentes (árboles, piedras, rosas)
            # El uso de *chunk.trees, etc. desempaqueta las listas en una sola para la iteración.
            for obj in [*chunk.trees, *chunk.small_stones, *chunk.Roses, *chunk.Roses_Yellow]:
                # Rectangle collision check
                # Comprobación de colisión de rectángulos
                if (grid_x < obj.x + obj.size and grid_x + constants.GRASS > obj.x and
                    grid_y < obj.y + obj.size and grid_y + constants.GRASS > obj.y):
                    return False # Cannot add farmland if it collides with an object
                    # No se puede añadir tierra de cultivo si colisiona con un objeto
            
            tile_key = (grid_x, grid_y)
            # Check if there is already water at the position
            # Comprueba si ya hay agua en la posición
            if tile_key in chunk.water_tiles:
                return False # Cannot add farmland in water
                # No se puede añadir tierra de cultivo en el agua

            # If the position is valid and there's no farmland yet, add it
            # Si la posición es válida y no hay ya tierra de cultivo, la añade
            if tile_key not in chunk.farmland_tiles:
                chunk.farmland_tiles[tile_key] = FarmLand(grid_x, grid_y)
                return True # Farmland added successfully
                # Tierra de cultivo añadida con éxito
        return False # The chunk is not active or some other condition is not met
        # El chunk no está activo o alguna otra condición no se cumple
    
=======
        
        chunk_key = self.get_chunk_key(grid_x, grid_y)
        if chunk_key not in self.active_chunks:
            return False
            
        chunk = self.active_chunks[chunk_key]
        tile_key = (grid_x, grid_y)
        
        # Verificar que no haya agua u obstáculos
        if (tile_key in chunk.water_tiles or 
            any(obj for obj in [*chunk.trees, *chunk.small_stones] 
                if pygame.Rect(obj.x, obj.y, obj.size, obj.size).colliderect(
                    pygame.Rect(grid_x, grid_y, constants.GRASS, constants.GRASS)))):
            return False
        
        # Si no existe farmland, crearlo
        if tile_key not in chunk.farmland_tiles:
            try:
                # Verificar que existan los assets
                for i in range(1, 7):
                    path = os.path.join('assets', 'images', 'objects', 'Farm', f'Farmland {i}.png')
                    if not os.path.exists(path):
                        print(f"Error: Falta archivo {path}")
                        return False
                
                chunk.farmland_tiles[tile_key] = FarmLand(grid_x, grid_y)
                
                # Eliminar hierbas decorativas
                for grass_list in [chunk.grasses1, chunk.grasses2, chunk.grasses3]:
                    chunk.grasses[:] = [g for g in grass_list 
                                    if not (grid_x <= g.x < grid_x + constants.GRASS and 
                                            grid_y <= g.y < grid_y + constants.GRASS)]
                return True
                
            except Exception as e:
                print(f"Error al crear farmland: {e}")
                return False
                
        return False
        
>>>>>>> 445b9609fa25c8f7d733ffc43bcba7446262cfc1
    def is_water_at(self, x, y):
        # Get the chunk to which the position belongs
        # Obtiene el chunk al que pertenece la posición
        chunk_key = self.get_chunk_key(x, y)
        chunk = self.active_chunks.get(chunk_key)

        if chunk:
            # Normalize coordinates to the tile grid
            # Normaliza las coordenadas a la cuadrícula de tiles
            grid_x = (x // constants.GRASS) * constants.GRASS
            grid_y = (y // constants.GRASS) * constants.GRASS

            tile_key = (grid_x, grid_y)
            # Returns True if there is water at the position, False otherwise
            # Retorna True si hay agua en la posición, False en caso contrario
            return tile_key in chunk.water_tiles

<<<<<<< HEAD
        return False # No water if the chunk is not active
        # No hay agua si el chunk no está activo
=======
        return False

                
    def get_farmland_at(self, x, y):
        chunk_key = self.get_chunk_key(x, y)
        chunk = self.active_chunks.get(chunk_key)

        if chunk:
            grid_x = (x // constants.GRASS) * constants.GRASS
            grid_y = (y // constants.GRASS) * constants.GRASS

            tile_key = (grid_x, grid_y)
            return chunk.farmland_tiles_get(tile_key)
        return None
    
    def update(self, dt):
        current_time = pygame.time.get_ticks()
        
        for chunk in self.active_chunks.values():
            for farmland in chunk.farmland_tiles.values():
                farmland.update(current_time)
>>>>>>> 445b9609fa25c8f7d733ffc43bcba7446262cfc1
