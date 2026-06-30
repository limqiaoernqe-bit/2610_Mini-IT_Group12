import pygame
import sys
import subprocess

from scenes.menu_scene import MenuScene
from scenes.scene_manager import SceneManager
from scenes.hotelscene1 import HotelScene1

pygame.init()

# screen setup
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Escape Code")

clock = pygame.time.Clock()

# START GAME
scene_manager = SceneManager(MenuScene())

run = True

while run:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            run = False

    # scene system
    scene_manager.handle_events(events)
    scene_manager.update()
    # If HotelScene1 finished, quit and launch level 2
    if isinstance(scene_manager.current_scene, HotelScene1) and getattr(scene_manager.current_scene, "finished", False):
        pygame.quit()
        subprocess.run(["python", "level2_map.py"])
        break 
    
    scene_manager.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()