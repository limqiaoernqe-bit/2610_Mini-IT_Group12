import os
import pygame

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")


class DialogueBox:
    def __init__(self, dialogue):
        self.dialogue = dialogue
        self.index = 0
        self.finished = False
        self.just_pressed = False
        self.scene = None

        self.font = pygame.font.SysFont(None, 30)
        self.name_font = pygame.font.SysFont(None, 36, bold=True)

    def handle_event(self, event):
        if self.finished:
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.just_pressed = True

    def get_current(self):
        if self.index >= len(self.dialogue):
            return None
        return self.dialogue[self.index]

    def advance(self):
        self.index += 1
        if self.index >= len(self.dialogue):
            self.finished = True

    def draw(self, screen, portrait_rect=None):

        print("DRAWING INDEX =", self.index)

        if self.finished:
            return

        current = self.get_current()
        if not current:
            return

        speaker, image, text = current

        # ---------------- PORTRAIT (DRAW FIRST = behind UI) ----------------
        if image:
            try:
                path = os.path.join(ASSETS_DIR, image)
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (650, 650))

                # bottom-right position
                x = 1280 - 650
                y = 720 - 650

                screen.blit(img, (x, y))

            except:
                pass

        # ---------------- TEXTBOX (DRAW AFTER = on top of image) ----------------
        pygame.draw.rect(screen, (0, 0, 0), (40, 520, 1200, 160))
        pygame.draw.rect(screen, (255, 255, 255), (40, 520, 1200, 160), 2)

        screen.blit(self.name_font.render(str(speaker), True, (255, 220, 0)), (80, 540))
        screen.blit(self.font.render(str(text), True, (255, 255, 255)), (80, 590))

class DialogueScene:
    def __init__(self, dialogue_data):
        self.dialogue_box = DialogueBox(dialogue_data)

    def handle_events(self, events):
        for e in events:
            self.dialogue_box.handle_event(e)

    def update(self):
        db = self.dialogue_box

        if db.just_pressed:
            print("SPACE DETECTED")
            db.just_pressed = False
            db.advance()
            print("INDEX =", db.index)


        if db.finished:
            return

        # 1. handle input
        if db.just_pressed:
            db.just_pressed = False
            db.advance()

        # 2. get current AFTER possible advance
        current = db.get_current()

        print("CURRENT =", current)

        # 3. COMMAND SYSTEM
       
        while current and current[0] == "COMMAND":
            _, action, value = current

            if db.scene:

                if action == "set_bg":
                    db.scene.set_background(value)

                elif action == "move_path":
                    db.scene.start_path(value)

                    db.advance()
                    return

                elif action == "spawn_janitor":
                    db.scene.spawn_janitor(value)

            db.advance()
            current = db.get_current()

    def draw(self, screen):
        self.dialogue_box.draw(screen)

    def is_finished(self):
        return self.dialogue_box.finished