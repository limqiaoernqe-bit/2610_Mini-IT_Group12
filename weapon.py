import pygame
from pygame.locals import *

import os

BASE_DIR = os.path.dirname(__file__)
ASSET_DIR = os.path.join(BASE_DIR, 'assets')
screen = pygame.display.set_mode((800, 600))
pygame.mixer.init()

active_traps = []
salt_line = []

#Sound
unlock_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, "unlock.wav"))
mw_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, "full.wav"))
spray_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, "spray.wav"))
vaccum_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, "vacuum.wav"))
swing_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, "baseballswing.mp3"))

# Weapon Zone
L2Weapons = {
    #Level 2 Weapons
    "MWpiece1": {
        "zone": pygame.Rect(1255, 1952, 90, 90), #just a placeholder cause im not sure of the exact position
        "uses": 0,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "MWpiece1.png")).convert_alpha(), (90,90)),
        "popup_text": "Main Weapon piece 1 collected"
    },
    "BananaPeel": {
        "zone":pygame.Rect(1552, 343, 90, 90), #just a placeholder cause im not sure of the exact position
        "uses": 3,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "BananaPeel.png")).convert_alpha(), (90,90)),
        "popup_text": "Banana Peel = Stops the janitor for 40 seconds. 3 use",
        "image_used": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "BananaPeelUse.png")).convert_alpha(), (75,75)),
    },
    "CleaningSpray": {
        "zone": pygame.Rect(3556, 2227, 90, 90),
        "uses": 3,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "cleaning-spray.png")).convert_alpha(), (90,90)),
        "popup_text": "Cleaning Spray = Slows the janitor for a few seconds. 3 uses"
    },
    "BaseballBat":{
        "zone": pygame.Rect(3184, 369, 90, 90),
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "BaseballBat.png")).convert_alpha(), (90,90)),
        "popup_text": "Baseball Bat = Helps defeat the janitor"
    } 
}

L1Weapons = {
    #Level 1 Weapons
    "MWpiece2": {
        "zone": pygame.Rect(2537, 2252, 90, 90),
        "uses": 0,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "MWpiece2.png")).convert_alpha(), (90,90)),
        "popup_text": "Main Weapon piece 2 collected!"
    },
    "Salt":{
        "zone": pygame.Rect(2422, 104, 45, 45),
        "uses": 3,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "Salt.png")).convert_alpha(), (45,45)),
        "popup_text": "Salt = Sprinkle across the doorway or drop a salt line to block the ghost temporarily. 3 uses"
    },
    "KitchenKnife":{
        "zone": pygame.Rect(1918, 328, 95, 95),
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "KitchenKnife.png")).convert_alpha(), (70,70)),
        "popup_text": "Kitchen Knife = Kill the receptionist."
    },
    "MWpiece3": {
        "zone": pygame.Rect(146, 1127, 50, 100),
        "uses": 0,
        "prompt": "R",
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "MWpiece3.png")).convert_alpha(), (80,80)),
        "popup_text": "Main weapon piece 3 collected!"
    },
    "MWfull":{
        "zone": None,
        "prompt" : "", 
        "collected": False,
        "image": pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "MWfull.png")).convert_alpha(), (100,100)),
        "popup_text": "Full weapon unlocked! Use it to kill the ghost!"
    }
}

Weapons = {}
Weapons.update(L1Weapons)
Weapons.update(L2Weapons)

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
def use_weapon(name, player, player_rect, enemies, player_direction, inventory):
    if "uses" in Weapons[name]:
    # everytime player use it the uses decrease
       Weapons[name]["uses"] -=1
    # if uses reach to 0 then u remove it from the inventory
       if Weapons[name]["uses"] <=0 :
           inventory.remove_item(name)
           if player.held_weapon == name:
               player.held_weapon = None
           return
       
    if name == "BananaPeel":
        slippery_zone = pygame.Rect(player.x, player.y + 40, 40, 40)
        active_traps.append({
            "rect": slippery_zone, 
            })
        Weapons[name]["uses"] -= 1
        if Weapons[name]["uses"] <= 0:
            inventory.remove_item(name)
            if player.held_weapon == name:
                player.held_weapon = None

    elif name == "CleaningSpray":
        spray_sound.play()
        attack_range = player_rect.inflate(80,80)
        for enemy in enemies:
            if attack_range.colliderect(enemy.rect):
                enemy.weapon_effect("CleaningSpray")
                Weapons[name]["uses"] -= 1 #only if it hits
                if Weapons[name]["uses"] <= 0:
                    inventory.remove_item(name)
                    if player.held_weapon == name:
                        player.held_weapon = None
                return

    elif name == "BaseballBat":
        swing_sound.play()
        attack_range = player_rect.inflate(80,80)
        for enemy in enemies:
            if attack_range.colliderect(enemy.rect):
                enemy.weapon_effect("BaseballBat")

    elif name == "MWfull":
        vaccum_sound.play()
        for enemy in enemies:
            if player_rect.colliderect(enemy.rect):
                enemy.weapon_effect("MWfull")

    elif name == "KitchenKnife":
        for enemy in enemies:
            if player_rect.colliderect(enemy.rect):
                enemy.weapon_effect("KitchenKnife")
 
# drawing traps
def draw_traps(screen, camera_x=0, camera_y=0):
    for trap in active_traps:
        screen.blit(
            Weapons["BananaPeel"]["image_used"],
            (trap["rect"].x - camera_x, trap["rect"].y - camera_y)
        )

# Salt 
def place_salt(x,y, direction):
    SALT_LENGTH = 120
    if direction in ["left", "right"]:
        salt_rect = pygame.Rect(x, y, SALT_LENGTH, 10)
    else:
        salt_rect = pygame.Rect(x, y, 10, SALT_LENGTH)
    salt_line.append(salt_rect)

def draw_salt(screen, camera_x=0, camera_y=0):
    for salt in salt_line: 
        pygame.draw.rect(
            screen,
            (255,255,255),
            pygame.Rect(
                salt.x - camera_x,
                salt.y - camera_y, 
                salt.width, 
                salt.height
            )
        )
