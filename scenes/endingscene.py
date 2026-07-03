
from dialogues import ENDING_DIALOGUE
from dialoguescene import DialogueScene  # your main reusable system

class EndingScene:
    def __init__(self):
        self.scene = DialogueScene(ENDING_DIALOGUE)

    def update(self, events):
        self.scene.update(events)

    def draw(self, screen):
        self.scene.draw(screen)