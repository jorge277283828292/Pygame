import pygame
import constants
import os

class InventoryItem:
    def __init__(self, name, image_path, quantity=1):
        self.name = name 
        self.quantity = quantity
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.SLOT_SIZE - 10, constants.SLOT_SIZE - 10))
        self.dragging = False
        self.drag_offset = (0, 0)

class Inventory:
    def __init__(self):
        self.left_hand = None
        self.right_hand = None
        self.hotbar = [None] * constants.HOTBAR_SLOTS
        self.inventory = [[None for _ in range(constants.INVENTORY_COLS)] for _ in range(constants.INVENTORY_ROWS)]
        self.crafting_grid = [[None for _ in range(constants.CRAFTING_GRID_SIZE)] for _ in range(constants.CRAFTING_GRID_SIZE)]
        self.dragged_item = None
        self.crafting_result = None
        self.font = pygame.font.Font(None, 24)

        self.item_images = {
            'tree': os.path.join('assets', 'images', 'objects', 'tree.png'),
            'stone': os.path.join('assets', 'images', 'objects', 'stone.png'),
            'flower': os.path.join('assets', 'images', 'objects', 'flowers.png'),
            'rose': os.path.join('assets', 'images', 'objects', 'rose.png'),
            'rose_yellow': os.path.join('assets', 'images', 'objects', 'rose-yellow.png'),
            'wood': os.path.join('assets', 'images', 'objects', 'wood.png'),
            'axe' : os.path.join('assets', 'images', 'objects', 'axe.png'),
            'bunch': os.path.join('assets', 'images', 'objects', 'bunch.png'),
            'stick': os.path.join('assets', 'images', 'objects', 'stick_stone.png')
        }

        self.recipes = {
            'axe': {
                'pattern': [('wood', 'stone'), (None, None)],
                'result': 'axe'
            },
            'bunch': {
                'pattern': [('rose', 'rose_yellow'), (None, None)],
                'result': 'bunch'
            },
            'stick': {
                'pattern': [('stone', None), (None, 'wood')],
                'result': 'stick'
            }
        }
    
    def add_item(self, item_name, quantity=1):
        for i, slot in enumerate(self.hotbar):
            if slot and slot.name == item_name:
                slot.quantity += quantity
                return True
            
        for row in range(constants.INVENTORY_ROWS):
            for col in range(constants.INVENTORY_COLS):
                if self.inventory[row][col] and self.inventory[row][col].name == item_name:
                    self.inventory[row][col].quantity += quantity
                    return True
                
        for i, slot in enumerate(self.hotbar):
            if slot is None:
                self.hotbar[i] = InventoryItem(item_name, self.item_images[item_name], quantity)
                return True
            
        for row in range(constants.INVENTORY_ROWS):
            for col in range(constants.INVENTORY_COLS):
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = InventoryItem(item_name, self.item_images[item_name], quantity)
                    return True 
        return False
    
    def draw(self, screen, camera_x=0, camera_y=0, show_inventory=False):
        screen_x = constants.INVENTORY_X
        screen_y = constants.INVENTORY_Y

        # Dibuja los slots de la mano
        self._draw_hand_slots(screen)
        # Dibuja el hotbar
        self._draw_hotbar(screen)
        # Dibuja el inventario principal si está abierto
        if show_inventory:
            self._draw_main_inventory(screen)
            self._draw_crafting_grid(screen)
        # Dibuja el item arrastrado si existe
        if self.dragged_item:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            offset_x, offset_y = self.dragged_item.drag_offset
            screen.blit(self.dragged_item.image, (mouse_x - offset_x, mouse_y - offset_y))
            if self.dragged_item.quantity > 1:
                text = self.font.render(str(self.dragged_item.quantity), True, constants.WHITE)
                text_rect = text.get_rect()
                text_rect.bottomright = (mouse_x + constants.SLOT_SIZE // 2, mouse_y + constants.SLOT_SIZE // 2)
                screen.blit(text, text_rect)

    def _draw_hotbar(self, screen):
    # 1 usage
        for i in range(constants.HOTBAR_SLOTS):
            x = constants.HOTBAR_X + (i * constants.SLOT_SIZE)
            y = constants.HOTBAR_Y

            # Dibujar fondo del slot
            pygame.draw.rect(screen, constants.SLOT_BORDER,
                            (x, y, constants.SLOT_SIZE, constants.SLOT_SIZE))

            pygame.draw.rect(screen, constants.SLOT_COLOR,
                            (x + 2, y + 2, constants.SLOT_SIZE - 4, constants.SLOT_SIZE - 4))

            if self.hotbar[i]:
                self._draw_item(screen, self.hotbar[i], x, y)

    def _draw_main_inventory(self, screen):
    # 1 usage
        for row in range(constants.INVENTORY_ROWS):
            for col in range(constants.INVENTORY_COLS):
                x = constants.INVENTORY_X + (col * constants.SLOT_SIZE)
                y = constants.INVENTORY_Y + (row * constants.SLOT_SIZE)

                # Dibujar fondo del slot
                pygame.draw.rect(screen, constants.SLOT_BORDER,
                                (x, y, constants.SLOT_SIZE, constants.SLOT_SIZE))

                pygame.draw.rect(screen, constants.SLOT_COLOR,
                                (x + 2, y + 2, constants.SLOT_SIZE - 4, constants.SLOT_SIZE - 4))
                
                if self.inventory[row][col]:
                    self._draw_item(screen, self.inventory[row][col], x, y)

    def _draw_item(self, screen, item, x, y):
        item_x = x + (constants.SLOT_SIZE - item.image.get_width()) // 2
        item_y = y + (constants.SLOT_SIZE - item.image.get_width()) // 2
        screen.blit(item.image, (item_x, item_y))

        if item.quantity > 1:
            text = self.font.render (str(item.quantity), True, constants.WHITE)
            text_rect = text.get_rect()
            text_rect.bottomright = (x + constants.SLOT_SIZE - 5, y + constants.SLOT_SIZE - 5)
            screen.blit(text, text_rect)

    def _draw_hand_slots(self, screen):
        pygame.draw.rect(screen, constants.SLOT_BORDER,
                         (constants.LEFT_HAND_SLOT_X, constants.LEFT_HAND_SLOT_Y,
                          constants.SLOT_SIZE, constants.SLOT_SIZE))
        pygame.draw.rect(screen, constants.SLOT_COLOR,
                         (constants.LEFT_HAND_SLOT_X + 2, constants.LEFT_HAND_SLOT_Y + 2,
                          constants.SLOT_SIZE - 4, constants.SLOT_SIZE - 4))
        if self.left_hand:
            self._draw_item(screen, self.left_hand,
                            constants.LEFT_HAND_SLOT_X,
                            constants.LEFT_HAND_SLOT_Y)
        
        pygame.draw.rect(screen, constants.SLOT_BORDER,
                 (constants.RIGHT_HAND_SLOT_X, constants.RIGHT_HAND_SLOT_Y,
                  constants.SLOT_SIZE, constants.SLOT_SIZE))
        pygame.draw.rect(screen, constants.SLOT_COLOR,
                        (constants.RIGHT_HAND_SLOT_X + 2, constants.RIGHT_HAND_SLOT_Y + 2,
                        constants.SLOT_SIZE - 4, constants.SLOT_SIZE - 4))
        if self.right_hand:
            self._draw_item(screen, self.right_hand,
                            constants.RIGHT_HAND_SLOT_X,
                            constants.RIGHT_HAND_SLOT_Y)

    def handle_click(self, pos, button, show_inventory=False):
        mouse_x, mouse_y = pos

        if (constants.LEFT_HAND_SLOT_X <= mouse_x <= constants.LEFT_HAND_SLOT_X + constants.SLOT_SIZE and
            constants.LEFT_HAND_SLOT_Y <= mouse_y <= constants.LEFT_HAND_SLOT_Y + constants.SLOT_SIZE):
            self._handle_hand_slot_click(button, 'left')
            return True

        if (constants.RIGHT_HAND_SLOT_X <= mouse_x <= constants.RIGHT_HAND_SLOT_X + constants.SLOT_SIZE and
            constants.RIGHT_HAND_SLOT_Y <= mouse_y <= constants.RIGHT_HAND_SLOT_Y + constants.SLOT_SIZE):
            self._handle_hand_slot_click(button, 'right')
            return True

        if constants.HOTBAR_Y <= mouse_y <= constants.HOTBAR_Y + constants.SLOT_SIZE:
            slot_index = (mouse_x - constants.HOTBAR_X) // constants.SLOT_SIZE
            if 0 <= slot_index < constants.HOTBAR_SLOTS:
                self._handle_slot_click(button, self.hotbar, slot_index,
                                        constants.HOTBAR_X + (slot_index * constants.SLOT_SIZE),
                                        constants.HOTBAR_Y)
                return True
        if show_inventory:
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

            # CRAFTING GRID
            if constants.CRAFTING_GRID_Y <= mouse_y <= constants.CRAFTING_GRID_Y + (
                constants.CRAFTING_GRID_SIZE * constants.SLOT_SIZE):
                row = (mouse_y - constants.CRAFTING_GRID_Y) // constants.SLOT_SIZE
                col = (mouse_x - constants.CRAFTING_GRID_X) // constants.SLOT_SIZE
                if (0 <= row < constants.CRAFTING_GRID_SIZE 
                    and 0 <= col < constants.CRAFTING_GRID_SIZE):
                    self._handle_crafting_grid_click(button, row, col)
                    return True

        # ESTE BLOQUE DEBE IR FUERA DE LOS IF ANTERIORES
        if (constants.CRAFTING_RESULT_SLOT_X <= mouse_x <= constants.CRAFTING_RESULT_SLOT_X + constants.SLOT_SIZE and
            constants.CRAFTING_RESULT_SLOT_Y <= mouse_y <= constants.CRAFTING_RESULT_SLOT_Y + constants.SLOT_SIZE):
            self._handle_crafting_result_click(button)
            return True

        if self.dragged_item and button == 1:
            self._return_dragged_item() 
        return False
    
    def _handle_slot_click(self, button, slot_list, index, slot_x, slot_y):  # 1 usage
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.dragged_item:
            # Soltar item
            if slot_list[index] is None:
                slot_list[index] = self.dragged_item
            else:
                # Intercambiar items
                slot_list[index], self.dragged_item = self.dragged_item, slot_list[index]
                return
            self.dragged_item = None
        elif slot_list[index]:
            self.dragged_item = slot_list[index]
            slot_list[index] = None
            item_rect = self.dragged_item.image.get_rect()
            item_rect.x = slot_x
            item_rect.y = slot_y
            self.dragged_item.drag_offset = (mouse_x - item_rect.centerx,
                                            mouse_y - item_rect.centery)
            
    def _handle_grid_slot_click(self, button, row, col, slot_x, slot_y):  # 1 usage
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos
        if button == 1:  # Click izquierdo
            if self.dragged_item:
                # Soltar item
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = self.dragged_item
                else:
                    self.inventory[row][col], self.dragged_item = self.dragged_item, self.inventory[row][col]
                    return  
                self.dragged_item = None
            elif self.inventory[row][col]:
                # Comenzar a arrastrar
                self.dragged_item = self.inventory[row][col]
                self.inventory[row][col] = None
                # Calcular offset para el arrastre centrado
                item_rect = self.dragged_item.image.get_rect()
                item_rect.x = slot_x
                item_rect.y = slot_y
                self.dragged_item.drag_offset = (mouse_x - item_rect.centerx,
                                                mouse_y - item_rect.centery)
    
    def _handle_hand_slot_click(self, button, hand):
            if button == 1:
                if hand == 'left':
                    if self.dragged_item:
                        self.left_hand, self.dragged_item = self.dragged_item, self.left_hand
                    else:
                        if self.left_hand:
                            self.dragged_item = self.left_hand
                            self.left_hand = None
                elif hand == 'right':
                    if self.dragged_item:
                        self.right_hand, self.dragged_item = self.dragged_item, self.right_hand
                    else:
                        if self.right_hand:
                            self.dragged_item = self.right_hand
                            self.right_hand = None
    
    def has_axe_equipped(self):
        return (
            (self.left_hand and self.left_hand.name == 'axe') or
            (self.right_hand and self.right_hand.name == 'axe')

        )
    def _return_dragged_item(self):  # 1 usage
    # Intentar devolver al hotbar primero
        for i, slot in enumerate(self.hotbar):
            if slot is None:
                self.hotbar[i] = self.dragged_item
                self.dragged_item = None
                return
            
        for row in range(constants.INVENTORY_ROWS):
            for col in range(constants.INVENTORY_COLS):
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = self.dragged_item
                    self.dragged_item = None
                    return
                
    def _draw_crafting_grid(self, screen):
        # Dibujar cuadrícula de crafteo
        for row in range(constants.CRAFTING_GRID_SIZE):
            for col in range(constants.CRAFTING_GRID_SIZE):
                x = constants.CRAFTING_GRID_X + (col * constants.SLOT_SIZE)
                y = constants.CRAFTING_GRID_Y + (row * constants.SLOT_SIZE)

                # Dibujar fondo del slot
                pygame.draw.rect(screen, constants.SLOT_BORDER,
                                (x, y, constants.SLOT_SIZE, constants.SLOT_SIZE))
                pygame.draw.rect(screen, constants.SLOT_COLOR,
                                (x + 2, y + 2, constants.SLOT_SIZE - 4, constants.SLOT_SIZE - 4))

                # Dibujar item si existe
                if self.crafting_grid[row][col]:
                    self._draw_item(screen, self.crafting_grid[row][col], x, y)

        pygame.draw.rect(screen, constants.SLOT_BORDER,
            (constants.CRAFTING_RESULT_SLOT_X, constants.CRAFTING_RESULT_SLOT_Y,
            constants.SLOT_SIZE, constants.SLOT_SIZE))
        pygame.draw.rect(screen, constants.SLOT_COLOR,
            (constants.CRAFTING_RESULT_SLOT_X + 2, constants.CRAFTING_RESULT_SLOT_Y + 2,
            constants.SLOT_SIZE - 4, constants.SLOT_SIZE - 4))
        
        if self.crafting_result:
            self._draw_item(screen, self.crafting_result,
                            constants.CRAFTING_RESULT_SLOT_X,
                            constants.CRAFTING_RESULT_SLOT_Y)

    def _handle_crafting_result_click(self, button):
        if button == 1 and self.crafting_result:
            self.add_item(self.crafting_result.name, self.crafting_result.quantity)
            # Consumir los materiales usados
            for row in range(constants.CRAFTING_GRID_ROWS):
                for col in range(constants.CRAFTING_GRID_COLS):
                    item = self.crafting_grid[row][col]
                    if item:
                        if item.quantity > 1:
                            item.quantity -= 1
                        else:
                            self.crafting_grid[row][col] = None
            self.crafting_result = None
            self.update_crafting_result()

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
                self.crafting_result = InventoryItem(recipe['result'],
                                                     self.item_images[recipe['result']])
                return
            
        self.crafting_result = None

    def clear_crafting_grid(self):
        for row in self.crafting_grid:
            for item in row:
                if item:
                    self.add_item(item.name, item.quantity)
        self.crafting_grid = [[None for _ in range(constants.CRAFTING_GRID_COLS)] for _ in range(constants.CRAFTING_GRID_ROWS)]
        self.update_crafting_result()

    def _handle_crafting_grid_click(self, button, row, col):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if button == 1:  # Click izquierdo
            if self.dragged_item:
                # Soltar item en la cuadrícula de crafteo
                if self.crafting_grid[row][col] is None:
                    self.crafting_grid[row][col] = self.dragged_item
                    self.dragged_item = None
                else:
                    # Intercambiar items
                    self.crafting_grid[row][col], self.dragged_item = self.dragged_item, self.crafting_grid[row][col]
                    return
            elif self.crafting_grid[row][col]:
                # Comenzar a arrastrar
                self.dragged_item = self.crafting_grid[row][col]
                self.crafting_grid[row][col] = None
                item_rect = self.dragged_item.image.get_rect()
                item_rect.x = constants.CRAFTING_GRID_X + (col * constants.SLOT_SIZE)
                item_rect.y = constants.CRAFTING_GRID_Y + (row * constants.SLOT_SIZE)
                self.dragged_item.drag_offset = (mouse_x - item_rect.centerx, mouse_y - item_rect.centery)
        # Actualiza el resultado de crafteo después de cada cambio
        self._check_recipe()

    def update_crafting_result(self):
        crafted_item = self.check_crafting()
        if crafted_item:
            # Si tu check_crafting devuelve solo el nombre, crea el objeto aquí:
            self.crafting_result = InventoryItem(
                crafted_item,
                self.item_images[crafted_item],
                1
            )
        else:
            self.crafting_result = None

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
                return recipe['result']
        return None