import pygame
import constants
import os
import math
import random

# Master Class
# Clase base para los elementos del juego
class GameElement:
    def __init__(self, x, y, image_path, size):
        self.x = x # X-coordinate of the element's position / Coordenada X de la posición del elemento
        self.y = y # Y-coordinate of the element's position / Coordenada Y de la posición del elemento
        # Load the image and convert it for optimal drawing, preserving transparency
        # Carga la imagen y la convierte para un dibujo óptimo, conservando la transparencia
        self.image = pygame.image.load(image_path).convert_alpha()
        # Scale the image to the specified size
        # Escala la imagen al tamaño especificado
        self.image = pygame.transform.scale(self.image, (size, size))
        self.size = self.image.get_width() # Get the actual width of the scaled image / Obtiene el ancho real de la imagen escalada

    def draw(self, screen, camera_x, camera_y):
        # Calculate the screen coordinates based on the camera position
        # Calcula las coordenadas en pantalla basándose en la posición de la cámara
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Draw the element only if it's visible on the screen
        # Dibuja el elemento solo si es visible en la pantalla
        if (screen_x + self.size >= 0 and screen_x <= constants.WIDTH and
                screen_y + self.size >= 0 and screen_y <= constants.HEIGHT):
            screen.blit(self.image, (screen_x, screen_y))

# Tree
# Árbol
class Tree(GameElement):
    def __init__(self, x, y):
        # Define the image path for the tree
        # Define la ruta de la imagen para el árbol
        tree_path = os.path.join('assets', 'images', 'objects', 'tree.png')
        # Call the constructor of the base class (GameElement)
        # Llama al constructor de la clase base (GameElement)
        super().__init__(x, y, tree_path, constants.TREE)
        self.wood = 5 # Amount of wood this tree has / Cantidad de madera que tiene este árbol

    def chop(self):
        # Decrease the wood amount and return True if successful
        # Disminuye la cantidad de madera y retorna True si tiene éxito
        if self.wood > 0:
            self.wood -= 1
            return True    
        return False # Return False if no wood left / Retorna False si no queda madera

# Small Stone
# Piedras pequeñas
class SmallStone(GameElement):
    def __init__(self, x, y):
        # Define the image path for the stone
        # Define la ruta de la imagen para la piedra
        stone_path = os.path.join('assets', 'images', 'objects', 'stone.png')
        # Call the constructor of the base class
        # Llama al constructor de la clase base
        super().__init__(x, y, stone_path, constants.SMALL_STONE)
        self.stone = 10 # Amount of stone this object has / Cantidad de piedra que tiene este objeto

    def mine(self):
        # Decrease the stone amount and return True if successful
        # Disminuye la cantidad de piedra y retorna True si tiene éxito
        if self.stone > 0:
            self.stone -= 1
            return True
        return False # Return False if no stone left / Retorna False si no queda piedra
    
# Flower
# Flor
class Flower(GameElement):
    def __init__(self, x, y):
        # Define the image path for the flower
        # Define la ruta de la imagen para la flor
        flower_path = os.path.join('assets', 'images', 'objects', 'flowers.png')
        # Call the constructor of the base class
        # Llama al constructor de la clase base
        super().__init__(x, y, flower_path, constants.FLOWER)

# Rose
# Rosa
class Rose(GameElement):
    def __init__(self, x, y):
        # Define the image path for the rose
        # Define la ruta de la imagen para la rosa
        rose_path = os.path.join('assets', 'images', 'objects', 'rose.png')
        # Call the constructor of the base class
        # Llama al constructor de la clase base
        super().__init__(x, y, rose_path, constants.FLOWER) # Assumes roses have the same size constant as flowers / Asume que las rosas tienen la misma constante de tamaño que las flores
        self.rose = 1 # Amount of roses / Cantidad de rosas

    def collect(self):
        # Decrease the rose amount and return True if successful
        # Disminuye la cantidad de rosas y retorna True si tiene éxito
        if self.rose > 0:
            self.rose -= 1
            return True
        return False # Return False if no roses left / Retorna False si no quedan rosas
    
# Rose Yellow 
# Rosa amarilla
class RoseYellow(GameElement):
    def __init__(self, x, y):
        # Define the image path for the yellow rose
        # Define la ruta de la imagen para la rosa amarilla
        rose_path = os.path.join('assets', 'images', 'objects', 'rose-yellow.png')
        # Call the constructor of the base class
        # Llama al constructor de la clase base
        super().__init__(x, y, rose_path, constants.FLOWER) # Assumes yellow roses have the same size constant as flowers / Asume que las rosas amarillas tienen la misma constante de tamaño que las flores
        self.rose_yellow = 1 # Amount of yellow roses / Cantidad de rosas amarillas

    def collect(self):
        # Decrease the yellow rose amount and return True if successful
        # Disminuye la cantidad de rosas amarillas y retorna True si tiene éxito
        if self.rose_yellow > 0:
            self.rose_yellow -= 1
            return True
        return False # Return False if no yellow roses left / Retorna False si no quedan rosas amarillas

