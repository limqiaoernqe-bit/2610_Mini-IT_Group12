import pygame
from pygame.locals import *

pygame.init()

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hotel')

run = True
while run :

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()