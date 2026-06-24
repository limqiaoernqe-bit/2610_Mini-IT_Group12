import pygame
import sys
from scenes.opening_scene import OpeningScene

class MenuScene:
    def __init__(self):
        self.next_scene = self

        self.WIDTH = 1280
        self.HEIGHT = 720

        self.main_menu = pygame.image.load("assets/main_menu.png")
        self.main_menu = pygame.transform.scale(
            self.main_menu, (self.WIDTH, self.HEIGHT)
        )

        self.controls_menu = pygame.image.load("assets/controls.png")
        self.controls_menu = pygame.transform.scale(
            self.controls_menu, (self.WIDTH, self.HEIGHT)
        )

        # False = main menu
        # True = controls screen
        self.show_controls = False

        self.start_button = pygame.Rect(870, 230, 360, 70)
        self.quit_button = pygame.Rect(870, 350, 360, 70)
        self.how_to_play_button = pygame.Rect(870, 470, 360, 70)

        # BACK button area on controls screen
        self.back_button = pygame.Rect(500, 580, 280, 90)

    def handle_events(self, events):
        for event in events:

            if event.type == pygame.QUIT:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                # CONTROLS SCREEN
                if self.show_controls:
                    if self.back_button.collidepoint(mouse_pos):
                        self.show_controls = False
                    return

                # MAIN MENU
                if self.start_button.collidepoint(mouse_pos):
                    self.next_scene = OpeningScene()
                    return

                if self.quit_button.collidepoint(mouse_pos):
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                    return

                if self.how_to_play_button.collidepoint(mouse_pos):
                    self.show_controls = True
                    return

    def update(self):
        pass

    def draw(self, screen):
        if self.show_controls:
            screen.blit(self.controls_menu, (0, 0))
        else:
            screen.blit(self.main_menu, (0, 0))

    def get_next_scene(self):
        return self.next_scene
