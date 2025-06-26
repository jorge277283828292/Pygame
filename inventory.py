import pygame
import constants
import os

# InventoryItem class to represent individual items in the inventory
# Clase InventoryItem para representar ítems individuales en el inventario
class InventoryItem:
    def __init__(self, name, image_path, quantity=1):
        self.name = name # Name of the item / Nombre del ítem
        self.quantity = quantity # Quantity of the item / Cantidad del ítem
        # Load the item's image and convert it with alpha for transparency
        # Carga la imagen del ítem y la convierte con alfa para transparencia
        self.image = pygame.image.load(image_path).convert_alpha()
        # Scale the image to fit within an inventory slot
        # Escala la imagen para que quepa dentro de un slot del inventario
        self.image = pygame.transform.scale(self.image, (constants.SLOT_SIZE - 10, constants.SLOT_SIZE - 10))
        self.dragging = False # Flag to indicate if the item is being dragged / Bandera para indicar si el ítem está siendo arrastrado
        self.drag_offset = (0, 0) # Offset for dragging to keep the mouse centered on the item / Desplazamiento para arrastrar y mantener el ratón centrado en el ítem

# Inventory class to manage all inventory-related logic and drawing
# Clase Inventory para manejar toda la lógica y el dibujo relacionados con el inventario
class Inventory:
    def __init__(self):
        self.left_hand = None # Item in the left hand slot / Ítem en el slot de la mano izquierda
        self.right_hand = None # Item in the right hand slot / Ítem en el slot de la mano derecha
        # Hotbar slots, initialized to None / Slots de la barra de acceso rápido, inicializados a None
        self.hotbar = [None] * constants.HOTBAR_SLOTS
        # Main inventory grid, initialized to None / Cuadrícula de inventario principal, inicializada a None
        self.inventory = [[None for _ in range(constants.INVENTORY_COLS)] for _ in range(constants.INVENTORY_ROWS)]
        # Crafting grid, initialized to None / Cuadrícula de crafteo, inicializada a None
        self.crafting_grid = [[None for _ in range(constants.CRAFTING_GRID_SIZE)] for _ in range(constants.CRAFTING_GRID_SIZE)]
        self.dragged_item = None # Item currently being dragged / Ítem actualmente arrastrado
        self.crafting_result = None # Result of the current crafting recipe / Resultado de la receta de crafteo actual
        self.font = pygame.font.Font(None, 24) # Font for rendering text (e.g., quantity) / Fuente para renderizar texto (ej. cantidad)

        # Dictionary mapping item names to their image paths
        # Diccionario que mapea los nombres de los ítems a las rutas de sus imágenes
        self.item_images = {
            'tree': os.path.join('assets', 'images', 'objects', 'tree.png'),
            'stone': os.path.join('assets', 'images', 'objects', 'stone.png'),
            'flower': os.path.join('assets', 'images', 'objects', 'flowers.png'),
            'rose': os.path.join('assets', 'images', 'objects', 'rose.png'),
            'rose_yellow': os.path.join('assets', 'images', 'objects', 'rose-yellow.png'),
            'wood': os.path.join('assets', 'images', 'objects', 'wood.png'),
            'axe' : os.path.join('assets', 'images', 'objects', 'axe.png'),
            'bunch': os.path.join('assets', 'images', 'objects', 'bunch.png'),
            'stick': os.path.join('assets', 'images', 'objects', 'stick_stone.png'),
            'hoe': os.path.join('assets', 'images', 'objects', 'hoe.png'),
            'bucket': os.path.join('assets', 'images', 'objects', 'bucket.png'),
            'water_bucket': os.path.join('assets', 'images', 'objects', 'full_bucket.png')
        }

        # Dictionary defining crafting recipes
        # Diccionario que define las recetas de crafteo
        self.recipes = {
            'axe': {
                'pattern': [('wood', 'stone'), (None, None)], # Recipe pattern / Patrón de la receta
                'result': 'axe' # Item crafted / Ítem crafteado
            },
            'bunch': {
                'pattern': [('rose', 'rose_yellow'), (None, None)],
                'result': 'bunch'
            },
            'stick': {
                'pattern': [('stone', None), (None, 'wood')],
                'result': 'stick'
            },
            'hoe': {
                'pattern': [(None, 'wood'), ('stone', 'stone')], 
                'result': 'hoe'
            },
            'bucket': {
                'pattern': [('stone', 'wood'), ('wood', 'wood')], 
                'result': 'bucket'
            }
        }
    
    # Method to add an item to the inventory
    # Método para añadir un ítem al inventario
    def add_item(self, item_name, quantity=1):
        # First, try to add to existing stacks in the hotbar
        # Primero, intenta añadir a pilas existentes en la hotbar
        for i, slot in enumerate(self.hotbar):
            if slot and slot.name == item_name:
                slot.quantity += quantity
                return True
            
        # Then, try to add to existing stacks in the main inventory
        # Luego, intenta añadir a pilas existentes en el inventario principal
        for row in range(constants.INVENTORY_ROWS):
            for col in range(constants.INVENTORY_COLS):
                if self.inventory[row][col] and self.inventory[row][col].name == item_name:
                    self.inventory[row][col].quantity += quantity
                    return True
                
        # If no existing stack, find an empty slot in the hotbar
        # Si no hay pila existente, busca un slot vacío en la hotbar
        for i, slot in enumerate(self.hotbar):
            if slot is None:
                self.hotbar[i] = InventoryItem(item_name, self.item_images[item_name], quantity)
                return True
            
        # If no empty hotbar slot, find an empty slot in the main inventory
        # Si no hay slot vacío en la hotbar, busca un slot vacío en el inventario principal
        for row in range(constants.INVENTORY_ROWS):
            for col in range(constants.INVENTORY_COLS):
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = InventoryItem(item_name, self.item_images[item_name], quantity)
                    return True 
        return False # Inventory is full / El inventario está lleno
    
    # Method to draw the inventory on the screen
    # Método para dibujar el inventario en la pantalla
    def draw(self, screen, camera_x=0, camera_y=0, show_inventory=False):
        # Draw hand slots
        # Dibuja los slots de la mano
        self._draw_hand_slots(screen)
        # Draw the hotbar
        # Dibuja la hotbar
        self._draw_hotbar(screen)
        # Draw the main inventory and crafting grid if the inventory is open
        # Dibuja el inventario principal y la cuadrícula de crafteo si el inventario está abierto
        if show_inventory:
            self._draw_main_inventory(screen)
            self._draw_crafting_grid(screen)
        # Draw the dragged item if one exists
        # Dibuja el ítem arrastrado si existe
        if self.dragged_item:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            offset_x, offset_y = self.dragged_item.drag_offset
            screen.blit(self.dragged_item.image, (mouse_x - offset_x, mouse_y - offset_y))
            # Draw the quantity if more than one
            # Dibuja la cantidad si es más de uno
            if self.dragged_item.quantity > 1:
                text = self.font.render(str(self.dragged_item.quantity), True, constants.WHITE)
                text_rect = text.get_rect()
                # Position the quantity text at the bottom right of the item
                # Posiciona el texto de cantidad en la esquina inferior derecha del ítem
                text_rect.bottomright = (mouse_x + constants.SLOT_SIZE // 2, mouse_y + constants.SLOT_SIZE // 2)
                screen.blit(text, text_rect)

    # Helper method to draw the hotbar slots
    # Método auxiliar para dibujar los slots de la hotbar
    def _draw_hotbar(self, screen):
        for i in range(constants.HOTBAR_SLOTS):
            x = constants.HOTBAR_X + (i * constants.SLOT_SIZE)
            y = constants.HOTBAR_Y

            # Draw slot border
            # Dibujar borde del slot
            pygame.draw.rect(screen, constants.SLOT_BORDER,
                                (x, y, constants.SLOT_SIZE, constants.SLOT_SIZE))

            # Draw slot background
            # Dibujar fondo del slot
            pygame.draw.rect(screen, constants.SLOT_COLOR,
                                (x + 2, y + 2, constants.SLOT_SIZE - 4, constants.SLOT_SIZE - 4))

            # Draw the item in the slot if it exists
            # Dibujar el ítem en el slot si existe
            if self.hotbar[i]:
                self._draw_item(screen, self.hotbar[i], x, y)

    # Helper method to draw the main inventory grid
    # Método auxiliar para dibujar la cuadrícula del inventario principal
    def _draw_main_inventory(self, screen):
        for row in range(constants.INVENTORY_ROWS):
            for col in range(constants.INVENTORY_COLS):
                x = constants.INVENTORY_X + (col * constants.SLOT_SIZE)
                y = constants.INVENTORY_Y + (row * constants.SLOT_SIZE)

                # Draw slot border
                # Dibujar borde del slot
                pygame.draw.rect(screen, constants.SLOT_BORDER,
                                    (x, y, constants.SLOT_SIZE, constants.SLOT_SIZE))

                # Draw slot background
                # Dibujar fondo del slot
                pygame.draw.rect(screen, constants.SLOT_COLOR,
                                    (x + 2, y + 2, constants.SLOT_SIZE - 4, constants.SLOT_SIZE - 4))
                
                # Draw the item in the slot if it exists
                # Dibujar el ítem en el slot si existe
                if self.inventory[row][col]:
                    self._draw_item(screen, self.inventory[row][col], x, y)

    # Helper method to draw an individual item and its quantity
    # Método auxiliar para dibujar un ítem individual y su cantidad
    def _draw_item(self, screen, item, x, y):
        # Calculate item position to center it within the slot
        # Calcula la posición del ítem para centrarlo dentro del slot
        item_x = x + (constants.SLOT_SIZE - item.image.get_width()) // 2
        item_y = y + (constants.SLOT_SIZE - item.image.get_width()) // 2
        screen.blit(item.image, (item_x, item_y))

        # Draw the quantity if greater than 1
        # Dibuja la cantidad si es mayor que 1
        if item.quantity > 1:
            text = self.font.render (str(item.quantity), True, constants.WHITE)
            text_rect = text.get_rect()
            # Position the quantity text at the bottom right of the slot
            # Posiciona el texto de cantidad en la esquina inferior derecha del slot
            text_rect.bottomright = (x + constants.SLOT_SIZE - 5, y + constants.SLOT_SIZE - 5)
            screen.blit(text, text_rect)

    # Helper method to draw the hand slots
    # Método auxiliar para dibujar los slots de la mano
    def _draw_hand_slots(self, screen):
        # Draw left hand slot border
        # Dibujar borde del slot de la mano izquierda
        pygame.draw.rect(screen, constants.SLOT_BORDER,
                             (constants.LEFT_HAND_SLOT_X, constants.LEFT_HAND_SLOT_Y,
                              constants.SLOT_SIZE, constants.SLOT_SIZE))
        # Draw left hand slot background
        # Dibujar fondo del slot de la mano izquierda
        pygame.draw.rect(screen, constants.SLOT_COLOR,
                             (constants.LEFT_HAND_SLOT_X + 2, constants.LEFT_HAND_SLOT_Y + 2,
                              constants.SLOT_SIZE - 4, constants.SLOT_SIZE - 4))
        # Draw item in left hand if it exists
        # Dibujar ítem en la mano izquierda si existe
        if self.left_hand:
            self._draw_item(screen, self.left_hand,
                             constants.LEFT_HAND_SLOT_X,
                             constants.LEFT_HAND_SLOT_Y)
        
        # Draw right hand slot border
        # Dibujar borde del slot de la mano derecha
        pygame.draw.rect(screen, constants.SLOT_BORDER,
                   (constants.RIGHT_HAND_SLOT_X, constants.RIGHT_HAND_SLOT_Y,
                    constants.SLOT_SIZE, constants.SLOT_SIZE))
        # Draw right hand slot background
        # Dibujar fondo del slot de la mano derecha
        pygame.draw.rect(screen, constants.SLOT_COLOR,
                         (constants.RIGHT_HAND_SLOT_X + 2, constants.RIGHT_HAND_SLOT_Y + 2,
                          constants.SLOT_SIZE - 4, constants.SLOT_SIZE - 4))
        # Draw item in right hand if it exists
        # Dibujar ítem en la mano derecha si existe
        if self.right_hand:
            self._draw_item(screen, self.right_hand,
                             constants.RIGHT_HAND_SLOT_X,
                             constants.RIGHT_HAND_SLOT_Y)

    # Method to handle mouse clicks on inventory slots
    # Método para manejar clics del ratón en los slots del inventario
    def handle_click(self, pos, button, show_inventory=False):
        mouse_x, mouse_y = pos

        # Check if click is on left hand slot
        # Comprueba si el clic es en el slot de la mano izquierda
        if (constants.LEFT_HAND_SLOT_X <= mouse_x <= constants.LEFT_HAND_SLOT_X + constants.SLOT_SIZE and
            constants.LEFT_HAND_SLOT_Y <= mouse_y <= constants.LEFT_HAND_SLOT_Y + constants.SLOT_SIZE):
            self._handle_hand_slot_click(button, 'left')
            return True

        # Check if click is on right hand slot
        # Comprueba si el clic es en el slot de la mano derecha
        if (constants.RIGHT_HAND_SLOT_X <= mouse_x <= constants.RIGHT_HAND_SLOT_X + constants.SLOT_SIZE and
            constants.RIGHT_HAND_SLOT_Y <= mouse_y <= constants.RIGHT_HAND_SLOT_Y + constants.SLOT_SIZE):
            self._handle_hand_slot_click(button, 'right')
            return True

        # Check if click is on hotbar slots
        # Comprueba si el clic es en los slots de la hotbar
        if constants.HOTBAR_Y <= mouse_y <= constants.HOTBAR_Y + constants.SLOT_SIZE:
            slot_index = (mouse_x - constants.HOTBAR_X) // constants.SLOT_SIZE
            if 0 <= slot_index < constants.HOTBAR_SLOTS:
                self._handle_slot_click(button, self.hotbar, slot_index,
                                        constants.HOTBAR_X + (slot_index * constants.SLOT_SIZE),
                                        constants.HOTBAR_Y)
                return True
        
        # Check if inventory is open and click is within main inventory or crafting grid
        # Comprueba si el inventario está abierto y el clic está dentro del inventario principal o la cuadrícula de crafteo
        if show_inventory:
            # Check if click is on main inventory grid
            # Comprueba si el clic es en la cuadrícula del inventario principal
            if constants.INVENTORY_Y <= mouse_y <= constants.INVENTORY_Y + \
                    (constants.INVENTORY_ROWS * constants.SLOT_SIZE):
                row = (mouse_y - constants.INVENTORY_Y) // constants.SLOT_SIZE
                col = (mouse_x - constants.INVENTORY_X) // constants.SLOT_SIZE
                if (0 <= row < constants.INVENTORY_ROWS and
                        0 <= col < constants.INVENTORY_COLS):
                    self._handle_grid_slot_click(button, row, col,
                                                 constants.INVENTORY_X + (col * constants.SLOT_SIZE),
                                                 constants.INVENTORY_Y + (row * constants.SLOT_SIZE))
                    return True

            # Check if click is on crafting grid
            # Comprueba si el clic es en la cuadrícula de crafteo
            if constants.CRAFTING_GRID_Y <= mouse_y <= constants.CRAFTING_GRID_Y + (
                constants.CRAFTING_GRID_SIZE * constants.SLOT_SIZE):
                row = (mouse_y - constants.CRAFTING_GRID_Y) // constants.SLOT_SIZE
                col = (mouse_x - constants.CRAFTING_GRID_X) // constants.SLOT_SIZE
                if (0 <= row < constants.CRAFTING_GRID_SIZE 
                    and 0 <= col < constants.CRAFTING_GRID_SIZE):
                    self._handle_crafting_grid_click(button, row, col)
                    return True

        # This block handles the crafting result slot click and should be outside the previous 'if show_inventory'
        # Este bloque maneja el clic en el slot del resultado de crafteo y debe estar fuera del 'if show_inventory' anterior
        if (constants.CRAFTING_RESULT_SLOT_X <= mouse_x <= constants.CRAFTING_RESULT_SLOT_X + constants.SLOT_SIZE and
            constants.CRAFTING_RESULT_SLOT_Y <= mouse_y <= constants.CRAFTING_RESULT_SLOT_Y + constants.SLOT_SIZE):
            self._handle_crafting_result_click(button)
            return True

        # If an item is being dragged and the click is a left click outside any valid slot, return the item to its origin
        # Si un ítem está siendo arrastrado y el clic es un clic izquierdo fuera de cualquier slot válido, devuelve el ítem a su origen
        if self.dragged_item and button == 1:
            self._return_dragged_item() 
        return False # No relevant slot was clicked / No se hizo clic en ningún slot relevante
    
    # Helper method to handle clicks on generic slots (hotbar)
    # Método auxiliar para manejar clics en slots genéricos (hotbar)
    def _handle_slot_click(self, button, slot_list, index, slot_x, slot_y):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.dragged_item:
            # Drop item
            # Soltar ítem
            if slot_list[index] is None:
                slot_list[index] = self.dragged_item
            else:
                # Swap items
                # Intercambiar ítems
                slot_list[index], self.dragged_item = self.dragged_item, slot_list[index]
                return # Exit after swapping to prevent further action / Salir después de intercambiar para evitar acciones adicionales
            self.dragged_item = None # Clear dragged item after dropping / Limpiar ítem arrastrado después de soltar
        elif slot_list[index]:
            # Start dragging item
            # Comenzar a arrastrar ítem
            self.dragged_item = slot_list[index]
            slot_list[index] = None # Clear the original slot / Limpiar el slot original
            # Calculate offset for centered dragging
            # Calcular offset para el arrastre centrado
            item_rect = self.dragged_item.image.get_rect()
            item_rect.x = slot_x
            item_rect.y = slot_y
            self.dragged_item.drag_offset = (mouse_x - item_rect.centerx,
                                             mouse_y - item_rect.centery)
            
    # Helper method to handle clicks on the main inventory grid slots
    # Método auxiliar para manejar clics en los slots de la cuadrícula del inventario principal
    def _handle_grid_slot_click(self, button, row, col, slot_x, slot_y):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos
        if button == 1:  # Left click / Clic izquierdo
            if self.dragged_item:
                # Drop item
                # Soltar ítem
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = self.dragged_item
                else:
                    # Swap items
                    # Intercambiar ítems
                    self.inventory[row][col], self.dragged_item = self.dragged_item, self.inventory[row][col]
                    return # Exit after swapping / Salir después de intercambiar
                self.dragged_item = None # Clear dragged item after dropping / Limpiar ítem arrastrado después de soltar
            elif self.inventory[row][col]:
                # Start dragging
                # Comenzar a arrastrar
                self.dragged_item = self.inventory[row][col]
                self.inventory[row][col] = None # Clear the original slot / Limpiar el slot original
                # Calculate offset for centered dragging
                # Calcular offset para el arrastre centrado
                item_rect = self.dragged_item.image.get_rect()
                item_rect.x = slot_x
                item_rect.y = slot_y
                self.dragged_item.drag_offset = (mouse_x - item_rect.centerx,
                                                 mouse_y - item_rect.centery)
    
    # Helper method to handle clicks on hand slots
    # Método auxiliar para manejar clics en los slots de la mano
    def _handle_hand_slot_click(self, button, hand):
        if button == 1: # Left click / Clic izquierdo
            if hand == 'left':
                if self.dragged_item:
                    # Swap items between dragged item and left hand
                    # Intercambiar ítems entre el ítem arrastrado y la mano izquierda
                    self.left_hand, self.dragged_item = self.dragged_item, self.left_hand
                else:
                    if self.left_hand:
                        # Start dragging item from left hand
                        # Comenzar a arrastrar ítem desde la mano izquierda
                        self.dragged_item = self.left_hand
                        self.left_hand = None
            elif hand == 'right':
                if self.dragged_item:
                    # Swap items between dragged item and right hand
                    # Intercambiar ítems entre el ítem arrastrado y la mano derecha
                    self.right_hand, self.dragged_item = self.dragged_item, self.right_hand
                else:
                    if self.right_hand:
                        # Start dragging item from right hand
                        # Comenzar a arrastrar ítem desde la mano derecha
                        self.dragged_item = self.right_hand
                        self.right_hand = None
    
    # Check if an axe is equipped in either hand
    # Comprueba si hay un hacha equipada en alguna de las manos
    def has_axe_equipped(self):
        return (
            (self.left_hand and self.left_hand.name == 'axe') or
            (self.right_hand and self.right_hand.name == 'axe')
        )
    
    # Check if a hoe is equipped in either hand
    # Comprueba si hay una azada equipada en alguna de las manos
    def has_hoe_equipped(self):
        return (
            (self.left_hand and self.left_hand.name == 'hoe') or
            (self.right_hand and self.right_hand.name == 'hoe')
        )
    
    # Check if an empty bucket is equipped, returns True and the hand ('left'/'right') if found
    # Comprueba si hay una cubeta vacía equipada, retorna True y la mano ('left'/'right') si se encuentra
    def has_bucket_equipped(self):
        if self.left_hand and self.left_hand.name == 'bucket':
            return True, 'left'
        if self.right_hand and self.right_hand.name == 'bucket':
            return True, 'right'
        return False, None
    
    # Check if a water bucket is equipped, returns True and the hand ('left'/'right') if found
    # Comprueba si hay una cubeta con agua equipada, retorna True y la mano ('left'/'right') si se encuentra
    def has_water_bucket_equipped(self):
        if self.left_hand and self.left_hand.name == 'water_bucket':
            return True, 'left'
        if self.right_hand and self.right_hand.name == 'water_bucket':
            return True, 'right'
        return False, None
    
    # Empties a water bucket from the specified hand, replacing it with an empty bucket
    # Vacía una cubeta con agua de la mano especificada, reemplazándola por una cubeta vacía
    def empty_bucket(self, hand):
        if hand == 'left' and self.left_hand and self.left_hand.name == 'water_bucket':
            # Replace full bucket with empty bucket
            # Reemplazar cubeta llena por cubeta vacía
            self.left_hand = InventoryItem('bucket', self.item_images['bucket'])
            return True
        elif hand == 'right' and self.right_hand and self.right_hand.name == 'water_bucket':
            # Replace full bucket with empty bucket
            # Reemplazar cubeta llena por cubeta vacía
            self.right_hand = InventoryItem('bucket', self.item_images['bucket'])
            return True
        return False

    # Fills an empty bucket in the specified hand with water
    # Llena una cubeta vacía en la mano especificada con agua
    def fill_bucket(self, hand):    
        if hand == 'left' and self.left_hand and self.left_hand.name == 'bucket':
            self.left_hand = InventoryItem('water_bucket', self.item_images['water_bucket'])
            return True
        elif hand == 'right' and self.right_hand and self.right_hand.name == 'bucket':
            self.right_hand = InventoryItem('water_bucket', self.item_images['water_bucket'])
            return True
        return False
    
    # Returns a dragged item to an empty slot in the hotbar or main inventory
    # Devuelve un ítem arrastrado a un slot vacío en la hotbar o en el inventario principal
    def _return_dragged_item(self):
        # Try to return to hotbar first
        # Intentar devolver a la hotbar primero
        for i, slot in enumerate(self.hotbar):
            if slot is None:
                self.hotbar[i] = self.dragged_item
                self.dragged_item = None
                return
            
        # Then try to return to main inventory
        # Luego intentar devolver al inventario principal
        for row in range(constants.INVENTORY_ROWS):
            for col in range(constants.INVENTORY_COLS):
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = self.dragged_item
                    self.dragged_item = None
                    return
                
    # Helper method to draw the crafting grid and result slot
    # Método auxiliar para dibujar la cuadrícula de crafteo y el slot de resultado
    def _draw_crafting_grid(self, screen):
        # Draw crafting grid slots
        # Dibujar slots de la cuadrícula de crafteo
        for row in range(constants.CRAFTING_GRID_SIZE):
            for col in range(constants.CRAFTING_GRID_SIZE):
                x = constants.CRAFTING_GRID_X + (col * constants.SLOT_SIZE)
                y = constants.CRAFTING_GRID_Y + (row * constants.SLOT_SIZE)

                # Draw slot border
                # Dibujar borde del slot
                pygame.draw.rect(screen, constants.SLOT_BORDER,
                                    (x, y, constants.SLOT_SIZE, constants.SLOT_SIZE))
                # Draw slot background
                # Dibujar fondo del slot
                pygame.draw.rect(screen, constants.SLOT_COLOR,
                                    (x + 2, y + 2, constants.SLOT_SIZE - 4, constants.SLOT_SIZE - 4))

                # Draw item if it exists in the crafting grid
                # Dibujar ítem si existe en la cuadrícula de crafteo
                if self.crafting_grid[row][col]:
                    self._draw_item(screen, self.crafting_grid[row][col], x, y)

        # Draw crafting result slot border
        # Dibujar borde del slot de resultado de crafteo
        pygame.draw.rect(screen, constants.SLOT_BORDER,
            (constants.CRAFTING_RESULT_SLOT_X, constants.CRAFTING_RESULT_SLOT_Y,
            constants.SLOT_SIZE, constants.SLOT_SIZE))
        # Draw crafting result slot background
        # Dibujar fondo del slot de resultado de crafteo
        pygame.draw.rect(screen, constants.SLOT_COLOR,
            (constants.CRAFTING_RESULT_SLOT_X + 2, constants.CRAFTING_RESULT_SLOT_Y + 2,
            constants.SLOT_SIZE - 4, constants.SLOT_SIZE - 4))
        
        # Draw the crafting result item if it exists
        # Dibujar el ítem resultado del crafteo si existe
        if self.crafting_result:
            self._draw_item(screen, self.crafting_result,
                            constants.CRAFTING_RESULT_SLOT_X,
                            constants.CRAFTING_RESULT_SLOT_Y)

    # Handles clicks on the crafting result slot
    # Maneja los clics en el slot de resultado de crafteo
    def _handle_crafting_result_click(self, button):
        if button == 1 and self.crafting_result:
            # Add the crafted item to the inventory
            # Añade el ítem crafteado al inventario
            self.add_item(self.crafting_result.name, self.crafting_result.quantity)
            # Consume the materials used in crafting
            # Consume los materiales usados en el crafteo
            for row in range(constants.CRAFTING_GRID_ROWS):
                for col in range(constants.CRAFTING_GRID_COLS):
                    item = self.crafting_grid[row][col]
                    if item:
                        if item.quantity > 1:
                            item.quantity -= 1 # Decrease quantity if more than one / Disminuye la cantidad si es más de uno
                        else:
                            self.crafting_grid[row][col] = None # Remove item if quantity is 1 / Elimina el ítem si la cantidad es 1
            self.crafting_result = None # Clear the crafting result / Limpiar el resultado de crafteo
            self.update_crafting_result() # Update the crafting result after consuming items / Actualiza el resultado de crafteo después de consumir ítems

    # Checks the crafting grid against known recipes to determine a result
    # Comprueba la cuadrícula de crafteo contra las recetas conocidas para determinar un resultado
    def _check_recipe(self):
        current_pattern = []
        for row in range(constants.CRAFTING_GRID_SIZE):
            pattern_row = []
            for col in range(constants.CRAFTING_GRID_SIZE):
                item = self.crafting_grid[row][col]
                pattern_row.append(item.name if item else None)
            current_pattern.append(tuple(pattern_row))

        for recipe_name, recipe in self.recipes.items():
            matches = True
            for row in range(constants.CRAFTING_GRID_SIZE):
                for col in range(constants.CRAFTING_GRID_SIZE):
                    expected = recipe['pattern'][row][col]
                    actual = current_pattern[row][col]
                    if expected != actual:
                        matches = False
                        break
                if not matches:
                    break

            if matches:
                # If a match is found, create the InventoryItem for the result
                # Si se encuentra una coincidencia, crea el InventoryItem para el resultado
                self.crafting_result = InventoryItem(recipe['result'],
                                                     self.item_images[recipe['result']])
                return # Exit once a recipe is found / Salir una vez que se encuentra una receta
            
        self.crafting_result = None # No recipe found, clear result / No se encontró receta, limpiar resultado

    # Clears the crafting grid and returns items to the inventory
    # Limpia la cuadrícula de crafteo y devuelve los ítems al inventario
    def clear_crafting_grid(self):
        for row in self.crafting_grid:
            for item in row:
                if item:
                    self.add_item(item.name, item.quantity) # Add items back to inventory / Añade ítems de vuelta al inventario
        # Reset the crafting grid to empty
        # Reinicia la cuadrícula de crafteo a vacía
        self.crafting_grid = [[None for _ in range(constants.CRAFTING_GRID_COLS)] for _ in range(constants.CRAFTING_GRID_ROWS)]
        self.update_crafting_result() # Update the crafting result after clearing / Actualiza el resultado de crafteo después de limpiar

    # Handles clicks on the crafting grid slots
    # Maneja los clics en los slots de la cuadrícula de crafteo
    def _handle_crafting_grid_click(self, button, row, col):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if button == 1:  # Left click / Clic izquierdo
            if self.dragged_item:
                # Drop item into the crafting grid
                # Soltar ítem en la cuadrícula de crafteo
                if self.crafting_grid[row][col] is None:
                    self.crafting_grid[row][col] = self.dragged_item
                    self.dragged_item = None
                else:
                    # Swap items
                    # Intercambiar ítems
                    self.crafting_grid[row][col], self.dragged_item = self.dragged_item, self.crafting_grid[row][col]
                    return # Exit after swapping / Salir después de intercambiar
            elif self.crafting_grid[row][col]:
                # Start dragging item from crafting grid
                # Comenzar a arrastrar ítem desde la cuadrícula de crafteo
                self.dragged_item = self.crafting_grid[row][col]
                self.crafting_grid[row][col] = None
                # Calculate offset for centered dragging
                # Calcular offset para el arrastre centrado
                item_rect = self.dragged_item.image.get_rect()
                item_rect.x = constants.CRAFTING_GRID_X + (col * constants.SLOT_SIZE)
                item_rect.y = constants.CRAFTING_GRID_Y + (row * constants.SLOT_SIZE)
                self.dragged_item.drag_offset = (mouse_x - item_rect.centerx, mouse_y - item_rect.centery)
        # Update the crafting result after each change in the grid
        # Actualiza el resultado de crafteo después de cada cambio en la cuadrícula
        self._check_recipe()

    # Updates the crafting result based on the current crafting grid content
    # Actualiza el resultado de crafteo basándose en el contenido actual de la cuadrícula de crafteo
    def update_crafting_result(self):
        crafted_item = self.check_crafting() # Get the name of the crafted item / Obtiene el nombre del ítem crafteado
        if crafted_item:
            # If a crafted item name is returned, create the InventoryItem object
            # Si se devuelve un nombre de ítem crafteado, crea el objeto InventoryItem
            self.crafting_result = InventoryItem(
                crafted_item,
                self.item_images[crafted_item],
                1 # Assume quantity is 1 for crafted items unless recipe specifies otherwise
                  # Asume que la cantidad es 1 para ítems crafteados a menos que la receta especifique lo contrario
            )
        else:
            self.crafting_result = None # No recipe matched, clear the result / Ninguna receta coincide, limpiar el resultado

    # Checks the crafting grid against recipes and returns the name of the crafted item if a match is found
    # Comprueba la cuadrícula de crafteo contra las recetas y devuelve el nombre del ítem crafteado si se encuentra una coincidencia
    def check_crafting(self):
        current_pattern = []
        for row in range(constants.CRAFTING_GRID_SIZE):
            pattern_row = []
            for col in range(constants.CRAFTING_GRID_SIZE):
                item = self.crafting_grid[row][col]
                pattern_row.append(item.name if item else None)
            current_pattern.append(tuple(pattern_row))

        for recipe in self.recipes.values():
            matches = True
            for row in range(constants.CRAFTING_GRID_SIZE):
                for col in range(constants.CRAFTING_GRID_SIZE):
                    expected = recipe['pattern'][row][col]
                    actual = current_pattern[row][col]
                    if expected != actual:
                        matches = False
                        break
                if not matches:
                    break
            if matches:
                return recipe['result'] # Return the name of the crafted item / Retorna el nombre del ítem crafteado
        return None # No recipe found / No se encontró receta