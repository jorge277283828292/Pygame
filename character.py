import pygame
import constants
import os
from constants import *
from inventory import Inventory

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = Inventory()

        # Load the character's main sprite sheet.
        # Carga la hoja de sprites principal del personaje.
        image_path = os.path.join("assets", "images", "character", "character.png")
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()
        
        # Load the character's action sprite sheet (e.g., for chopping, hoeing).
        # Carga la hoja de sprites de acciones del personaje (ej. para talar, arar).
        self.action_sprite_sheet = pygame.image.load(
            os.path.join('assets','images','character','Player_Actions.png')
        ).convert_alpha()

        # Animation properties.
        # Propiedades de la animación.
        self.frame_size = FRAME_SIZE
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_delay = ANIMATION_DELAY
        self.current_state = IDLE_DOWN
        self.moving = False
        self.facing_left = False
        self.is_running = False

        self.is_chopping = False
        self.chop_timer = 0
        self.chop_frame = 0
        self.is_hoeing = False
        self.hoe_timer = 0
        self.hoe_frame = 0

        # Load all animations.
        # Carga todas las animaciones.
        self.animations = self.load_animations()
        self.axe_animations = self.load_axe_animations()
        self.hoe_animations = self.load_hoe_animations()
        
        # Initialize character status.
        # Inicializa los estados del personaje.
        self.energy = constants.MAX_ENERGY
        self.food = constants.MAX_FOOD
        self.thirst = constants.MAX_THIRST
        self.stamina = constants.MAX_STAMINA
        
    # Load basic character animations (idle, walk).
    # Carga las animaciones básicas del personaje (idle, caminar).
    def load_animations(self):
        animations = {}
        for state in range(6):
            frames = [] 
            for frame in range(BASIC_FRAMES):
                temp_surface = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
                temp_surface.blit(self.sprite_sheet, (0, 0), 
                                 (frame * self.frame_size,
                                  state * self.frame_size,
                                  self.frame_size, 
                                  self.frame_size))
        
                surface = pygame.Surface((constants.PLAYER, constants.PLAYER), pygame.SRCALPHA)
                scaled_temp = pygame.transform.scale(temp_surface, (constants.PLAYER, constants.PLAYER))
                surface.blit(scaled_temp, (0, 0))

                frames.append(surface)
            animations[state] = frames
        return animations

    # Load axe-wielding animations.
    # Carga las animaciones de uso del hacha.
    def load_axe_animations(self):
        animations = {}

        row_mapping = {
            3: 3, # Corresponds to right/left chopping animation
            4: 4, # Corresponds to down chopping animation
            5: 5  # Corresponds to up chopping animation
        }

        for state, row in row_mapping.items():
            frames = []
            for frame in range(AXE_FRAMES):
                temp_surface = pygame.Surface((constants.ACTION_FRAME_SIZE, constants.ACTION_FRAME_SIZE), pygame.SRCALPHA)
                x = (frame % AXE_COLS) * constants.ACTION_FRAME_SIZE
                frame_rect = pygame.Rect(x, row * constants.ACTION_FRAME_SIZE,
                                         constants.ACTION_FRAME_SIZE,
                                         constants.ACTION_FRAME_SIZE)

                temp_surface.blit(self.action_sprite_sheet, (0, 0), frame_rect)

                action_scale = constants.ACTION_FRAME_SIZE / constants.FRAME_SIZE
                action_size = int(constants.PLAYER * action_scale)

                surface = pygame.Surface((action_size, action_size), pygame.SRCALPHA)

                scaled_temp = pygame.transform.scale(temp_surface, (action_size, action_size))
                surface.blit(scaled_temp, (0, 0))

                frames.append(surface)
            animations[state] = frames
        return animations

    # Load hoe-wielding animations.
    # Carga las animaciones de uso de la azada.
    def load_hoe_animations(self):
        animations = {}
        row_mapping = {
            3: 6, # Corresponds to right/left hoeing animation
            4: 7, # Corresponds to down hoeing animation
            5: 8  # Corresponds to up hoeing animation
        }

        for state, row in row_mapping.items():
            frames = []
            for frame in range(HOE_FRAMES):
                temp_surface = pygame.Surface((constants.ACTION_FRAME_SIZE, constants.ACTION_FRAME_SIZE), pygame.SRCALPHA)
                x = (frame % HOE_COLS) * constants.ACTION_FRAME_SIZE
                frame_rect = pygame.Rect(x, row * constants.ACTION_FRAME_SIZE,
                                         constants.ACTION_FRAME_SIZE,
                                         constants.ACTION_FRAME_SIZE)

                temp_surface.blit(self.action_sprite_sheet, (0, 0), frame_rect)

                action_scale = constants.ACTION_FRAME_SIZE / constants.FRAME_SIZE
                action_size = int(constants.PLAYER * action_scale)

                surface = pygame.Surface((action_size, action_size), pygame.SRCALPHA)

                scaled_temp = pygame.transform.scale(temp_surface, (action_size, action_size))
                surface.blit(scaled_temp, (0, 0))

                frames.append(surface)
            animations[state] = frames
        return animations

    # Update the current animation frame based on character's action.
    # Actualiza el frame actual de la animación según la acción del personaje.
    def update_animation(self):
        current_time = pygame.time.get_ticks()

        if self.is_chopping:
            if current_time - self.chop_timer > AXE_ANIMATIONS_DELAY:
                self.chop_timer = current_time
                self.chop_frame = (self.chop_frame + 1) % AXE_FRAMES
                if self.chop_frame == 0:  # Animation completed.
                                          # Animación completada.
                    self.is_chopping = False

        elif self.is_hoeing:
            if current_time - self.hoe_timer > HOE_ANIMATION_DELAY:
                self.hoe_timer = current_time
                self.hoe_frame = (self.hoe_frame + 1) % HOE_FRAMES
                if self.hoe_frame == HOE_FRAMES - 1:  # Animation completed on the last frame.
                                                      # Animación completada en el último frame.
                    self.is_hoeing = False
        else:
            animation_speed = RUNNING if self.is_running else ANIMATION_DELAY
            if current_time - self.animation_timer > animation_speed:
                self.animation_timer = current_time
                self.animation_frame = (self.animation_frame + 1) % 6

    # Draw the character on the screen, handling different action animations.
    # Dibuja el personaje en la pantalla, manejando las diferentes animaciones de acción.
    def draw(self, screen, camera_x, camera_y, show_inventory=False):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        if self.is_chopping:
            # Axe animation.
            # Animación de hacha.
            if self.current_state in [IDLE_RIGHT, WALK_RIGHT] or (self.current_state == WALK_RIGHT and self.facing_left):
                current_frame = self.axe_animations[3][self.chop_frame]
                if self.facing_left:
                    current_frame = pygame.transform.flip(current_frame, True, False)
            elif self.current_state in [IDLE_DOWN, WALK_DOWN]:
                current_frame = self.axe_animations[4][self.chop_frame]
            elif self.current_state in [IDLE_UP, WALK_UP]:
                current_frame = self.axe_animations[5][self.chop_frame]
            else: # Fallback to general animation if state doesn't match a specific axe animation.
                  # Vuelve a la animación general si el estado no coincide con una animación de hacha específica.
                current_frame = self.animations[self.current_state][self.animation_frame]

            frame_rect = current_frame.get_rect()
            offset_x = (frame_rect.width - constants.PLAYER) // 2
            offset_y = (frame_rect.height - constants.PLAYER)
            screen.blit(current_frame, (screen_x - offset_x, screen_y - offset_y))

        elif self.is_hoeing:
            # Hoe animation.
            # Animación de azada.
            if self.current_state in [IDLE_RIGHT, WALK_RIGHT] or (self.current_state == WALK_RIGHT and self.facing_left):
                current_frame = self.hoe_animations[3][self.hoe_frame]  # Use 3 for right/left.
                                                                        # Usa 3 para derecha/izquierda.
                if self.facing_left:
                    current_frame = pygame.transform.flip(current_frame, True, False)
            elif self.current_state in [IDLE_DOWN, WALK_DOWN]:
                current_frame = self.hoe_animations[4][self.hoe_frame]  # Use 4 for down.
                                                                        # Usa 4 para abajo.
            elif self.current_state in [IDLE_UP, WALK_UP]:
                current_frame = self.hoe_animations[5][self.hoe_frame]  # Use 5 for up.
                                                                        # Usa 5 para arriba.
            else: # Fallback to general animation if state doesn't match a specific hoe animation.
                  # Vuelve a la animación general si el estado no coincide con una animación de azada específica.
                current_frame = self.animations[self.current_state][self.animation_frame]

            frame_rect = current_frame.get_rect()
            offset_x = (frame_rect.width - constants.PLAYER) // 2
            offset_y = (frame_rect.height - constants.PLAYER)
            screen.blit(current_frame, (screen_x - offset_x, screen_y - offset_y))

        else:
            # Regular movement/idle animation.
            # Animación de movimiento/idle regular.
            current_frame = self.animations[self.current_state][self.animation_frame]
            if self.facing_left:
                current_frame = pygame.transform.flip(current_frame, True, False)
            screen.blit(current_frame, (screen_x, screen_y))
            
    # Check if the character is currently in water.
    # Verifica si el personaje está actualmente en el agua.
    def is_in_water(self, world):
        return world.is_water_at(self.x + constants.PLAYER // 2, self.y + constants.PLAYER // 2)

    # Move the character, handling speed, animation state, and collisions.
    # Mueve el personaje, gestionando la velocidad, el estado de la animación y las colisiones.
    def move(self, dx, dy, world):
        self.moving = dx != 0 or dy != 0
        speed_multiplier = 1.0

        if self.is_in_water(world):
            speed_multiplier *= constants.WATER_MOVE_MULTIPLIER
        
        if self.moving:
            speed_multiplier = RUN_SPEED if self.is_running and self.stamina > 0 else WALK_SPEED
            dx *= speed_multiplier / WALK_SPEED
            dy *= speed_multiplier / WALK_SPEED
            if dy > 0:
                self.current_state = WALK_DOWN
                self.facing_left = False
            elif dy < 0:
                self.current_state = WALK_UP
                self.facing_left = False
            elif dx > 0:
                self.current_state = WALK_RIGHT
                self.facing_left = False 
            elif dx < 0:
                self.current_state = WALK_RIGHT
                self.facing_left = True
        else:
            # Transition to idle state when not moving.
            # Transición al estado de "idle" cuando no se está moviendo.
            if self.current_state == WALK_DOWN:
                self.current_state = IDLE_DOWN
            elif self.current_state == WALK_UP:
                self.current_state = IDLE_UP
            elif self.current_state == WALK_RIGHT:
                self.current_state = IDLE_RIGHT

        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check for collisions with trees before moving.
        # Comprueba colisiones con los árboles antes de moverse.
        for tree in world.trees:
            if self.check_collision(new_x, new_y, tree):
                self.moving = False
                return
            
        self.x = new_x
        self.y = new_y

        self.update_animation()

        # Update energy and stamina based on movement.
        # Actualiza energía y resistencia según el movimiento.
        if self.moving:
            if self.is_running and self.stamina > 0:
                self.update_stamina(-STAMINA_DECREASE_RATE)
                self.update_energy(-MOVEMENT_ENERGY_COST * 2)
            else:
                self.update_energy(-MOVEMENT_ENERGY_COST)
            if not self.moving: # This condition will always be false inside the 'if self.moving' block.
                                # Esta condición siempre será falsa dentro del bloque 'if self.moving'.
                self.update_stamina(STAMINA_INCREASE_RATE)

    # Check for collision with an object, using a reduced collision area.
    # Verifica la colisión con un objeto, usando un área de colisión reducida.
    def check_collision(self, x, y, obj):
        shrink = 0.7  # Reduce the collision area by 25%.
                      # Reduce el área de colisión en un 25%.
        obj_x = obj.x + obj.size * shrink / 2
        obj_y = obj.y + obj.size * shrink / 2
        obj_size = obj.size * (1 - shrink)
        return (
            x < obj_x + obj_size and
            x + constants.PLAYER > obj_x and
            y < obj_y + obj_size and
            y + constants.PLAYER > obj_y
        )

    # Check if the character is near an object for interaction purposes.
    # Verifica si el personaje está cerca de un objeto para interactuar.
    def is_near(self, obj):
        return (
            abs(self.x - obj.x) <= max(constants.PLAYER, obj.size) + 5 and
            abs(self.y - obj.y) <= max(constants.PLAYER, obj.size) + 5
        )
    
    # Handle character interactions with the world (e.g., collecting resources, using tools).
    # Gestiona las interacciones del personaje con el mundo (ej. recolectar recursos, usar herramientas).
    def interact(self, world):
        keys = pygame.key.get_pressed()
<<<<<<< HEAD
        if keys[pygame.K_p]:
            in_water = self.is_in_water(world)  # Use existing method.
                                                 # Usar el método existente.
            if in_water:
                bucket_equipped, hand = self.inventory.has_bucket_equipped()
                if bucket_equipped:
                    success = self.inventory.fill_bucket(hand)
                    if success:
                        return  # Exit after filling the bucket.
                                # Salir después de llenar la cubeta.
                # Drink water if no bucket is equipped.
                # Beber agua si no tenemos cubeta equipada.
                self.update_thirst(constants.WATER_THIRST_RECOVERY)
                return
            else:
                # Check if a water bucket is equipped to empty it.
                # Verificar si tenemos cubeta de agua equipada para vaciarla.
                water_bucket_equipped, hand = self.inventory.has_water_bucket_equipped()
                if water_bucket_equipped:
                    self.inventory.empty_bucket(hand)
                    return

=======

        # ===== MANEJO DE CUBETA DE AGUA =====
        bucket_equipped, hand = self.inventory.has_bucket_equipped()
        water_bucket_equipped, water_hand = self.inventory.has_water_bucket_equipped()
        
        # Llenar cubeta en agua
        if bucket_equipped and keys[pygame.K_q]:
            if world.is_water_at(self.x + constants.PLAYER//2, self.y + constants.PLAYER//2):
                self.inventory.fill_bucket(hand)
                return True
        
        # Vaciar cubeta en cultivos
        elif water_bucket_equipped and keys[pygame.K_q]:
            grid_x = (self.x // constants.GRASS) * constants.GRASS
            grid_y = (self.y // constants.GRASS) * constants.GRASS
            
            # Regar en un área 3x3
            watered = False
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    target_x = grid_x + dx * constants.GRASS
                    target_y = grid_y + dy * constants.GRASS
                    
                    chunk_key = world.get_chunk_key(target_x, target_y)
                    if chunk_key in world.active_chunks:
                        chunk = world.active_chunks[chunk_key]
                        tile_key = (target_x, target_y)
                        
                        if tile_key in chunk.farmland_tiles:
                            if chunk.farmland_tiles[tile_key].water():
                                watered = True
            
            if watered:
                self.inventory.empty_bucket(water_hand)
                return True

        # ===== USO DE AZADA =====
>>>>>>> 445b9609fa25c8f7d733ffc43bcba7446262cfc1
        if keys[pygame.K_q] and self.inventory.has_hoe_equipped() and not self.is_hoeing:
            self.is_hoeing = True
            self.hoe_timer = pygame.time.get_ticks()
            self.hoe_frame = 0
            
<<<<<<< HEAD
            # Determine target location for hoeing based on character's direction.
            # Determinar la ubicación objetivo para arar basándose en la dirección del personaje.
            if self.current_state in [IDLE_RIGHT, WALK_RIGHT]:
=======
            # Determinar dirección de interacción
            if self.current_state in [constants.IDLE_RIGHT, constants.WALK_RIGHT]:
>>>>>>> 445b9609fa25c8f7d733ffc43bcba7446262cfc1
                target_x = self.x + constants.PLAYER if not self.facing_left else self.x - constants.PLAYER
                target_y = self.y
            elif self.current_state in [constants.IDLE_UP, constants.WALK_UP]:
                target_x = self.x
                target_y = self.y - constants.PLAYER
            elif self.current_state in [constants.IDLE_DOWN, constants.WALK_DOWN]:
                target_x = self.x
                target_y = self.y + constants.PLAYER
            else:
                target_x = self.x
                target_y = self.y
            
            world.add_farmland(target_x, target_y)
            return True

        # ===== COSECHAR =====
        if keys[pygame.K_SPACE]:
        # Determinar dirección de interacción
            if self.current_state in [constants.IDLE_RIGHT, constants.WALK_RIGHT]:
                target_x = self.x + constants.PLAYER if not self.facing_left else self.x - constants.PLAYER
                target_y = self.y
            elif self.current_state in [constants.IDLE_UP, constants.WALK_UP]:
                target_x = self.x
                target_y = self.y - constants.PLAYER
            elif self.current_state in [constants.IDLE_DOWN, constants.WALK_DOWN]:
                target_x = self.x
                target_y = self.y + constants.PLAYER
            else: # Default to current position if no specific direction.
                  # Por defecto, la posición actual si no hay una dirección específica.
                target_x = self.x
                target_y = self.y
                
<<<<<<< HEAD
            world.add_farmland(target_x, target_y)
            return
        
        # Iterate through active chunks to check for interactable objects.
        # Iterar a través de los "chunks" activos para buscar objetos interactuables.
=======
            grid_x = (target_x // constants.GRASS) * constants.GRASS
            grid_y = (target_y // constants.GRASS) * constants.GRASS
            
            chunk_key = world.get_chunk_key(grid_x, grid_y)
            if chunk_key in world.active_chunks:
                chunk = world.active_chunks[chunk_key]
                tile_key = (grid_x, grid_y)
                
                if tile_key in chunk.farmland_tiles:
                    farmland = chunk.farmland_tiles[tile_key]
                    if farmland.harvest():
                        self.inventory.add_item('carrot')
                        return True


        # ===== INTERACCIÓN CON OTROS OBJETOS =====
>>>>>>> 445b9609fa25c8f7d733ffc43bcba7446262cfc1
        for chunk in world.active_chunks.values():
            # Trees.
            # Árboles.
            for tree in chunk.trees[:]:
                if self.is_near(tree):
                    if self.inventory.has_axe_equipped():
                        self.is_chopping = True
                        self.chop_timer = pygame.time.get_ticks()
                        self.chop_frame = 0
<<<<<<< HEAD
                    if tree.chop(): # Attempt to chop the tree.
                                    # Intentar talar el árbol.
                        self.inventory.add_item('wood')
                        if tree.wood == 0:
                            chunk.trees.remove(tree)
                    return

            # Roses.
            # Rosas.
            for rose in chunk.Roses[:]:
                if self.is_near(rose):
                    if rose.collect(): # Attempt to collect the rose.
                                       # Intentar recolectar la rosa.
                        self.inventory.add_item('rose')
                    if rose.rose == 0:
                        chunk.Roses.remove(rose)
                    return

            # Yellow Roses.
            # Rosas amarillas.
            for rose_yellow in chunk.Roses_Yellow[:]:
                if self.is_near(rose_yellow):
                    if rose_yellow.collect(): # Attempt to collect the yellow rose.
                                             # Intentar recolectar la rosa amarilla.
                        self.inventory.add_item('rose_yellow')
                    if rose_yellow.rose_yellow == 0:
                        chunk.Roses_Yellow.remove(rose_yellow)
                    return
=======
                    
                    if tree.chop():
                        self.inventory.add_item('wood')
                        if tree.wood == 0:
                            chunk.trees.remove(tree)
                    return True
>>>>>>> 445b9609fa25c8f7d733ffc43bcba7446262cfc1

            # Stones.
            # Piedras.
            for stone in chunk.small_stones[:]:
                if self.is_near(stone):
                    if stone.mine(): # Attempt to mine the stone.
                                     # Intentar minar la piedra.
                        self.inventory.add_item('stone')
<<<<<<< HEAD
                    if stone.stone == 0:
                        chunk.small_stones.remove(stone)
                    return

    # Draw the character's inventory on the screen.
    # Dibuja el inventario del personaje en la pantalla.
=======
                        if stone.stone == 0:
                            chunk.small_stones.remove(stone)
                    return True

            # Flores/Rosas
            for collectible in [*chunk.flowers, *chunk.Roses, *chunk.Roses_Yellow]:
                if self.is_near(collectible):
                    if hasattr(collectible, 'collect') and collectible.collect():
                        item_name = {
                            'Rose': 'rose',
                            'RoseYellow': 'rose_yellow',
                            'Flower': 'flower'
                        }.get(collectible.__class__.__name__, 'flower')
                        self.inventory.add_item(item_name)
                        return True

        return False
    #Draw the inventory on the screen   
    #Dibuja el inventario en la pantalla
>>>>>>> 445b9609fa25c8f7d733ffc43bcba7446262cfc1
    def draw_inventory(self, screen, show_inventory=False):
        self.inventory.draw(screen, 0, 0, show_inventory)

        if show_inventory:
            font = pygame.font.Font(None, 24)  
            close_text = font.render("Press 'E' to close the inventory", True, constants.WHITE)
            screen.blit(close_text, (constants.WIDTH // 2 - close_text.get_width() // 2, constants.INVENTORY_Y - 35))

    # Update the character's energy level.
    # Actualiza el nivel de energía del personaje.
    def update_energy(self, amount):
        self.energy = max(0, min(self.energy + amount, constants.MAX_ENERGY))

    # Update the character's food level.
    # Actualiza el nivel de comida del personaje.
    def update_food(self, amount):
        self.food = max(0, min(self.food + amount, constants.MAX_FOOD))
    
    # Update the character's thirst level.
    # Actualiza el nivel de sed del personaje.
    def update_thirst(self, amount):
        self.thirst = max(0, min(self.thirst + amount, constants.MAX_THIRST))

    # Update the character's stamina level.
    # Actualiza el nivel de resistencia del personaje.
    def update_stamina(self, amount):
        self.stamina = max(0, min(self.stamina +amount, constants.MAX_STAMINA))

    # Draw the character's status bars (energy, thirst, food, stamina).
    # Dibuja las barras de estado del personaje (energía, sed, comida, resistencia).
    def draw_status_bars(self, screen):
        bar_width = 100
        bar_height = 10
        x_offset = 10
        y_offset = 10

        # ENERGY BAR.
        # Barra de energía.
        pygame.draw.rect(screen, constants.BAR_BACKGROUND_COLOR, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constants.ENERGY_COLOR, (x_offset, y_offset, bar_width * (self.energy / constants.MAX_ENERGY), bar_height))
        y_offset += bar_height + 5

        # THIRST BAR.
        # Barra de sed.
        pygame.draw.rect(screen, constants.BAR_BACKGROUND_COLOR, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constants.THIRST_COLOR, (x_offset, y_offset, bar_width * (self.thirst / constants.MAX_THIRST), bar_height))
        y_offset += bar_height + 5

        # FOOD BAR.
        # Barra de comida.
        pygame.draw.rect(screen, constants.BAR_BACKGROUND_COLOR, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constants.FOOD_COLOR, (x_offset, y_offset, bar_width * (self.food / constants.MAX_FOOD), bar_height))
        y_offset += bar_height + 5
        
        # STAMINA BAR.
        # Barra de Resistencia.
        pygame.draw.rect(screen, constants.BAR_BACKGROUND_COLOR, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constants.STAMINA_COLOR, (x_offset, y_offset, bar_width * (self.stamina / constants.MAX_STAMINA), bar_height))
        y_offset += bar_height + 5

        font = pygame.font.Font(None, 20)
        if hasattr(self, 'in_water') and self.in_water:
            water_text = font.render("Press 'Q' to drink water", True, constants.WHITE)
            screen.blit(water_text, (x_offset, y_offset + 25))

# Update the character's status (food, thirst, energy) over time.
# Actualiza el estado del personaje (comida, sed, energía) con el tiempo.
    def update_status(self):
        # Calculate food and thirst decrease rates, considering if the character is running.
        # Calcula las tasas de disminución de comida y sed, considerando si el personaje está corriendo.
        food_rate = FOOD_DECREASE_RATE * (RUN_FOOD_DECREASE_MULTIPLER if self.is_running else 1)
        thirst_rate = THIRST_DECREASE_RATE * (RUN_THIRST_DECREASE_MULTIPLER if self.is_running else 1)

        self.update_food(-constants.FOOD_DECREASE_RATE)
        self.update_thirst(-constants.THIRST_DECREASE_RATE)

        # Decrease energy if food or thirst are low, otherwise increase energy.
        # Disminuye la energía si la comida o la sed son bajas, de lo contrario, aumenta la energía.
        if self.food < constants.MAX_FOOD * 0.2 or self.thirst < constants.MAX_THIRST * 0.2:
            self.update_energy(-constants.ENERGY_DECREASE_RATE) 
        else:
            self.update_energy(-constants.ENERGY_INCREASE_RATE)

        # Recover stamina when not running.
        # Recupera la resistencia cuando no está corriendo.
        if not self.is_running:
            self.update_stamina(STAMINA_INCREASE_RATE)