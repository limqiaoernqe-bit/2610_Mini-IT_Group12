import pygame

SCALE_SIZE = (150, 150)

class Janitor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1

        self.frame = 0
        self.anim_speed = 0.12

        # IDLE
        self.idle_front = pygame.transform.scale(
            pygame.image.load("assets/janitor.png").convert_alpha(),
            SCALE_SIZE
        )

        self.idle_back = pygame.transform.scale(
            pygame.image.load("assets/janitor_back.png").convert_alpha(),
            SCALE_SIZE
        )

        # SPRITE SHEETS
        self.left_sheet = pygame.image.load("assets/janitor_walk_left.png").convert_alpha()
        self.right_sheet = pygame.image.load("assets/janitor_walk_right.png").convert_alpha()
        self.front_sheet = pygame.image.load("assets/janitor_walk_front.png").convert_alpha()
        self.back_sheet = pygame.image.load("assets/janitor_walk_back.png").convert_alpha()

        # ✅ FIXED SIZES
        # left/right = 2x2 (4 frames total)
        self.walk_left = self.load_sheet(self.left_sheet, 2, 2)
        self.walk_right = self.load_sheet(self.right_sheet, 2, 2)

        # front/back = 2 sprites = 2x1
        self.walk_front = self.load_sheet(self.front_sheet, 2, 1)
        self.walk_back = self.load_sheet(self.back_sheet, 2, 1)

        self.image = self.idle_front
        self.direction = "front"
        self.current_frames = self.walk_front

        self.stop_distance = 40

  
    def load_sheet(self, sheet, rows, cols):
        frames = []

        w = sheet.get_width() // cols
        h = sheet.get_height() // rows

        for row in range(rows):
            for col in range(cols):
                frame = sheet.subsurface((col*w, row*h, w, h)).copy()
                frame = pygame.transform.scale(frame, SCALE_SIZE)
                frames.append(frame)

        return frames


    def animate(self):
        self.frame += self.anim_speed
        if self.frame >= len(self.current_frames):
            self.frame = 0
        return self.current_frames[int(self.frame)]


    def set_frames(self, new_frames):
        if self.current_frames != new_frames:
            self.current_frames = new_frames
            self.frame = 0  

    def update(self, player_x, player_y):

        dx = player_x - self.x
        dy = player_y - self.y

        # stop distance check (unchanged)
        if abs(dx) < self.stop_distance and abs(dy) < self.stop_distance:
            if self.direction == "back":
                self.image = self.idle_back
            else:
                self.image = self.idle_front
            return

        # movement + animation logic (FIXED DIAGONAL ISSUE)

        # PRIORITY: vertical movement controls animation (prevents sprite flicker)
        if dy < 0:
            # moving up (including diagonals)
            self.y -= self.speed
            self.direction = "back"
            self.set_frames(self.walk_back)

        elif dy > 0:
            # moving down (including diagonals)
            self.y += self.speed
            self.direction = "front"
            self.set_frames(self.walk_front)

        else:
            # only horizontal movement if no vertical movement
            if dx > 0:
                self.x += self.speed
                self.direction = "right"
                self.set_frames(self.walk_right)

            elif dx < 0:
                self.x -= self.speed
                self.direction = "left"
                self.set_frames(self.walk_left)

        # apply animation frame
        self.image = self.animate()


 
    def draw(self, screen):
        rect = self.image.get_rect(midbottom=(self.x, self.y))
        screen.blit(self.image, rect)