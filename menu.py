import pygame

from player import Player
from janitor import Janitor
from receptionist import Receptionist
from ghost import Ghost


import sys

pygame.init()


WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape Mode")

clock = pygame.time.Clock()


main_menu = pygame.image.load("assets/main_menu.png")
game_over = pygame.image.load("assets/game_over.png")

main_menu = pygame.transform.scale(main_menu, (WIDTH, HEIGHT))
game_over = pygame.transform.scale(game_over, (WIDTH, HEIGHT))


game_state = "menu"


start_button = pygame.Rect(870, 230, 360, 70)
quit_button = pygame.Rect(870, 350, 360, 70)

retry_button = pygame.Rect(500, 500, 250, 80)
gameover_quit_button = pygame.Rect(500, 600, 250, 80)


player = Player()
janitor = Janitor(700, 300)
# TEMP TEST SPAWNS (REMOVE LATER)

ghost = Ghost(500, 300)
receptionist = Receptionist(800, 300)
player_speed = 5


def reset_game():
    player.x = 100
    player.y = 300


running = True

while running:

    mouse_pos = pygame.mouse.get_pos()


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            
            if game_state == "menu":

                if start_button.collidepoint(mouse_pos):
                    game_state = "play"

                if quit_button.collidepoint(mouse_pos):
                    running = False

            
            elif game_state == "gameover":

                if retry_button.collidepoint(mouse_pos):
                    reset_game()
                    game_state = "play"

                if gameover_quit_button.collidepoint(mouse_pos):
                    running = False


    if game_state == "menu":
        screen.blit(main_menu, (0, 0))

  
    elif game_state == "play":
        screen.fill((30, 30, 30))

        keys = pygame.key.get_pressed()

        player.update(keys)

        janitor.update(player.x, player.y)
        ghost.update(player.x, player.y)
        receptionist.update(player.x, player.y)

        # DEPTH SORTING
        sprites = [player, janitor, ghost, receptionist]

        sprites.sort(key=lambda sprite: sprite.y)

        for sprite in sprites:
            sprite.draw(screen)

        if keys[pygame.K_k]:
            game_state = "gameover"

  
    elif game_state == "gameover":
        screen.blit(game_over, (0, 0))

        # optional debug buttons
        pygame.draw.rect(screen, (255, 0, 0), retry_button, 2)
        pygame.draw.rect(screen, (0, 0, 255), gameover_quit_button, 2)

  
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()

