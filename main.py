import pygame
import sys
import constants
from character import Character
from world import World

pygame.init()

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("My Minecraft 2D")

def main():
    clock = pygame.time.Clock()
    world = World(constants.WIDTH, constants.HEIGHT)
    character = Character(constants.WIDTH // 2, constants.HEIGHT // 2)
    show_inventory = False

    status_update_timer = 0 

    while True:
        dt = clock.tick(60)  # Controla la velocidad del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del ratón
                    character.interact(world)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    show_inventory = not show_inventory
                if event.key == pygame.K_f: 
                    character.update_food(20) #Update food(In the future, this will be replaced by a food item)
                if event.key == pygame.K_t: 
                    character.update_thirst(20) #Update thirst(In the future, this will be replaced by a water item)


        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            character.move(dx=-5, dy=0, world=world)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            character.move(dx=5, dy=0, world=world)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            character.move(dx=0, dy=-5, world=world)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            character.move(dx=0, dy=5, world=world)

        # Update the world time
        world.update_time(dt)

        status_update_timer += dt
        if status_update_timer >= constants.STATUS_UPDATE_INTERVAL:
            character.update_energy(-0.1)
            character.update_food(-0.05) 
            character.update_thirst(-0.1)   
            status_update_timer = 0

        if character.energy <= 0 or character.food <= 0 or character.thirst <= 0:
            print("Game over!")
            pygame.quit()
            sys.exit()
        
        world.draw(screen)
        character.draw(screen)
        if show_inventory:
            character.draw_inventory(screen)

        font = pygame.font.Font(None, 24)
        energy_text = font.render(f"Energy: {int(character.energy)}", True, constants.WHITE)
        food_text = font.render(f"Food: {int(character.food)}", True, constants.WHITE)
        thirst_text = font.render(f"Thirst: {int(character.thirst)}", True, constants.WHITE)
        time_of_day = (world.current_time / constants.DAY_LENGTH) * 24
        time_text = font.render(f"Time: {int(time_of_day):02d}:00", True, constants.WHITE)

        screen.blit(energy_text, (10, constants.HEIGHT - 90))
        screen.blit(food_text, (10, constants.HEIGHT - 65))
        screen.blit(thirst_text, (10, constants.HEIGHT - 40))
        screen.blit(time_text, (10, constants.HEIGHT - 15))

        pygame.display.flip()

class Surface:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.day_overlay = pygame.Surface((width, height))

if __name__ == '__main__':
    main()


