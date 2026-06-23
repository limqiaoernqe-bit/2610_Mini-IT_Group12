import os
import pygame

SCALE_SIZE = (120, 120)

class Player:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.speed = 4

        self.control_enabled = True
        self.target_x = None
        self.target_y = None

        # asset path handling
        base_path = os.path.dirname(__file__)
        assets_path = os.path.join(base_path, "assets")


        # idle sprites
        self.idle_front = pygame.transform.scale(
            pygame.image.load(os.path.join(assets_path, "mia.png")).convert_alpha(),
            SCALE_SIZE
        )
        self.idle_back = pygame.transform.scale(
            pygame.image.load(os.path.join(assets_path, "mia_back.png")).convert_alpha(),
            SCALE_SIZE
        )

        # animation sheets
        self.sheet_front = pygame.image.load(os.path.join(assets_path, "mia_walk_front.png")).convert_alpha()
        self.sheet_back = pygame.image.load(os.path.join(assets_path, "mia_walk_back.png")).convert_alpha()
        self.sheet_left = pygame.image.load(os.path.join(assets_path, "mia_walk_left.png")).convert_alpha()
        self.sheet_right = pygame.image.load(os.path.join(assets_path, "mia_walk_right.png")).convert_alpha()

        self.frame = 0
        self.anim_speed = 0.2

        # split sheets into frames
        self.walk_front = self.load_sheet(self.sheet_front, rows=2, cols=1)
        self.walk_back  = self.load_sheet(self.sheet_back, rows=2, cols=1)
        self.walk_left  = self.load_sheet(self.sheet_left, rows=3, cols=2)
        self.walk_right = self.load_sheet(self.sheet_right, rows=3, cols=2)

        self.image = self.idle_front
        self.direction = "front"

        # collision rect
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def load_sheet(self, sheet, rows, cols):
        frames = []
        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()
        frame_w = sheet_width // cols
        frame_h = sheet_height // rows

        for row in range(rows):
            for col in range(cols):
                frame = sheet.subsurface(
                    (col * frame_w, row * frame_h, frame_w, frame_h)
                ).copy()
                frame = pygame.transform.scale(frame, SCALE_SIZE)
                frames.append(frame)
        return frames

    def animate(self, frames):
        self.frame += self.anim_speed
        if self.frame >= len(frames):
            self.frame = 0
        return frames[int(self.frame)]

    def move_to(self, x, y):
        self.target_x = x
        self.target_y = y
        self.control_enabled = False

    def update(self, keys, walls=None):

        # ---------------- AUTO MOVE MODE ----------------
        if not self.control_enabled and self.target_x is not None:

            dx = self.target_x - self.x
            dy = self.target_y - self.y

            if abs(dx) < 3 and abs(dy) < 3:
                self.x = self.target_x
                self.y = self.target_y
                self.control_enabled = True
                self.target_x = None
                self.target_y = None
                return

            if abs(dx) > abs(dy):
                self.x += self.speed if dx > 0 else -self.speed
            else:
                self.y += self.speed if dy > 0 else -self.speed

            self.rect.midbottom = (self.x, self.y)
            return

        # ---------------- MANUAL CONTROL ----------------
        dx = dy = 0

        if keys[pygame.K_RIGHT]:
            dx = self.speed
            self.image = self.animate(self.walk_right)

        elif keys[pygame.K_LEFT]:
            dx = -self.speed
            self.image = self.animate(self.walk_left)

        elif keys[pygame.K_DOWN]:
            dy = self.speed
            self.image = self.animate(self.walk_front)

        elif keys[pygame.K_UP]:
            dy = -self.speed
            self.image = self.animate(self.walk_back)

        self.x += dx
        self.y += dy
        self.rect.midbottom = (self.x, self.y)

    def draw(self, screen, camera_x=0, camera_y=0):
        rect = self.image.get_rect(
            midbottom=(self.x - camera_x, self.y - camera_y)
        )
        screen.blit(self.image, rect)
