import pygame
from pygame.locals import *

pygame.init()

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hotel')

font = pygame.font.Font(None,30)

#For puzzle
answer= ""
solution = "206"
message= "Complete the puzzle to figure out where your friend is hiding."
message2= "Input the number of treadmills, balls and dumbells you see."
end_message = " "
inventory = []
puzzle = True

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
    message_text = font.render(message, True, (0,0,0))
    screen.blit(message_text, (60,60))

    message2_text = font.render(message2, True, (0,0,0))
    screen.blit(message2_text, (60,100))

    #players input code
    input_text = font.render(answer,True, (153,204,255))
    screen.blit(input_text,(input_rect.x + 5, input_rect.y + 5))

    if end_message:
        end_text = font.render(end_message, True, (204, 204,0))
        screen.blit(end_text, (60, 180))

    pygame.display.flip()

run = True
while run :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if puzzle and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                answer = answer[:-1]
            else:
             answer += event.unicode

            if event.key == pygame.K_RETURN:
                if answer.strip() == solution:
                    end_message = "Correct! Key to Door 206 is in your inventory."
                    puzzle= False
                    inventory.append('Door Key 206')
                else:
                    end_message= "Wrong answer. Try again!"
                answer ="" #resets it

        puzzle_screen()

pygame.quit()


