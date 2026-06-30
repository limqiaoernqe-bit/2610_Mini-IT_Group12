import pygame
from weapon import active_traps

SCALE_SIZE = (140, 140)
from weapon import active_traps

class Receptionist:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1.5
        self.state = "chasing"
        self.defeat = False
        self.stun_timer = 0
        self.slip_unti = 0 

        self.frame = 0
        self.anim_speed = 0.12

        # IDLE
        self.idle_front = pygame.transform.scale(
            pygame.image.load("assets/receptionist.png").convert_alpha(),
            SCALE_SIZE
        )

        self.idle_back = pygame.transform.scale(
            pygame.image.load("assets/receptionist_back.png").convert_alpha(),
            SCALE_SIZE
        )

        # SPRITE SHEETS
        self.left_sheet = pygame.image.load("assets/receptionist_walk_left.png").convert_alpha()
        self.right_sheet = pygame.image.load("assets/receptionist_walk_right.png").convert_alpha()
        self.front_sheet = pygame.image.load("assets/receptionist_walk_front.png").convert_alpha()
        self.back_sheet = pygame.image.load("assets/receptionist_walk_back.png").convert_alpha()

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

    def update(self, player_x, player_y, walls):

        if self.defeat:
            return

        if self.state == "stunned":
            if pygame.time.get_ticks() - self.stun_timer > 10000: 
                self.state = "chasing"
            else:
                return

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

        # Receptionist collision hitbox
        receptionist_rect = pygame.Rect(
            self.x - 20,
            self.y - 40,
            40,
            40
        )

        # stop near player
        if abs(dx) < self.stop_distance and abs(dy) < self.stop_distance:
            if self.direction == "back":
                self.image = self.idle_back
            else:
                self.image = self.idle_front
            return

        # EXACT SAME STYLE AS YOUR JANITOR (no diagonal movement)

        # Movement values used for collision checking
        move_x = 0
        move_y = 0

        # Receptionist chases player
        # Prioritises vertical movement before horizontal movement
        if dy < 0:
            move_y = -self.speed
            self.direction = "back"
            self.set_frames(self.walk_back)

        elif dy > 0:
            move_y = self.speed
            self.direction = "front"
            self.set_frames(self.walk_front)

        else:
            if dx > 0:
                move_x = self.speed
                self.direction = "right"
                self.set_frames(self.walk_right)

            elif dx < 0:
                move_x = -self.speed
                self.direction = "left"
                self.set_frames(self.walk_left)

        # Horizontal wall collision
        test_rect = receptionist_rect.copy()
        test_rect.x += move_x
        
        blocked = False
        
        for wall in walls:
            if test_rect.colliderect(wall):
                blocked = True
                break

        # Move receptionist only if path not blocked
        if not blocked:
            self.x += move_x

        # Vertical wall collision 
        test_rect = receptionist_rect.copy()
        test_rect.y += move_y

        blocked = False

        for wall in walls:
            if test_rect.colliderect(wall):
                blocked = True
                break

        # Move receptionist only if path not blocked
        if not blocked:
            self.y += move_y
                
        self.image = self.animate()

        # check for trap collisions
        for trap in active_traps[:]:
            if self.image.get_rect(center=(self.x, self.y)).colliderect(trap["rect"]):
                self.weapon_effect("BananaPeel")
                active_traps.remove(trap)

 
    def draw(self, screen, camera_x = 0, camera_y = 0):
        rect = self.image.get_rect(
            midbottom=(
                self.x - camera_x, 
                self.y - camera_y
            )
        )
        screen.blit(self.image, rect)

    def weapon_effect(self, effect):
        if effect == "BananaPeel":
            self.speed = max(1,self.speed -1)

        elif effect == "CleaningSpray":
            self.state = "stunned" 
            self.stun_timer = pygame.time.get_ticks()
            self.original_speed = self.speed 
            self.speed = max(0.5, self.speed - 0.5)

        elif effect == "KitchenKnife":
            self.state = "defeated" 
            self.defeat = True
