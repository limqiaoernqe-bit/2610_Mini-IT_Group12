import pygame
import sys

from scenes.endingscene import EndingScene

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Ending")

clock = pygame.time.Clock()

ending = EndingScene()

running = True

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    ending.handle_events(events)
    ending.update()
    ending.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()