# Grass 1
# Pasto 1
class Grass1(GameElement):
    def __init__(self, x, y):
        # Define the image path for grass type 1
        # Define la ruta de la imagen para el pasto tipo 1
        grass_path = os.path.join('assets', 'images', 'objects', 'grass1.png')
        # Call the constructor of the base class
        # Llama al constructor de la clase base
        super().__init__(x, y, grass_path, constants.GRASS_OBJ)

# Grass 2
# Pasto 2
class Grass2(GameElement):
    def __init__(self, x, y):
        # Define the image path for grass type 2
        # Define la ruta de la imagen para el pasto tipo 2
        grass_path = os.path.join('assets', 'images', 'objects', 'grass2.png')
        # Call the constructor of the base class
        # Llama al constructor de la clase base
        super().__init__(x, y, grass_path, constants.GRASS_OBJ)

# Grass 3
# Pasto 3
class Grass3(GameElement):
    def __init__(self, x, y):
        # Define the image path for grass type 3
        # Define la ruta de la imagen para el pasto tipo 3
        grass_path = os.path.join('assets', 'images', 'objects', 'grass3.png')
        # Call the constructor of the base class
        # Llama al constructor de la clase base
        super().__init__(x, y, grass_path, constants.GRASS_OBJ)

# Farm Land
# Tierra de cultivo
class FarmLand:
    def __init__(self, x, y):
        self.x = x # X-coordinate of the farmland tile / Coordenada X del tile de tierra de cultivo
        self.y = y # Y-coordinate of the farmland tile / Coordenada Y del tile de tierra de cultivo
        # Define the image path for farmland
        # Define la ruta de la imagen para la tierra de cultivo
        farmland_path = os.path.join('assets', 'images', 'objects', 'FarmLand.png')
        # Load and scale the image, preserving transparency
        # Carga y escala la imagen, conservando la transparencia
        self.image = pygame.image.load(farmland_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.GRASS, constants.GRASS))
        self.size = self.image.get_width() # Get the actual width of the scaled image / Obtiene el ancho real de la imagen escalada

    def draw(self, screen, camera_x, camera_y):
        # Calculate the screen coordinates based on the camera position
        # Calcula las coordenadas en pantalla basándose en la posición de la cámara
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        # Draw the farmland tile only if it's visible on the screen
        # Dibuja el tile de tierra de cultivo solo si es visible en la pantalla
        if(screen_x + self.size >= 0 and screen_x <= constants.WIDTH and
                screen_y + self.size >= 0 and screen_y <= constants.HEIGHT):
            screen.blit(self.image, (screen_x, screen_y))

# Water
# Agua
class Water:
    def __init__(self, x, y):
        self.x = x # X-coordinate of the water tile / Coordenada X del tile de agua
        self.y = y # Y-coordinate of the water tile / Coordenada Y del tile de agua
        self.size = constants.GRASS # Size of the water tile / Tamaño del tile de agua
        self.time = 0 # Timer for animation / Temporizador para la animación

    def update(self, dt):
        # Update the time for wave animation
        # Actualiza el tiempo para la animación de olas
        self.time += dt * 0.002

    def draw(self, screen, camera_x, camera_y):
        # Calculate the screen coordinates based on the camera position
        # Calcula las coordenadas en pantalla basándose en la posición de la cámara
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        # Draw the water tile only if it's visible on the screen
        # Dibuja el tile de agua solo si es visible en la pantalla
        if (screen_x + self.size >= 0 and screen_x <= constants.WIDTH and
                screen_y + self.size >= 0 and screen_y <= constants.HEIGHT):
            # Create a transparent surface for the water effect
            # Crea una superficie transparente para el efecto de agua
            water_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            # Fill the surface with the water color and a semi-transparent alpha value
            # Rellena la superficie con el color del agua y un valor alfa semi-transparente
            water_surface.fill((*constants.WATER_COLOR, 180))
            
            # Apply a small vertical offset based on a sine wave for a subtle animation effect
            # Aplica un pequeño desplazamiento vertical basado en una onda sinusoidal para un efecto de animación sutil
            wave_offset = int(math.sin(self.time) * 1.5)
            screen.blit(water_surface, (screen_x, screen_y + wave_offset))