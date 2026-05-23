import pygame

SCALE_SIZE = (200, 200)

class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1.5

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

        dx = player_x - self.x
        dy = player_y - self.y

        if abs(dx) < self.stop_distance and abs(dy) < self.stop_distance:
            return

        # smooth glide movement
        length = (dx**2 + dy**2) ** 0.5

        if length != 0:
            dx /= length
            dy /= length

            self.x += dx * self.speed
            self.y += dy * self.speed

        # face left/right only
        if dx > 0:
            self.image = self.image_right
        else:
            self.image = self.image_left


    def draw(self, screen):
        rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, rect)
