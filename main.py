import pygame
import sys
import constants
from character import Character
from world import World

pygame.init()

# Initialize the game window
# Inicializa la ventana del juego
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("My Minecraft 2D")

#Set the background color
def main():
    clock = pygame.time.Clock()
    world = World(constants.WIDTH, constants.HEIGHT)
    character = Character(constants.WIDTH // 2, constants.HEIGHT // 2)
    show_inventory = False

    status_update_timer = 0 

    camera_x = 0
    camera_y = 0
    # Create a surface for the day/night overlay
    while True:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Close the game
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: # Handle mouse button events
                if event.button == 1:  
                    character.interact(world)
                    character.inventory.handle_click(pygame.mouse.get_pos(), event.button, show_inventory)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    character.inventory.handle_click(pygame.mouse.get_pos(), event.button, show_inventory)

            if event.type == pygame.KEYDOWN: # Handle keyboard events
                if event.key == pygame.K_e: # Toggle inventory visibility
                    show_inventory = not show_inventory
                if event.key == pygame.K_f: 
                    character.update_food(20) #Update food(In the future, this will be replaced by a food item)
                if event.key == pygame.K_t: 
                    character.update_thirst(20) #Update thirst(In the future, this will be replaced by a water item)

        
        #Control the character movement
        #Controles de movimiento
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx=-5
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx=5
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy=-5
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy=5

        character.is_running = keys[pygame.K_LSHIFT] and character.stamina > 0
        character.move(dx, dy, world)
        
        camera_x = character.x - constants.WIDTH // 2
        camera_y = character.y - constants.HEIGHT // 2

        world.update_chunks(character.x, character.y)

        # Update the world time
        #Actualiza el tiempo del mundo
        world.update_time(dt)

        status_update_timer += dt
        if status_update_timer >= constants.STATUS_UPDATE_INTERVAL:
            character.update_energy(-0.005)
            character.update_food(-0.1) 
            character.update_thirst(-0.3)   
            status_update_timer = 0 

        #If the character's energy, food, or thirst reaches zero, end the game
        #Si la energia, comida o sed llegan a cero, el juego termina
        if character.energy <= 0 or character.food <= 0 or character.thirst <= 0:
            print("Game over!")
            pygame.quit()
            sys.exit()
        
        screen.fill((0, 0, 0))

        world.draw(screen, camera_x, camera_y)
        character.draw(screen, camera_x, camera_y)
        if show_inventory:
            character.draw_inventory(screen)

        character.draw_inventory(screen, show_inventory)
        #Draw the status bars for energy, food, and thirst
        #Dibuja las barras de estado para energia, comida y sed

        font = pygame.font.Font(None, 24)
        energy_text = font.render(f"Energy: {int(character.energy)}", True, constants.WHITE)
        food_text = font.render(f"Food: {int(character.food)}", True, constants.WHITE)
        thirst_text = font.render(f"Thirst: {int(character.thirst)}", True, constants.WHITE)
        stamina_text = font.render(f"Stamina: {int(character.stamina)}", True, constants.WHITE)
        time_of_day = (world.current_time / constants.DAY_LENGTH) * 24
        time_text = font.render(f"Time: {int(time_of_day):02d}:00", True, constants.WHITE)

        # Draw the status bars
        #Dibuja ls barras de estado
        screen.blit(energy_text, (10, constants.HEIGHT - 115))
        screen.blit(food_text, (10, constants.HEIGHT - 90))
        screen.blit(thirst_text, (10, constants.HEIGHT - 65))
        screen.blit(stamina_text, (10, constants.HEIGHT - 40))
        screen.blit(time_text, (10, constants.HEIGHT - 15))
        

        pygame.display.flip()

# Define the Surface class to handle the day/night overlay
class Surface:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.day_overlay = pygame.Surface((width, height))

if __name__ == '__main__':
    main()


