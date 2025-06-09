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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del ratón
                    character.interact(world)
                # Si quieres usar el botón derecho, descomenta la siguiente línea:
                # if event.button == 3:
                #     pass

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character.move(dx=-5, dy=0, world=world)
        if keys[pygame.K_RIGHT]:
            character.move(dx=5, dy=0, world=world)
        if keys[pygame.K_UP]:
            character.move(dx=0, dy=-5, world=world)
        if keys[pygame.K_DOWN]:
            character.move(dx=0, dy=5, world=world)

        world.draw(screen)
        character.draw(screen)
        world.draw_inventory(screen, character)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
