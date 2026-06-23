import os
import pygame
from scenes.base_scene import BaseScene
from scenes.dialogue_scene import DialogueScene
from dialogues import OPENING_DIALOGUE
from scenes.hotelscene1 import HotelScene1


class OpeningScene(BaseScene):
    def __init__(self):
        super().__init__()

        base_path = os.path.dirname(__file__)

        self.bg_images = {
            "hotelentrance": pygame.image.load(os.path.join(base_path, "..", "assets", "hotelentrance.png")).convert(),
            "hotelopening": pygame.image.load(os.path.join(base_path, "..", "assets", "hotelopening.png")).convert(),
            "hotelrooms": pygame.image.load(os.path.join(base_path, "..", "assets", "hotelrooms.png")).convert(),
            "miaroom": pygame.image.load(os.path.join(base_path, "..", "assets", "miaroom.png")).convert(),
        }

        for k in self.bg_images:
            self.bg_images[k] = pygame.transform.scale(self.bg_images[k], (1280, 720))

        self.background = self.bg_images["hotelentrance"]

        self.dialogue = DialogueScene(OPENING_DIALOGUE)
        self.dialogue.dialogue_box.scene = self

    def set_background(self, name):
        if name in self.bg_images:
            self.background = self.bg_images[name]

    def handle_events(self, events):
        self.dialogue.handle_events(events)

    def update(self):
        self.dialogue.update()

        if self.dialogue.is_finished():
            self.switch_to(HotelScene1())

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.dialogue.draw(screen)