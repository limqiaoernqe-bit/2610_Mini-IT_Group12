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

inventory = []

Puzzle = {
   "Treadmill":{
      "zone": pygame.Rect(300,300,50,50),
      "prompt": "R",
      "collected": False,
      "solution": "206",
      "answer": "",
      "active": False,
      "end_message":""
   }
}
def show_prompt(screen, font, player_rect, item):
   # Show R if player is around the zone
   if not item["collected"] and player_rect.colliderect(item["zone"]):
      text = font.render(item["prompt"], True, (0,0,0))
      screen.blit(text,(item["zone"].x, item["zone"].y - 30))
      return True
   return False

def puzzle_screen(puzzle):

    #Text box
    box_width = 720
    box_height = 250

    #To make the box in center
    box_x = (screen_width - box_width) // 2
    box_y = (screen_height - box_height) //2

    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

    pygame.draw.rect(screen, (250,250,250), box_rect) #color of box bg
    pygame.draw.rect(screen, (153,204,255), box_rect, 4) #color of border

    msg1 = font.render("Complete the puzzle to find where you friend is hiding", True, (0,0,0))
    msg2 = font.render("Input the number of treadmills, balls and dumbells you see.", True, (0,0,0))
    msg3 = font.render("Press C to close the puzzle", True, (255,0,0))
    screen.blit(msg1, (box_x + 20, box_y + 20))
    screen.blit(msg2, (box_x + 20, box_y + 50))
    screen.blit(msg3, (box_x + 20, box_y + 80))

    input_rect = pygame.Rect(box_x + 20, box_y + 110,200,30)
    pygame.draw.rect(screen, pygame.Color('lightskyblue3'), input_rect, 2)
    input_text = font.render(puzzle["answer"], True, (153,204,255))
    screen.blit(input_text, (input_rect.x + 5, input_rect.y +5))

    if puzzle["end_message"]:
       end_text = font.render(puzzle["end_message"], True, (204,204,0))
       screen.blit(end_text,(60,180))

clock = pygame.time.Clock()
run = True
active_puzzle = None

while run :
    clock.tick(60)
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
            if event.key == K_r:
               for name, puzzle in Puzzle.items():
                  if player_rect.colliderect(puzzle["zone"])and not puzzle["collected"]:
                     puzzle["active"] = True
                     active_puzzle = puzzle

            if event.key == K_c and active_puzzle:
                active_puzzle["active"] = False
                active_puzzle = None

            if active_puzzle and active_puzzle["active"]:
               puzzle_screen(active_puzzle)
               if event.key == K_BACKSPACE:
                  active_puzzle["answer"] = active_puzzle["answer"][:-1]
               elif event.key == K_RETURN:
                  if active_puzzle ["answer"].strip() == active_puzzle["solution"]:
                     active_puzzle["collected"] = True
                     active_puzzle["end_message"] = "Correct! Key to Door 206 is in your inventory."
                     inventory.append("Door Key 206")
                  else:
                        active_puzzle["end_message"] = "Wrong answer. Try again!"
                        active_puzzle["answer"] = ""
               else:
                    active_puzzle["answer"] += event.unicode

#TEST
    screen.fill((200,200,200))
    pygame.draw.rect(screen, (255,0,0), player_rect)

    for name, puzzle in Puzzle.items():
        pygame.draw.rect(screen, (0,255,0), puzzle["zone"],2)
        show_prompt(screen, font, player_rect, puzzle)

    if active_puzzle and active_puzzle["active"]:
        puzzle_screen(active_puzzle)

    pygame.display.flip()

pygame.quit()