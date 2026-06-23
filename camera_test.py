import pygame
import pytmx

# Used to open level 1 after player reaches the stairs
import subprocess

from player import Player
from room_navigation import RoomTrigger
from door import Door
from inventory import (
    Inventory,
    ROOM_210_KEY,
    JANITOR_KEY,
    ROOM_206_KEY,
    SECURITY_BADGE
)
from puzzle_clue import Puzzle, Clue, show_puzzle_prompt, show_clue_prompt, show_popup, puzzle_screen, handle_puzzle_input 
from weapon import Weapons, inventory, use_weapon, show_prompt, draw_traps, place_salt, draw_salt, pieces_collected, unlock_sound, mw_sound
from inventory_bar import draw_inventory, handle_inventory_click 
from janitor import Janitor

# Weapon Popup system
weapon_popup = False
popup_start_time = 0
popup_duration = 1
popup_message = ""
main_weapon_unlocked = False
main_weapon_popup_shown = False

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

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Camera Test")

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

# Load Map
tmx_data = pytmx.load_pygame("level2_map.tmx")
TILE_SIZE = tmx_data.tilewidth

# Level 2 Collision layers
collision_layers = [
    "Collision",
    "stairs collision",
    "room210 collision",
    "janitor collision",
    "room206 collision"
]

normal_walls = []
stairs_walls = []
room210_walls = []
janitor_walls = []
room206_walls = []

# Create collision recctangles
for layer in tmx_data.visible_layers:

    if isinstance(layer, pytmx.TiledTileLayer):

        if layer.name in collision_layers:

            for x, y, gid in layer:

                if gid != 0:

                    wall_rect = pygame.Rect(
                        x * TILE_SIZE,
                        y * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )

                    if layer.name == "Collision":
                        normal_walls.append(wall_rect)

                    elif layer.name == "stairs collision":
                        stairs_walls.append(wall_rect)

                    elif layer.name == "room210 collision":
                        room210_walls.append(wall_rect)

                    elif layer.name == "janitor collision":
                        janitor_walls.append(wall_rect)

                    elif layer.name == "room206 collision":
                        room206_walls.append(wall_rect)

# Create Player
player = Player()

# Janitor spawn position
janitor = Janitor(
    1632,
    1056
)

enemies = [janitor]

# Spawn position
player.x = 2160
player.y = 2160

inventory = Inventory()

# Currently active puzzle (None when no puzzle is active)
active_puzzle = None

# Level 2 Door Objects
room210_door = Door(
    "Room 210",
    ROOM_210_KEY
)

janitor_door = Door(
    "Janitor Room",
    JANITOR_KEY
)

room206_door= Door(
    "Room 206",
    ROOM_206_KEY  
)

# Room Triggers
maintenance_room = RoomTrigger(
    pygame.Rect(1897, 2013, 39, 197),
    "Maintenance Room"
)

gym_room = RoomTrigger(
    pygame.Rect(1608, 389, 72, 184),
    "Gym Room"
)

janitor_room = RoomTrigger(
    pygame.Rect(3265, 2333, 192, 55),
    "Janitor Room",
    locked=True
)

room_206 = RoomTrigger(
    pygame.Rect(71, 2300, 44, 101),
    "Room 206",
    locked=True
)

room_210 = RoomTrigger(
    pygame.Rect(3408, 463, 144, 39),
    "Room 210",
    locked=True
)

room_208 = RoomTrigger(
    pygame.Rect(2689, 463, 141, 43),
    "Room 208"
)

room_204 = RoomTrigger(
    pygame.Rect(76, 1439, 45, 97),
    "Room 204"
)

room_203 = RoomTrigger(
    pygame.Rect(1420, 1439, 40, 100),
    "Room 203"
)

room_205 = RoomTrigger(
    pygame.Rect(75, 1872, 40, 93),
    "Room 205"
)

room_202 = RoomTrigger(
    pygame.Rect(1423, 1875, 37, 95),
    "Room 202"
)

room_201 = RoomTrigger(
    pygame.Rect(1423, 2301, 41, 100),
    "Room 201"
)

room_207 = RoomTrigger(
    pygame.Rect(2157, 1211, 148, 51),
    "Room 207"
)

room_209 = RoomTrigger(
    pygame.Rect(2785, 1212, 143, 48),
    "Room 209"
)

room_211 = RoomTrigger(
    pygame.Rect(3408, 1207, 143, 59),
    "Room 211"
)

# Stairs to Level 1
stairs_trigger = RoomTrigger(
    pygame.Rect(2475, 2776, 241, 104),
    "Stairs", 
    locked=True
)

# Static item hitboxes (keys placed at fixed map coordinates)
room210_key_rect = pygame.Rect(
    3160, 
    2052, 
    56, 
    48
)

janitor_key_rect = pygame.Rect(
    1360,
    312,
    64,
    63
)

security_badge_rect = pygame.Rect(
    3021,
    2041,
    59,
    53
)

# Key collection status
room210_key_collected = False
janitor_key_collected = False
security_badge_collected = False

