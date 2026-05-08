import pygame
from pygame.locals import *

pygame.init ()
screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hotel')
font = pygame.font.Font(None,30)

#TESTING PURPOSES
player_rect = pygame.Rect(100, 100, 50,50)
player_speed = 7

#Clue1 
clue1= pygame.Rect(300, 300, 50, 50) #just a placeholder cause im not sure of the exact position
clue1_active = True
show_prompt= False
show_popup = False

#Clue2
clue2 = pygame.Rect(500, 500, 50, 50) #just a placeholder cause im not sure of the exact position
clue2_active = True
show_prompt2 = False
show_popup2 = False

clock = pygame.time.Clock()
run = True
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

        #TEST PLAYER MOVEMENT
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                player_rect.x -= player_speed
            elif event.key == K_RIGHT:
                player_rect.x += player_speed
            elif event.key == K_UP:
                player_rect.y -= player_speed
            elif event.key == K_DOWN:
                player_rect.y += player_speed

        # Player has to press R to open popup
        if event.type == KEYDOWN:
            if event.key == K_r and show_prompt and clue1_active:
                show_popup = True
                clue1_active = False

            if event.key == K_r and show_prompt2 and clue2_active:
                show_popup2 = True
                clue2_active = False

            elif event.key == K_c and show_popup: # Press C to close popup 
                show_popup = False

            elif event.key == K_c and show_popup2: # Press C to close popup
                show_popup2 = False


    # Check if player is in clue1 area
    if clue1_active and player_rect.colliderect(clue1):
        show_prompt = True
    else:
        show_prompt = False

    # Check if player is in clue2 area
    if clue2_active and player_rect.colliderect(clue2):
        show_prompt2 = True
    else:        
        show_prompt2 = False

    #TEST 
    screen.fill((200, 200, 200))
    pygame.draw.rect(screen, (0, 0, 255), player_rect) #player
    pygame.draw.rect(screen, (255, 0, 0), clue1) 
    pygame.draw.rect(screen, (0, 255, 0), clue2)
    
    # Display prompt to press R
    if show_prompt:
        prompt_text = font.render("Press R", True, (0,0,0))
        screen.blit(prompt_text, (clue1.x, clue1.y - 30))

    if show_prompt2:
        prompt_text2 = font.render("Press R", True, (0,0,0))
        screen.blit(prompt_text, (clue2.x, clue2.y - 30))

    # Show popup with clue information
    #Clue1
    if show_popup:
        popup_width, popup_height = 400, 200
        popup_x = (screen_width - popup_width) // 2
        popup_y = (screen_height - popup_height) // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

        pygame.draw.rect(screen, (250,250,250), popup_rect) #box
        pygame.draw.rect(screen, (153,204,255), popup_rect, 2) #border
        
        clue1_text1 = font.render("Loud steps mean he’s near..", True, (0,0,0))
        clue1_text2 = font.render("Soft steps mean he’s far.", True, (0,0,0))
        close_text = font.render("Press C to close", True, (204,204,0))
        screen.blit(clue1_text1, (popup_x + 20, popup_y + 40))
        screen.blit(clue1_text2, (popup_x + 20, popup_y + 70))
        screen.blit(close_text, (popup_rect.x+20, popup_rect.y+130))

        #Clue2
    if show_popup2:
        popup_width, popup_height = 400, 200
        popup_x = (screen_width - popup_width) // 2
        popup_y = (screen_height - popup_height) // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

        pygame.draw.rect(screen, (250,250,250), popup_rect) #box
        pygame.draw.rect(screen, (153,204,255), popup_rect, 2) #border

        clue2_text1 = font.render("He dropped what carried him.", True, (0,0,0))
        clue2_text2 = font.render("The Door besides it holds it still.", True, (0,0,0))
        screen.blit(clue2_text1, (popup_x + 20, popup_y + 40))
        screen.blit(clue2_text2, (popup_x + 20, popup_y + 70))
        screen.blit(close_text, (popup_rect.x+20, popup_rect.y+130))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()