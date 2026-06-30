import pygame

SCALE_SIZE = (150, 150)
from weapon import active_traps

class Janitor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1.5
        self.image = pygame.image.load("assets/janitor.png").convert_alpha()
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.state = "chasing"
        self.defeat = False
        self.stun_timer = 0
        self.slip_until = 0

        self.frame = 0
        self.anim_speed = 0.12
        self.rect.center = (self.x, self.y)

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

       
        self.walk_left = self.load_sheet(self.left_sheet, 2, 2)
        self.walk_right = self.load_sheet(self.right_sheet, 2, 2)

        # front/back = 2 sprites = 2x1
        self.walk_front = self.load_sheet(self.front_sheet, 2, 1)
        self.walk_back = self.load_sheet(self.back_sheet, 2, 1)

        self.image = self.idle_front
        self.direction = "front"
        self.current_frames = self.walk_front

        self.stop_distance = 40

        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

  
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

    def update(self, player_x, player_y, walls):
        
        # if defeats the janitor js stops moving
        if self.defeat:
            return 
         # stops the janitor for 10 seconds
        if self.state == "stunned":
            if pygame.time.get_ticks() - self.stun_timer > 10000: 
                self.state = "chasing"
            else:
                return
            
        # if janitor is slipping
        if self.state == "slipping":
            now = pygame.time.get_ticks()
            
            if now < self.slip_until:
               self.slip_angle = (self.slip_angle + 10) % 360
               self.image = pygame.transform.rotate(self.idle_front, self.slip_angle)
               self.x -= 2
               self.y -= 1 
               self.rect.center = (self.x, self.y)

            else:
               self.image = pygame.transform.rotate(self.idle_front, 90)
            if now > self.lay_until:
                self.state = "chasing"
            return
        
        if self.state == "slowed":
            if pygame.time.get_ticks() - self.stun_timer > 5000:
                self.speed = self.original_speed
                self.state = "chasing"

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

        move_x = 0
        move_y = 0

        if dy < 0:
            self.direction = "back"
            self.set_frames(self.walk_back)
        elif dy > 0:
            self.direction = "front"
            self.set_frames(self.walk_front)
        elif dx > 0:
            self.direction = "right"
            self.set_frames(self.walk_right)
        elif dx < 0:
            self.direction = "left"
            self.set_frames(self.walk_left)

        if dx < 0:
            move_x = -self.speed
        elif dx > 0:
            move_x = self.speed

        if dy < 0:
            move_y = -self.speed
        elif dy > 0:
            move_y = self.speed

        janitor_rect = self.rect.copy()

        if move_x != 0:
            janitor_rect.x += move_x
            blocked = any(janitor_rect.colliderect(wall) for wall in walls)
            if not blocked:
                self.x += move_x

        janitor_rect = self.rect.copy()

        if move_y != 0:
            janitor_rect.y += move_y
            blocked = any(janitor_rect.colliderect(wall) for wall in walls)
            if not blocked:
                self.y += move_y

        # apply animation frame
        self.image = self.animate()
        self.rect.center = (self.x, self.y)

       # check for trap collisions
        for trap in active_traps[:]:
            if self.state == "chasing" and self.rect.colliderect(trap["rect"]):
                self.weapon_effect("BananaPeel")
                active_traps.remove(trap)

    def draw(self, screen, camera_x=0, camera_y=0):

        rect = self.image.get_rect(
            midbottom=(
                self.x - camera_x,
                self.y - camera_y
            )
        )

        screen.blit(self.image, rect)

    def weapon_effect (self, effect):
        if effect== "BananaPeel":
            self.state = "slipping"
            self.slip_until = pygame.time.get_ticks() + 2000
            self.lay_until = pygame.time.get_ticks() + 40000
            self.slip_angle = 0

        elif effect == "CleaningSpray":
            self.state = "slowed" 
            self.stun_timer = pygame.time.get_ticks()
            self.original_speed = self.speed
            self.speed = max(0.5, self.speed - 0.5 ) #speed reduced by 0.5

        elif effect == "BaseballBat":
            self.state = "defeated"
            self.defeat = True
