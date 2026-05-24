import pygame
from pygame.locals import *

pygame.init()

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hotel')
font = pygame.font.Font(None,30)

#TESTING PURPOSES
player_rect = pygame.Rect(100, 100, 50,50)
player_speed = 7

#For puzzle
answer= ""
solution = "206"
puzzle_message= "Complete the puzzle to figure out where your friend is hiding."
puzzle_message2= "Input the number of treadmills, balls and dumbells you see."
puzzle_message3= "Press C to close the puzzle."
end_message = " "
inventory = []
show_puzzle = False
show_prompt = False

#Trigger zone for puzzle (when player co)
treadmill= pygame.Rect(300, 300, 50, 50) #just a placeholder cause im not sure of the exact position
treadmill_active = True

input_rect = pygame.Rect(60, 140, 200, 30) #box for user input
color = pygame.Color('lightskyblue3') #color of input box

def puzzle_screen():
    screen.fill((0,0,0))

    #Text box
    box_rect= pygame.Rect(40, 40, 720, 250)
    pygame.draw.rect(screen, (250,250,250), box_rect) #color of box bg
    pygame.draw.rect(screen, (153,204,255), box_rect, 4) #color of border

    #Input Box
    pygame.draw.rect(screen, color, input_rect, 2)

    #Display message and clue
    message_text = font.render(puzzle_message, True, (0,0,0))
    screen.blit(message_text, (60,60))

    message2_text = font.render(puzzle_message2, True, (0,0,0))
    screen.blit(message2_text, (60,80))

    message3_text = font.render(puzzle_message3, True, ('red'))
    screen.blit(message3_text, (60,115))

    #players input code
    input_text = font.render(answer,True, (153,204,255))
    screen.blit(input_text,(input_rect.x + 5, input_rect.y + 5))

    if end_message:
        end_text = font.render(end_message, True, (204, 204,0))
        screen.blit(end_text, (60, 180))


clock = pygame.time.Clock()
run = True
while run :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        #TEST PLAYER MOVEMENT
        if event.type == KEYDOWN:
            if event.key == K_LEFT: player_rect.x -= player_speed
            elif event.key == K_RIGHT:player_rect.x += player_speed
            elif event.key == K_UP: player_rect.y -= player_speed
            elif event.key == K_DOWN: player_rect.y += player_speed

# Player has to press R to open puzzle
            if event.key == K_r and treadmill_active and show_prompt:
                    show_puzzle= True
            if event.key == K_c and show_puzzle:
                    show_puzzle = False


            if show_puzzle and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                 answer = answer[:-1]
                else:
                  answer += event.unicode

                if event.key == pygame.K_RETURN:
                  if answer.strip() == solution:
                    end_message = "Correct! Key to Door 206 is in your inventory."
                    treadmill_active = False
                    puzzle= False
                    inventory.append('Door Key 206')
                  else:
                    end_message= "Wrong answer. Try again!"
                    answer ="" #resets it

#TEST
    screen.fill((200,200,200))
    pygame.draw.rect(screen, (255,0,0), player_rect)
    pygame.draw.rect(screen, (0,255,0), treadmill)

# check if player is in treadmill zone
    if treadmill_active and player_rect.colliderect(treadmill):
     show_prompt = True
    else:
      show_prompt = False

    if show_prompt and not show_puzzle:
     prompt_text = font.render("Press R to solve the puzzle", True, (0,0,0))
     screen.blit(prompt_text, (treadmill.x, treadmill.y - 30))

# Show puzzle if active
    if show_puzzle:
     puzzle_screen()

    pygame.display.flip()
    clock.tick(60)      

pygame.quit()