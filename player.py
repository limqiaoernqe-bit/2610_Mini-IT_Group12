import pygame
SCALE_SIZE = (48, 48)
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

    
    def update(self, keys):
        moving = False

     
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.image = self.animate(self.walk_right)
            self.direction = "right"
            moving = True

      
        elif keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.image = self.animate(self.walk_left)
            self.direction = "left"
            moving = True

       
        elif keys[pygame.K_DOWN]:
            self.y += self.speed
            self.image = self.animate(self.walk_front)
            self.direction = "front"
            moving = True

        
        elif keys[pygame.K_UP]:
            self.y -= self.speed
            self.image = self.animate(self.walk_back)
            self.direction = "back"
            moving = True

       
        if not moving:
            self.frame = 0
            if self.direction == "front":
                self.image = self.idle_front
            elif self.direction == "back":
                self.image = self.idle_back

    
    def draw(self, screen):
        rect = self.image.get_rect(midbottom=(self.x, self.y))
        screen.blit(self.image, rect)