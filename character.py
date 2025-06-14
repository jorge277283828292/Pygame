import pygame
import constants
import os
from constants import *

class Character:
    #Inventory items
    #Ítems del inventario
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = {"wood" : 0, 
                          "stone": 0,
                          "flower": 0,
                          "rose": 0,
                          "rose_yellow": 0
                          }
        

        #Load Character image
        #Carga la imagen del personaje
        image_path = os.path.join("assets", "images", "character", "character.png")
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()

        #Animation properties
        #Propiedades de la animación
        self.frame_size = FRAME_SIZE
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_delay = ANIMATION_DELAY
        self.current_state = IDLE_DOWN
        self.moving = False
        self.facing_left = False
        self.is_running = False

        #Load all animations
        #Carga todas las animaciones
        self.animations = self.load_animations()

        #Load item images
        #Carga las imágenes de los ítems
        self.item_images = {
            "wood": self.load_item_images("wood.png"),
            "stone": self.load_item_images("stone.png"),
            "flower": self.load_item_images("flowers.png"), 
            "rose": self.load_item_images("rose.png"),
            "rose_yellow": self.load_item_images("rose-yellow.png")
        }
        
        #Initialize status
        #Inicializa los estados
        self.energy = constants.MAX_ENERGY
        self.food = constants.MAX_FOOD
        self.thirst = constants.MAX_THIRST
        self.stamina = constants.MAX_STAMINA

    #Load the animations by character
    #Carga las animaciones del personaje
    def load_animations(self):
        animations = {}
        for state in range(6):
            frames = [] 
            for frame in range(BASIC_FRAMES):
                surface = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
                surface.blit(self.sprite_sheet, (0, 0), 
                             (frame * self.frame_size,
                              state * self.frame_size,
                              self.frame_size, 
                              self.frame_size))
        
                if constants.PLAYER != self.frame_size:
                    surface = pygame.transform.scale(surface, (constants.PLAYER, constants.PLAYER))
                frames.append(surface)
            animations[state] = frames
        return animations

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        animation_speed = RUNNING if self.is_running else ANIMATION_DELAY
        if current_time - self.animation_timer > animation_speed:
            self.animation_timer = current_time
            self.animation_frame = (self.animation_frame + 1) % 6

    #Load item images from the assets folder 
    #Carga imágenes de ítems desde la carpeta de assets
    def load_item_images(self, filename):
        path = os.path.join("assets", "images", "objects", filename)
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (24, 24))

    #Draw the character on the screen
    #Dibuja el personaje en la pantalla
    def draw(self, screen, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        current_frame = self.animations[self.current_state][self.animation_frame]
        if self.facing_left:
            current_frame = pygame.transform.flip(current_frame, True, False)
        screen.blit(current_frame, (screen_x, screen_y))

        self.draw_status_bars(screen)

    #Move the character, checking for collisions with trees
    #Mueve el personaje, comprobando colisiones con árboles
    def move(self, dx, dy, world):
        self.moving = dx != 0 or dy != 0

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
            if self.current_state == WALK_DOWN:
                self.current_state = IDLE_DOWN
            elif self.current_state == WALK_UP:
                self.current_state = IDLE_UP
            elif self.current_state == WALK_RIGHT:
                self.current_state = IDLE_RIGHT


        new_x = self.x + dx
        new_y = self.y + dy
        
        for tree in world.trees:
            if self.check_collision(new_x, new_y, tree):
                self.moving = False
                return
            
        self.x = new_x
        self.y = new_y

        self.update_animation()

        #When he moves, he loses energy
        #Cuando se mueve, pierde energía
        if self.moving:
            if self.is_running and self.stamina > 0:
                self.update_stamina(-STAMINA_DECREASE_RATE)
                self.update_energy(-MOVEMENT_ENERGY_COST * 2)
            else:
                self.update_energy(-MOVEMENT_ENERGY_COST)
            if not self.moving:
                self.update_stamina(STAMINA_INCREASE_RATE)

    #Check if the character collides with an object, reducing the collision area by 25%
    #Verifica si el personaje colisiona con un objeto, reduciendo el área de colisión en un 25%
    def check_collision(self, x, y, obj):
        shrink = 1  # Reduce el área de colisión en un 25%
        obj_x = obj.x + obj.size * shrink / 2
        obj_y = obj.y + obj.size * shrink / 2
        obj_size = obj.size * (1 - shrink)
        return (
            x < obj_x + obj_size and
            x + constants.PLAYER > obj_x and
            y < obj_y + obj_size and
            y + constants.PLAYER > obj_y
        )

    #Check if the character is near an object, allowing interaction
    #Verifica si el personaje está cerca de un objeto, permitiendo la interacción
    def is_near(self, obj):
        return (
            abs(self.x - obj.x) <= max(constants.PLAYER, obj.size) + 5 and
            abs(self.y - obj.y) <= max(constants.PLAYER, obj.size) + 5
        )
    
    #Interact with the world, collecting resources from trees, stones, and flowers
    #Interacciona con el mundo, recolectando recursos de árboles, piedras y flores
    def interact(self, world):
        #Trees
        # Árboles
        for chunk in world.active_chunks.values():
            for tree in chunk.trees:
                if self.is_near(tree):
                    if tree.chop():
                        self.inventory["wood"] += 1
                        if tree.wood == 0:
                            chunk.trees.remove(tree)
                        return

            #Stones
            #Piedras
            for stone in chunk.small_stones:
                if self.is_near(stone):
                    if stone.mine():
                        self.inventory["stone"] += 1
                        if stone.stone == 0:
                            chunk.small_stones.remove(stone)
                        return

            #Flowers
            #Flores
            for flower in chunk.flowers:
                if self.is_near(flower):
                    if flower.collect():
                        self.inventory["flower"] += 1
                    if flower.flower == 0:
                        chunk.flowers.remove(flower)
                    return

            #Roses
            #Rosas
            for rose in chunk.Roses:
                if self.is_near(rose):
                    if rose.collect():
                        self.inventory["rose"] += 1
                    if rose.rose == 0:
                        chunk.Roses.remove(rose)
                    return

            #Yellow Roses
            #Rosas amarillas
            for rose_yellow in chunk.Roses_Yellow:
                if self.is_near(rose_yellow):
                    if rose_yellow.collect():
                        self.inventory["rose_yellow"] += 1
                    if rose_yellow.rose_yellow == 0:
                        chunk.Roses_Yellow.remove(rose_yellow)
                    return

    #Draw the inventory on the screen   
    #Dibuja el inventario en la pantalla
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
        #Text for close the inventory
        #Texto para cerrar el inventario
        screen.blit(close_text, (constants.WIDTH // 2 - close_text.get_width() // 2, constants.HEIGHT - 40))    

    #Update the character's energy, food, and thirst levels
    #Actualiza los niveles de energía, comida y sed del personaje
    def update_energy(self, amount):
        self.energy = max(0, min(self.energy + amount, constants.MAX_ENERGY))

    def update_food(self, amount):
        self.food = max(0, min(self.food + amount, constants.MAX_FOOD))
    
    def update_thirst(self, amount):
        self.thirst = max(0, min(self.thirst + amount, constants.MAX_THIRST))

    def update_stamina(self, amount):
        self.stamina = max(0, min(self.stamina +amount, constants.MAX_STAMINA))

    #Draw the status bars for energy, food, and thirst
    #Dibuja las barras de estado para energía, comida y sed
    def draw_status_bars(self, screen):
        bar_width = 100
        bar_height = 10
        x_offset = 10
        y_offset = 10

        # ENERGY BAR
        # Barra de energía
        pygame.draw.rect(screen, constants.BAR_BACKGROUND_COLOR, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constants.ENERGY_COLOR, (x_offset, y_offset, bar_width * (self.energy / constants.MAX_ENERGY), bar_height))
        y_offset += bar_height + 5

        # THIRST BAR
        # Barra de sed
        pygame.draw.rect(screen, constants.BAR_BACKGROUND_COLOR, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constants.THIRST_COLOR, (x_offset, y_offset, bar_width * (self.thirst / constants.MAX_THIRST), bar_height))
        y_offset += bar_height + 5

        # FOOD BAR
        # Barra de comida
        pygame.draw.rect(screen, constants.BAR_BACKGROUND_COLOR, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constants.FOOD_COLOR, (x_offset, y_offset, bar_width * (self.food / constants.MAX_FOOD), bar_height))
        y_offset += bar_height + 5
        # STAMINA BAR
        # Barra de Stamina
        pygame.draw.rect(screen, constants.BAR_BACKGROUND_COLOR, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constants.STAMINA_COLOR, (x_offset, y_offset, bar_width * (self.stamina / constants.MAX_STAMINA), bar_height))
        y_offset += bar_height + 5
# Update the character's status over time
# Actualiza el estado del personaje con el tiempo
    def update_status(self):
        food_rate = FOOD_DECREASE_RATE * (RUN_FOOD_DECREASE_MULTIPLER if self.is_running else 1)
        thirst_rate = THIRST_DECREASE_RATE * (RUN_THIRST_DECREASE_MULTIPLER if self.is_running else 1)


        self.update_food(-constants.FOOD_DECREASE_RATE)
        self.update_thirst(-constants.THIRST_DECREASE_RATE)

        if self.food < constants.MAX_FOOD * 0.2 or self.thirst < constants.MAX_THIRST * 0.2:
            self.update_energy(-constants.ENERGY_DECREASE_RATE)	
        else:
            self.update_energy(-constants.ENERGY_INCREASE_RATE)

        if not self.is_running:
            self.update_stamina(STAMINA_INCREASE_RATE)