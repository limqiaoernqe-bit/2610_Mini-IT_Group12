import pygame
import json

from weapon import salt_line

SCALE_SIZE = (200, 200)

class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1.5
        self.state = "chasing"
        self.defeat = False
        self.blocked_until = 0
        self.rect = pygame.Rect(0, 0, 100, 150)
        self.rect.center = (self.x, self.y)


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

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, player_x, player_y):

        if self.defeat:
            return
        
        #blocked by salt
        if self.state == "blocked":
            if pygame.time.get_ticks() > self.blocked_until:
                self.state = "chasing"
            else:
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
        future_rect = self.image.get_rect(center=(next_x, next_y))
        for salt in salt_line:
            if future_rect.colliderect(salt["rect"]):
                self.state = "blocked"
                self.blocked_until= pygame.time.get_ticks() + 40000
                return

        # Move ghost   
        self.x = next_x
        self.y = next_y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect.center = (self.x, self.y)

        # Update rect to new position
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen, camera_x = 0, camera_y = 0):
        # Use the existing self.rect, offset by camera
        draw_rect = self.rect.move(-camera_x, -camera_y)
        screen.blit(self.image, draw_rect)

    def weapon_effect(self, effect):
        if effect == "MWfull":
            self.state = "defeated"
            self.defeat = True

            # save ghost defeated
            try:
                with open("save_level1.json", "r") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}

            data["ghost_defeated"] = True

            with open("save_level1.json", "w") as f:
                json.dump(data, f, indent=4)

            self.popup_message = "Ghost Defeated!"
            self.popup_start_time = pygame.time.get_ticks()
            self.popup_duration = 3000

        elif effect == "Salt":
            self.state = "blocked"
            self.blocked_until = pygame.time.get_ticks() + 40000