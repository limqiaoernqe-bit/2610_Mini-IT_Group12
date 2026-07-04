import os
import pygame

from scenes.base_scene import BaseScene
from scenes.dialogue_scene import DialogueScene
from dialogues import ENDING_DIALOGUE


class EndingScene(BaseScene):
    def __init__(self):
        super().__init__()

        base_path = os.path.dirname(__file__)

        self.background = pygame.image.load(
            os.path.join(base_path, "..", "assets", "hotelentrance.png")
        ).convert()

        self.background = pygame.transform.scale(self.background, (1280, 720))

        self.dialogue = DialogueScene(ENDING_DIALOGUE)
        self.dialogue.dialogue_box.scene = self

    def set_background(self, name):
        pass

    def handle_events(self, events):
        self.dialogue.handle_events(events)

    def update(self):
        self.dialogue.update()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.dialogue.draw(screen)
    