room_triggers = [
    maintenance_room,
    gym_room,
    janitor_room,
    room_206,
    room_210,
    room_208,
    room_204,
    room_203,
    room_205,
    room_202,
    room_201,
    room_207,
    room_209,
    room_211,
    stairs_trigger
]

# Draw map function
def draw_map(surface, camera_x, camera_y):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    surface.blit(
                        tile, 
                        (
                            x * TILE_SIZE - camera_x,
                            y * TILE_SIZE - camera_y
                        )
                    )

# Main Game Loop
running = True

while running:

    clock.tick(60)

    # Player collision rect
    player_rect = pygame.Rect(
        player.x - 30,
        player.y - 60,
        60,
        60
    )  

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:

                # Open puzzle
                if player_rect.colliderect(Puzzle["Treadmill"]["zone"]):
                    Puzzle["Treadmill"]["active"] = True

                # Pick up Room 210 Key
                elif (
                    player_rect.colliderect(room210_key_rect)
                    and not room210_key_collected
                ):
                    inventory.add_item(ROOM_210_KEY)
                    room210_key_collected = True

                # Pick up Janitor Key
                elif (
                    player_rect.colliderect(janitor_key_rect)
                    and not janitor_key_collected
                ):
                    inventory.add_item(JANITOR_KEY)
                    janitor_key_collected = True
                    
                # Pick up Security Badge
                elif (
                    player_rect.colliderect(security_badge_rect)
                    and not security_badge_collected
                ):
                    inventory.add_item(SECURITY_BADGE)
                    security_badge_collected = True

                # Go to level 1 after stairs are unlocked
                elif stairs_trigger.check_collision(player_rect):
                    if not stairs_trigger.locked:
                        print("Going to Level 1...")
                        # Close level 2 and open level 1
                        pygame.quit()

                        subprocess.run(["python", "level1_map.py"])
                        running = False
                    else:
                        print("The stairs are locked. Find a way to unlock them.")

            # close puzzle when press C
            if event.key == pygame.K_c and active_puzzle and active_puzzle["active"]:
                active_puzzle["active"] = False

        # to find coordinates
        if event.type == pygame.MOUSEBUTTONDOWN:
            world_x = event.pos[0] + camera_x
            world_y = event.pos[1] + camera_y
            print(f"World Coordinates: ({world_x}, {world_y})")

            mouse_x, mouse_y = event.pos
            for i, weapon_name in enumerate(inventory.items):
                rect = pygame.Rect(50 + i*60, SCREEN_HEIGHT-60, 50, 50)
                if rect.collidepoint(mouse_x, mouse_y):
                   selected_index = i

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            handle_inventory_click(event.pos, player, inventory, SCREEN_HEIGHT)

        # puzzle 
        if active_puzzle and active_puzzle["active"]:
            handle_puzzle_input(event, active_puzzle, inventory)

        # clue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                for clue in Clue.values():
                    if clue["show_prompt"] and clue ["active"]:
                        clue["show_popup"] = True
                        clue["active"] = False
            if event.key == pygame.K_c:
                for clue in Clue.values():
                    if clue ["show_popup"]:
                        clue["show_popup"] = False

        # Collect Weapons
            if event.key == pygame.K_r:
              for name, weapon in Weapons.items():
                if weapon["zone"] is not None and player_rect.colliderect(weapon["zone"]) and not weapon["collected"]:
                    weapon["collected"] = True
                    unlock_sound.play()
                    inventory.add_item(name)

                    if pieces_collected() == 3 and not main_weapon_unlocked:
                        main_weapon_unlocked = True
                        Weapons["MWfull"]["collected"] = True
                        inventory.remove_item("MWpiece1")
                        inventory.remove_item("MWpiece2")
                        inventory.remove_item("MWpiece3")
                        inventory.add_item("MWfull")
                        main_weapon_popup_shown = True
                        popup_start_time = pygame.time.get_ticks()
                        mw_sound.play()
                    else:
                        weapon_popup = True
                        popup_start_time = pygame.time.get_ticks()
                        popup_message = weapon["popup_text"]

                        # Use currectly selected eapons
            if event.key == pygame.K_w:

                if player.held_weapon is not None:
                    use_weapon(
                        player.held_weapon,
                        player_rect,
                        enemies,
                        player.direction
                    )

    # Player Movement
    keys = pygame.key.get_pressed()

    # Active collision walls
    active_walls = normal_walls + stairs_walls

    # Locked room walls    
    if room210_door.is_locked():
        active_walls += room210_walls

    if janitor_door.is_locked():
        active_walls += janitor_walls

    if room206_door.is_locked():
        active_walls += room206_walls

    # Move player
    player.update(keys, active_walls)

    # Move janitor
    janitor.update(
        player.x, 
        player.y,
        active_walls
    )

    # Unlock stairs when janitor is defeated
    if janitor.defeat:
        stairs_trigger.locked = False

    # Camera System
    camera_x = player.x - SCREEN_WIDTH // 2
    camera_y = player.y - SCREEN_HEIGHT // 2

    # Draw everything
    screen.fill((0, 0, 0))

    # Draw map
    draw_map(screen, camera_x, camera_y)

    # Draw Janitor
    janitor.draw(screen, camera_x, camera_y)

    # Draw player 
    player.draw(screen, camera_x, camera_y)

