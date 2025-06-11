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

    while True:
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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            character.move(dx=-5, dy=0, world=world)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            character.move(dx=5, dy=0, world=world)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            character.move(dx=0, dy=-5, world=world)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            character.move(dx=0, dy=5, world=world)

        world.draw(screen)
        character.draw(screen)
        if show_inventory:
            character.draw_inventory(screen)
        else:
            world.draw_inventory(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()


