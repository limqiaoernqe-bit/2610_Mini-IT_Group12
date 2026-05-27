import pygame
from pygame.locals import *

import os

BASE_DIR = os.path.dirname(__file__)
ASSET_DIR = os.path.join(BASE_DIR, 'assets')
pygame.init ()
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hotel')
font = pygame.font.Font(None,30)

#PLAYER TESTING PURPOSES
player_rect = pygame.Rect(100, 100, 50,50)
player_speed = 7

# Inventory
inventory = []
main_weapon_unlocked = False
main_weapon_popup_shown = False

# Weapon Zone
Weapons = {
    #Level 2 Weapons
    "MWpiece1": {
        "zone": pygame.Rect(600, 400, 20, 10), #just a placeholder cause im not sure of the exact position
        "uses": 0,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "MWpiece1.png")).convert_alpha(), (90,90)),
        "image transformed": pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSET_DIR, "MWpiece1.png")).convert_alpha(), (90,90)),
        "popup_text": "Main Weapon piece 1 collected"
    },
    "BananaPeel": {
        "zone":pygame.Rect(350, 390, 50, 85), #just a placeholder cause im not sure of the exact position
        "uses": 2,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "BananaPeel.png")).convert_alpha(), (90,90)),
        "image transformed": pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSET_DIR, "BananaPeel.png")).convert_alpha(), (90,90)),
        "popup_text": "Banana Peel = Helps slow down the janitor. 2 uses"
    },
    "CleaningSpray": {
        "zone": pygame.Rect(500, 350, 70, 50),
        "uses": 3,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "cleaning-spray.png")).convert_alpha(), (90,90)),
        "image transformed": pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSET_DIR, "cleaning-spray.png")).convert_alpha(), (90,90)),
        "popup_text": "Cleaning Spray = Use it to attack the janitor. 3 uses"
    },
    "BaseballBat":{
        "zone": pygame.Rect(350, 350, 50, 50),
        "uses": 1,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "BaseballBat.png")).convert_alpha(), (90,90)),
        "image transformed": pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSET_DIR, "BaseballBat.png")).convert_alpha(), (90,90)),
        "popup_text": "Baseball Bat = Helps defeat the janitor. 1 use"
    },
    #Level 1 Weapons
    "MWpiece2": {
        "zone": pygame.Rect(150, 380, 80, 55),
        "uses": 0,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "MWpiece2.png")).convert_alpha(), (90,90)),
        "image transformed": pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSET_DIR, "MWpiece2.png")).convert_alpha(), (90,90)),
        "popup_text": "Main Weapon piece 2 collected!"
    },
    "Salt":{
        "zone": pygame.Rect(700, 350, 70, 80),
        "uses": 1,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "Salt.png")).convert_alpha(), (45,45)),
        "image transformed": pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSET_DIR, "Salt.png")).convert_alpha(), (45,45)),
        "popup_text": "Salt = Sprinkle across the doorway or drop a salt line to block the ghost temporarily. 1 use"
    },
    "KitchenKnife":{
        "zone": pygame.Rect(100, 400, 50, 50),
        "uses": 1,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "KitchenKnife.png")).convert_alpha(), (70,70)),
        "image transformed": pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSET_DIR, "KitchenKnife.png")).convert_alpha(), (70,70)),
        "popup_text": "Kitchen Knife = Kill the receptionist. 1 use"
    },
    "MWpiece3": {
        "zone": pygame.Rect(200, 470, 50, 100),
        "uses": 0,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "MWpiece3.png")).convert_alpha(), (80,80)),
        "image transformed": pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSET_DIR, "MWpiece3.png")).convert_alpha(), (80,80)),
        "popup_text": "Main weapon piece 3 collected!"
    },
    "Board":{
        "zone": pygame.Rect(360,510,90,30),
        "uses": 2,
        "prompt": "R",
        "collected": False, 
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "Board.png")).convert_alpha(), (90,90)),
        "image transformed": pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSET_DIR, "Board.png")).convert_alpha(),(90,90)),
        "popup_text": "Board = Barricade one of the doors to trap the receptionist. 2 use"
    },
    "MWfull":{
        "zone": None,
        "uses": 1,
        "prompt" : "", 
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "MWfull.png")).convert_alpha(), (100,100)),
        "image transformed": pygame.transform.smoothscale(pygame.image.load(os.path.join(ASSET_DIR, "MWfull.png")).convert_alpha(),(100,100)),
        "popup_text": "Full weapon unlocked"
    }
}
# Popup system
show_popup = False
popup_start_time = 0
popup_duration = 1
popup_message = ""

