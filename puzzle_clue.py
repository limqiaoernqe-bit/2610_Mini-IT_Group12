import pygame
from pygame.locals import K_BACKSPACE, K_RETURN
import os
from inventory import ROOM_206_KEY, ROOM116_KEY

BASE_DIR = os.path.dirname(__file__)
ASSET_DIR = os.path.join(BASE_DIR, 'assets')

# Puzzle Zone
Puzzle = {
   "Treadmill":{
      "zone": pygame.Rect(243,640,100,80),
      "prompt": "R",
      "collected": False,
      "solution": "246",
      "answer": "",
      "active": False,
      "end_message":""
   }
}

PuzzleL1 = {
    "KeyArea": {
      "zone": pygame.Rect(2294,1802,100,80),
      "prompt": "R",
      "collected": False,
      "solution": "116",
      "answer": "",
      "active": False,
      "end_message":""
    }
}
clue_image = pygame.image.load(os.path.join(ASSET_DIR, "Clue.png"))
clue_image = pygame.transform.scale(clue_image, (80,80))

# Clue Zone
ClueL2 = {
    "Clue1": {
        "zone": pygame.Rect(2095,2227,150,150),
        "prompt": "R",
        "active": True,
        "show_prompt": False,
        "show_popup": False,
        "text": "Loud steps mean he's near, Soft steps mean he's far",
        "image": clue_image,
    }
}

ClueL1 = {
    "Clue2": {
        "zone": pygame.Rect(2034,1836,90,90),
        "prompt":"R",
        "active": True,
        "show_prompt": False,
        "show_popup": False,
        "text":"He dropped what carried him. The door besides it holds it",
        "image": clue_image,
    }
}  

def show_puzzle_prompt(screen, font, player_rect, item, marker_x, marker_y, camera_x=0, camera_y=0):
   
   # Don't show anything if puzzle already completed
   if item["collected"]:
       return 
   
   draw_x = marker_x - camera_x 
   draw_y = marker_y - camera_y
   
   # Draw circle around R
   pygame.draw.circle(screen, (153,204,255), (draw_x, draw_y), 20)
   
   text = font.render(item["prompt"], True, (0,0,0))
   text_rect = text.get_rect(center=(draw_x, draw_y))
   screen.blit(text, text_rect)

def show_clue_prompt(screen,font,player_rect,clue, camera_x=0, camera_y=0):
    if clue["active"] and player_rect.colliderect(clue["zone"]):
        text = font.render(clue["prompt"], True, (0,0,0))
        screen.blit(text, (clue["zone"].x - camera_x, clue["zone"].y - camera_y - 30))
        clue["show_prompt"]= True
    else:
        clue["show_prompt"] = False

def show_popup(screen,font,clue, screen_width =800, screen_height = 600):
    popup_width = 400
    line_height = font.size("Tg")[1]

    # Word wrap
    words = clue["text"].split(" ")
    lines, line = [], ""
    for word in words:
        test_line = line + word + " "
        if font.size(test_line)[0] < popup_width - 40:
            line = test_line
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    # so that the height changes auto
    total_height = len(lines) * line_height + 40
    popup_height = max(200, total_height)

    # center box
    popup_x = (screen_width - popup_width) // 2
    popup_y = (screen_height - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

    # Draw box
    pygame.draw.rect(screen, (255,255,255), popup_rect)
    pygame.draw.rect(screen, (153,204,255), popup_rect, 2)

    # draw text in center
    y = popup_rect.y + (popup_rect.height - total_height) // 2
    for line in lines:
        text_surface = font.render(line, True, (0,0,0))
        text_rect = text_surface.get_rect(centerx=popup_rect.centerx)
        text_rect.y = y
        screen.blit(text_surface, text_rect)
        y += line_height

    close_text = font.render("Press C to close", True, (204,204,0))
    screen.blit(close_text, (popup_rect.x+20, popup_rect.y+popup_rect.height-30))

def puzzle_screen(puzzle,screen, font, screen_width=800, screen_height=600):

    #Text box
    box_width = 720
    box_height = 250

    #To make the box in center
    box_x = (screen_width - box_width) // 2
    box_y = (screen_height - box_height) //2

    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

    pygame.draw.rect(screen, (250,250,250), box_rect) #color of box bg
    pygame.draw.rect(screen, (153,204,255), box_rect, 4) #color of border

    if puzzle["collected"]:
        success_msg = font.render(puzzle["end_message"], True, (0,200,0))
        success_rect = success_msg.get_rect(center=box_rect.center)
        screen.blit(success_msg, success_rect)
    else:
        if puzzle is PuzzleL1["KeyArea"]:   
           msg1 = font.render("Input a room number you would like the key for", True, (0,0,0))
           msg2 = font.render("Press C to close the puzzle", True, (255,0,0))
           screen.blit(msg1, (box_x + 20, box_y + 20))
           screen.blit(msg2, (box_x + 20, box_y + 50))
        else:
           msg1 = font.render("Complete the puzzle to find where you friend is hiding", True, (0,0,0))
           msg2 = font.render("Input the number of treadmills, balls and dumbells", True, (0,0,0))
           msg3 = font.render("( first row only ) you see.", True, (0,0,0))
           msg4 = font.render("Press C to close the puzzle", True, (255,0,0))
           screen.blit(msg1, (box_x + 20, box_y + 20))
           screen.blit(msg2, (box_x + 20, box_y + 50))
           screen.blit(msg3, (box_x + 20, box_y + 80))
           screen.blit(msg4, (box_x + 20, box_y + 140))

        # Input box
        input_rect = pygame.Rect(box_x + 20, box_y + 110,200,30)
        pygame.draw.rect(screen, pygame.Color('lightskyblue3'), input_rect, 2)
        input_text = font.render(str(puzzle["answer"]), True, (153,204,255))
        screen.blit(input_text, (input_rect.x + 5, input_rect.y +5))

        if puzzle["end_message"]:
          end_text = font.render(puzzle["end_message"], True, (204,204,0))
          end_text_rect = end_text.get_rect(centerx=box_rect.centerx)
          end_text_rect.bottom = box_rect.bottom - 20
          screen.blit(end_text,end_text_rect)

def handle_puzzle_input(event, active_puzzle, inventory, object_interaction):
    from inventory import game_inventory as inventory, ROOM_206_KEY
    if event.type == pygame.KEYDOWN:    
               if event.key == K_BACKSPACE:
                  active_puzzle["answer"] = active_puzzle["answer"][:-1]
               elif event.key == K_RETURN:
                  if active_puzzle ["answer"].strip() == active_puzzle["solution"]:
                     active_puzzle["collected"] = True
                     # L1 key area
                     if active_puzzle is PuzzleL1["KeyArea"]:
                         active_puzzle["end_message"] = "Key Available. Key Room 116 is now in your inventory"
                         inventory.add_item(ROOM116_KEY)
                         object_interaction.trigger(ROOM116_KEY)
                     else: 
                       active_puzzle["end_message"] = "Correct! Key to Door 206 is in your inventory."
                       inventory.add_item(ROOM_206_KEY)
                       object_interaction.trigger(ROOM_206_KEY)
                       active_puzzle["correct_start"] = pygame.time.get_ticks()
                  else:
                        active_puzzle["end_message"] = "Wrong answer. Try again!"
                        active_puzzle["answer"] = ""
               elif event.key == pygame.K_c:
                    active_puzzle["active"] = False
               else:
                    active_puzzle["answer"] = str(active_puzzle["answer"]) + str(event.unicode)
