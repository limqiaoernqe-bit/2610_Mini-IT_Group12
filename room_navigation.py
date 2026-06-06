import pygame

class RoomTrigger:
    def __init__(self, rect, message, locked=False):
        self.rect = rect
        self.message = message
        self.locked = locked

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)