# WEAPON PART
    # hide popup
    if weapon_popup and (pygame.time.get_ticks()- popup_start_time > popup_duration * 1000):
        weapon_popup = False

        # Effect when main weapon shows
    if weapon_popup or (main_weapon_unlocked and main_weapon_popup_shown):
        dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        dark_overlay.set_alpha(180) # darkens the bg and makes the weapon stands out 
        dark_overlay.fill((0,0,0))
        screen.blit(dark_overlay, (0,0))

        # popup box
    if weapon_popup:
        popup_width = 400
        popup_height = 200
        popup_x =(SCREEN_WIDTH - popup_width) //2 
        popup_y = (SCREEN_HEIGHT - popup_height) //2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

            #draw popup box
        pygame.draw.rect(screen, (255,255,255), popup_rect)
        pygame.draw.rect(screen, (153, 204, 255), popup_rect, 2)
        draw_text(screen, popup_message, popup_rect, font, (0,0,0))

    if main_weapon_unlocked and main_weapon_popup_shown:
        MWimage = Weapons["MWfull"]["image"]
        MW_rect = MWimage.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(MWimage, MW_rect)

        if pygame.time.get_ticks() - popup_start_time > 1000:
            main_weapon_popup_shown = False
            weapon_popup = True
            popup_start_time = pygame.time.get_ticks()
            popup_message = Weapons["MWfull"]["popup_text"]

    # Draw image of weapons
    for name, weapon in Weapons.items():
        if weapon["zone"] is not None and not weapon["collected"]:
            screen.blit(weapon["image"],( weapon["zone"].x - camera_x, weapon["zone"].y - camera_y))
        show_prompt(screen, font, player_rect, weapon, camera_x, camera_y)

    # draw use weapon
    draw_traps(screen)
    draw_salt(screen)

    # outline puzzle zone & clue js to check
    zone = Puzzle["Treadmill"]["zone"]
    pygame.draw.rect(screen, (255, 0, 0),
         pygame.Rect(zone.x - camera_x, zone.y - camera_y, zone.width, zone.height), 2)
    
        # draw inventory
    draw_inventory(screen, inventory, Weapons, SCREEN_HEIGHT, SCREEN_WIDTH)
    
    for clue in Clue.values():
        czone = clue["zone"]
        pygame.draw.rect(screen, (255, 0, 0),
            pygame.Rect(czone.x - camera_x, czone.y - camera_y, czone.width, czone.height), 2)

    # Press E to unlock Room 210
    if room_210.check_collision(player_rect):
        
        if keys[pygame.K_e]:
            inventory.use_item(
                ROOM_210_KEY,
                room210_door
            )

    # Press E to unlock Janitor Room
    if janitor_room.check_collision(player_rect):
        
        if keys[pygame.K_e]:
            
            inventory.use_item(
                JANITOR_KEY,
                janitor_door
            )
    
    # Press E to unlock Room 206
    if room_206.check_collision(player_rect):
        
        if keys[pygame.K_e]:
            
            inventory.use_item(
                ROOM_206_KEY,
                room206_door
            )

    # Sync trigger status with door status
    room_210.locked = room210_door.is_locked()
    janitor_room.locked = janitor_door.is_locked()
    room_206.locked = room206_door.is_locked()

    # Room labels
    for room in room_triggers:

        # puzzle trigger 
        if player_rect.colliderect(Puzzle["Treadmill"]["zone"]):
                if keys[pygame.K_r]:
                    treadmill_puzzle = Puzzle["Treadmill"]
                    if not treadmill_puzzle["collected"]:
                        treadmill_puzzle["active"] = True
                        active_puzzle = treadmill_puzzle

            # puzzle prompt
        show_puzzle_prompt(screen,font, Puzzle["Treadmill"],255, 747, camera_x, camera_y)

        if active_puzzle and active_puzzle["active"]:
                puzzle_screen(active_puzzle, screen, font)

        if active_puzzle and active_puzzle["collected"]:
            if pygame.time.get_ticks() - active_puzzle.get("correct_start", 0) > 3000:  # Show message for 3 seconds
                active_puzzle["active"] = False

            # clue 
        for clue in Clue.values():
                if "image" in clue:
                    screen.blit(clue["image"], (clue["zone"].x  - camera_x, clue["zone"].y - camera_y))
                show_clue_prompt(screen, font, player_rect, clue, camera_x, camera_y)
                if clue["show_popup"]:
                    show_popup(screen, font, clue)

        if room.check_collision(player_rect):
            
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (10, 10, 650, 50)
            )

            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (10, 10, 650, 50),
                2
            )

            if room == stairs_trigger and room.locked:
                message = "Defeat the janitor to unlock the stairs."

            elif room.locked:
                message = f"{room.message} is locked. Please find a key."

            else:
                message = room.message

            text_surface = font.render(
                message,
                True,
                (255, 255, 255)
            )

            screen.blit(text_surface, (20, 20))

    pygame.display.flip()

pygame.quit()
