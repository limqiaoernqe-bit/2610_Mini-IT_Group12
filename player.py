import pygame
from weapon import Weapons

SCALE_SIZE = (120, 120)
class Player:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.speed = 4


        self.idle_front = pygame.transform.scale(
            pygame.image.load("assets/mia.png").convert_alpha(),
            SCALE_SIZE
        )

        self.idle_back = pygame.transform.scale(
            pygame.image.load("assets/mia_back.png").convert_alpha(),
            SCALE_SIZE
        )


        self.sheet_front = pygame.image.load("assets/mia_walk_front.png").convert_alpha()
        self.sheet_back = pygame.image.load("assets/mia_walk_back.png").convert_alpha()
        self.sheet_left = pygame.image.load("assets/mia_walk_left.png").convert_alpha()
        self.sheet_right = pygame.image.load("assets/mia_walk_right.png").convert_alpha()


        self.frame = 0
        self.anim_speed = 0.2


        self.walk_front = self.load_sheet(self.sheet_front, rows=2, cols=1)
        self.walk_back  = self.load_sheet(self.sheet_back, rows=2, cols=1)


        self.walk_left = self.load_sheet(self.sheet_left, rows=3, cols=2)
        self.walk_right = self.load_sheet(self.sheet_right, rows=3, cols=2)

        self.image = self.idle_front
        self.direction = "front"
        self.hold_weapon = None
        self.held_weapon = None

    def load_sheet(self, sheet, rows, cols):
        frames = []

        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()

        frame_w = sheet_width // cols
        frame_h = sheet_height // rows

        for row in range(rows):
            for col in range(cols):
                frame = sheet.subsurface(
                    (col * frame_w,
                    row * frame_h,
                    frame_w,
                    frame_h)
                ).copy()

                frame = pygame.transform.scale(frame, SCALE_SIZE)
                frames.append(frame)

        return frames


    def animate(self, frames):
        self.frame += self.anim_speed
        if self.frame >= len(frames):
            self.frame = 0
        return frames[int(self.frame)]

    def update(self, keys, walls):
            moving = False

            dx = 0
            dy = 0


            if keys[pygame.K_RIGHT]:
                dx = self.speed
                self.image = self.animate(self.walk_right)
                self.direction = "right"
                moving = True


            elif keys[pygame.K_LEFT]:
                dx = -self.speed
                self.image = self.animate(self.walk_left)
                self.direction = "left"
                moving = True


            elif keys[pygame.K_DOWN]:
                dy = self.speed
                self.image = self.animate(self.walk_front)
                self.direction = "front"
                moving = True


            elif keys[pygame.K_UP]:
                dy = -self.speed
                self.image = self.animate(self.walk_back)
                self.direction = "back"
                moving = True

            # Collision Rect
            player_rect = pygame.Rect(
                 self.x - 20,
                 self.y - 40,
                    40,
                    40
            )

            # Horizontal collision 
            player_rect.x += dx

            for wall in walls:
                if player_rect.colliderect(wall):
                     dx = 0
                     break

            # Vertical collision
            player_rect.y += dy

            for wall in walls:
                if player_rect.colliderect(wall):
                    dy = 0
                    break

            # Apply movement after collision checks
            self.x += dx
            self.y += dy

            if not moving:
                 self.frame = 0
                 if self.direction == "front":
                    self.image = self.idle_front
                 elif self.direction == "back":
                    self.image = self.idle_back

#later delete after all enemy movement finish
    def draw(self, screen, camera_x=0, camera_y=0):
        rect = self.image.get_rect(midbottom=(self.x - camera_x, self.y - camera_y))
        screen.blit(self.image, rect)

        # if player holds weapon 
        if self.hold_weapon is not None and self.hold_weapon in Weapons:
             weapon_img = Weapons [self.hold_weapon]["image"]
        if self.held_weapon is not None and self.held_weapon in Weapons:
             weapon_img = Weapons [self.held_weapon]["image"]

             # flip 
             if self.direction == "left": 
                  weapon_img = pygame.transform.flip(weapon_img, True, False)
                  offset_x = rect.x + 20
                  offset_y = rect.y +40
             elif self.direction == "right":
                  offset_x = rect.x +40
                  offset_y = rect.y +60

             else:
              offset_x = rect.x + 50
              offset_y = rect.y + 30

             screen.blit(weapon_img, (offset_x, offset_y))