def show_prompt(screen, font, player_rect, weapon):
    if weapon["zone"] is not None and not weapon["collected"] and player_rect.colliderect(weapon["zone"]):
        text = font.render(weapon["prompt"], True, (0, 0, 0))
        screen.blit(text, (weapon["zone"].x, weapon["zone"].y - 30))
        return True
    return False

def draw_text(surface, text, rect, font, color):
    words = text.split(" ")
    lines = []
    line = ""
    for word in words:
        test_line = line + word + " "
        if font.size(test_line)[0] < rect.width - 40:
            line = test_line
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)


    line_height = font.size("Tg")[1]
    total_height =len(lines) * line_height
    y = rect.y + (rect.height - total_height) // 2


    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(centerx=rect.centerx, y=y)
        surface.blit(text_surface, text_rect)
        y += line_height

def pieces_collected ():
    return sum([
        Weapons["MWpiece1"]["collected"],
        Weapons["MWpiece2"]["collected"],
        Weapons["MWpiece3"]["collected"]
    ])


clock = pygame.time.Clock()
run = True

def mw_image_get_rect(center):
    raise NotImplementedError

while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False


        # TESTING PURPOSES
        if event.type == KEYDOWN:
            if event.key == K_LEFT: player_rect.x -= player_speed
            elif event.key == K_RIGHT: player_rect.x += player_speed
            elif event.key == K_UP: player_rect.y -= player_speed
            elif event.key == K_DOWN: player_rect.y += player_speed
       
        # Collect Weapons
            if event.key == K_r:
               for name, weapon in Weapons.items():
                   if weapon["zone"] is not None and player_rect.colliderect(weapon["zone"]) and not weapon["collected"]:
                      weapon["collected"] = True
                      inventory.append(name)

                      if pieces_collected() == 3 and not main_weapon_unlocked:
                          main_weapon_unlocked = True
                          Weapons["MWfull"]["collected"] = True
                          inventory.append("MWfull")
                          main_weapon_popup_shown = True
                          popup_start_time = pygame.time.get_ticks()
                      else:
                         show_popup = True
                         popup_start_time = pygame.time.get_ticks()
                         popup_message = weapon["popup_text"]

        # hide popup
        if show_popup and (pygame.time.get_ticks()- popup_start_time > popup_duration * 1000):
             show_popup = False


        # Testing purposes
        screen.fill((200,200,200))
        pygame.draw.rect(screen, (0, 0, 255), player_rect)


        # Draw image of weapons
        for name, weapon in Weapons.items():
             if weapon["zone"] is not None and not weapon["collected"]:
                screen.blit(weapon["image"], weapon["zone"].topleft)
             show_prompt(screen, font, player_rect, weapon)


        # popup box
        if show_popup:
            popup_width = 400
            line_height = font.size("Tg")[1]
            words = popup_message.split(" ")
            lines, line = [], ""
            for word in words:
                test_line = line + word + " "
                if font.size(test_line)[0] < popup_width - 40:
                    line = test_line
                else:
                    lines.append(line)
                    line = word + " "
            lines.append(line)
            total_height = len(lines) * line_height + 40
            popup_height = max (200, total_height)

            popup_x = (screen_width - popup_width) // 2
            popup_y = (screen_height - popup_height) // 2
            popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

            pygame.draw.rect(screen, (255, 255, 255), popup_rect)
            pygame.draw.rect(screen, (153,204,255), popup_rect, 2)

            y = popup_rect.y + (popup_rect.height - total_height) //2
            for line in lines:
                text_surface = font.render(line, True, (0, 0, 0))
                text_rect = text_surface.get_rect(centerx=popup_rect.centerx)
                text_rect.y = y
                screen.blit(text_surface, text_rect)
                y += line_height

        if main_weapon_unlocked and main_weapon_popup_shown:
            MWimage = Weapons["MWfull"]["image"]
            MW_rect = MWimage.get_rect(center=(screen_width//2, screen_height//2))
            screen.blit(MWimage, MW_rect)

            if pygame.time.get_ticks() - popup_start_time > 1000:
                main_weapon_popup_shown = False
                show_popup = True
                popup_start_time = pygame.time.get_ticks()
                popup_message = Weapons["MWfull"]["popup_text"]

        pygame.display.flip()
        clock.tick(60)

pygame.quit()