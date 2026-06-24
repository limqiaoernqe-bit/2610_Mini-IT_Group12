import pygame

from weapon import salt_line

SCALE_SIZE = (200, 200)

class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1.5
        self.state = "chasing"
        self.defeat = False


        # SINGLE SPRITES ONLY
        self.image_right = pygame.transform.scale(
            pygame.image.load("assets/ghost_right.png").convert_alpha(),
            SCALE_SIZE
        )

        self.image_left = pygame.transform.scale(
            pygame.image.load("assets/ghost_left.png").convert_alpha(),
            SCALE_SIZE
        )

        self.image = self.image_right

        self.stop_distance = 40


    def update(self, player_x, player_y):

        if self.defeat:
            return
        
        dx = player_x - self.x
        dy = player_y - self.y

        if abs(dx) < self.stop_distance and abs(dy) < self.stop_distance:
            return

        # smooth glide movement
        length = (dx**2 + dy**2) ** 0.5

        if length != 0:
            dx /= length
            dy /= length

            next_x = self.x + dx * self.speed
            next_y = self.y + dy * self.speed

        # face left/right only
        if dx > 0:
            self.image = self.image_right
        else:
            self.image = self.image_left

        # Check salt collision    
        future_rect = self.image.get_rect(midbottom=(next_x, next_y))
        for salt in salt_line:
            if future_rect.colliderect(salt["rect"]):
                return 

        # Move ghost   
        self.x = next_x
        self.y = next_y


    def draw(self, screen, camera_x = 0, camera_y = 0):
        rect = self.image.get_rect(
            center=(
                self.x - camera_x, 
                self.y - camera_y
            )
        )
        screen.blit(self.image, rect)

    def weapon_effect(self, effect):

        if effect == "MWfull":
            self.state = "defeat"
            self.defeat = True

        if effect == "Salt":
            self.state = "blocked"
