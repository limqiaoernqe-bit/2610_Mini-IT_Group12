import pygame

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Door Unlocking System")

class Door:
    def __init__(self, name, required_key):
        self.name = name
        self.required_key = required_key
        self.locked = True
    
    def unlock(self):
            self.locked = False

    # Show door usage
    def show_status(self):
        if self.locked:
            print(f"{self.name} is LOCKED.")
        else:
            print(f"{self.name} is unlocked.")
