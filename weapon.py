import pygame
from pygame.locals import *

import os

BASE_DIR = os.path.dirname(__file__)
ASSET_DIR = os.path.join(BASE_DIR, 'assets')
screen = pygame.display.set_mode((800, 600))
pygame.mixer.init()

# Inventory
inventory = []
active_traps = []
salt_line = []
barricade = []

#Sound
unlock_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, "unlock.wav"))
mw_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, "full.wav"))
spray_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, "spray.wav"))
vaccum_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, "vacuum.wav"))
swing_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, "baseballswing.mp3"))

# Weapon Zone
Weapons = {
    #Level 2 Weapons
    "MWpiece1": {
        "zone": pygame.Rect(1379, 894, 90, 90), #just a placeholder cause im not sure of the exact position
        "uses": 0,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "MWpiece1.png")).convert_alpha(), (90,90)),
        "popup_text": "Main Weapon piece 1 collected"
    },
    "BananaPeel": {
        "zone":pygame.Rect(1428, 341, 90, 90), #just a placeholder cause im not sure of the exact position
        "uses": 2,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "BananaPeel.png")).convert_alpha(), (90,90)),
        "popup_text": "Banana Peel = Helps slow down the janitor. 2 use",
        "image_used": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "BananaPeelUse.png")).convert_alpha(), (90,90)),
    },
    "CleaningSpray": {
        "zone": pygame.Rect(3109, 2229, 90, 90),
        "uses": 3,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "cleaning-spray.png")).convert_alpha(), (90,90)),
        "popup_text": "Cleaning Spray = Stops the janitor for a few seconds. 3 uses"
    },
    "BaseballBat":{
        "zone": pygame.Rect(3184, 369, 90, 90),
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "BaseballBat.png")).convert_alpha(), (90,90)),
        "popup_text": "Baseball Bat = Helps defeat the janitor"
    },
    #Level 1 Weapons
    "MWpiece2": {
        "zone": pygame.Rect(150, 380, 80, 55),
        "uses": 0,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "MWpiece2.png")).convert_alpha(), (90,90)),
        "popup_text": "Main Weapon piece 2 collected!"
    },
    "Salt":{
        "zone": pygame.Rect(700, 350, 70, 80),
        "uses": 3,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "Salt.png")).convert_alpha(), (45,45)),
        "popup_text": "Salt = Sprinkle across the doorway or drop a salt line to block the ghost temporarily. 3 uses"
    },
    "KitchenKnife":{
        "zone": pygame.Rect(100, 400, 50, 50),
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "KitchenKnife.png")).convert_alpha(), (70,70)),
        "popup_text": "Kitchen Knife = Kill the receptionist."
    },
    "MWpiece3": {
        "zone": pygame.Rect(200, 470, 50, 100),
        "uses": 0,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "MWpiece3.png")).convert_alpha(), (80,80)),
        "popup_text": "Main weapon piece 3 collected!"
    },
    "Board":{
        "zone": pygame.Rect(360,510,90,30),
        "uses": 2,
        "prompt": "R",
        "collected": False, 
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "Board.png")).convert_alpha(), (90,90)),
        "popup_text": "Board = Barricade one of the doors to trap the receptionist. 2 use"
    },
    "MWfull":{
        "zone": None,
        "prompt" : "", 
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "MWfull.png")).convert_alpha(), (100,100)),
        "popup_text": "Full weapon unlocked! Use it to kill the ghost!"
    }
}

def show_prompt(screen, font, player_rect, weapon, camera_x=0, camera_y=0):
    if weapon["zone"] is not None and not weapon["collected"] and player_rect.colliderect(weapon["zone"]):
        text = font.render(weapon["prompt"], True, (0, 0, 0))
        screen.blit(text, (weapon["zone"].x - camera_x , weapon["zone"].y - camera_y - 30))
        return True
    return False

def pieces_collected ():
    return sum([
        Weapons["MWpiece1"]["collected"],
        Weapons["MWpiece2"]["collected"],
        Weapons["MWpiece3"]["collected"]
    ])

# weapon use
def use_weapon(name, player_rect, enemies, player_direction):
    if "uses" in Weapons[name]:
    # everytime player use it the uses decrease
       Weapons[name]["uses"] -=1
    # if uses reach to 0 then u remove it from the inventory
       if Weapons[name]["uses"] <=0 :
           inventory.remove(Weapons[name])
           return
       
    if name == "BananaPeel":
        slippery_zone = pygame.Rect(player_rect.x+50, player_rect.y, 40, 40)
        active_traps.append({"rect": slippery_zone, "start": pygame.time.get_ticks()})
        for enemy in enemies:
            if enemy.image.get_rect(center=(enemy.x, enemy.y)).colliderect(slippery_zone):
                enemy.weapon_effect("BananaPeel")

    elif name == "CleaningSpray":
        spray_sound.play()
        for enemy in enemies:
            if player_rect.colliderect(enemy.image.get_rect(center=(enemy.x,enemy.y))):
                enemy.weapon_effect("CleaningSpray")

    elif name == "BaseballBat":
        swing_sound.play()
        for enemy in enemies:
            if player_rect.colliderect(enemy.image.get_rect(center=(enemy.x,enemy.y))):
                enemy.weapon_effect("BaseballBat")

    elif name == "Board":
        new_barricade = pygame.Rect(player_rect.x, player_rect.y, 80,20)
        barricade.append(new_barricade)

    elif name == "MWfull":
        vaccum_sound.play()
        for enemy in enemies:
            if player_rect.colliderect(enemy.image.get_rect(center=(enemy.x, enemy.y))):
                enemy.weapon_effect("MWfull")
 
# drawing traps
def draw_traps(screen):
    for trap in active_traps:
        screen.blit(Weapons["BananaPeel"]["image_used"], trap["rect"].topleft)

# Salt 
def place_salt(x,y, direction):
    SALT_LENGTH = 120
    if direction in ["left", "right"]:
        salt_rect = pygame.Rect(x, y, SALT_LENGTH, 10)
    else:
        salt_rect = pygame.Rect(x, y, 10, SALT_LENGTH)
    salt_line.append(salt_rect)

def draw_salt(screen):
    for salt in salt_line: 
        pygame.draw.rect(screen, (255, 255, 255), salt)

def draw_barricades(screen):
    for b in barricade:
        board_image = Weapons["Board"]["image transformed"]
        screen.blit(board_image, b.topleft)

