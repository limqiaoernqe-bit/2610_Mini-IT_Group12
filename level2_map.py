import pygame
import pytmx

# Used to open level 1 after player reaches the stairs
import subprocess

import json
import sys

from inventory import game_inventory as inventory, ROOM_210_KEY, ROOM_206_KEY, JANITOR_KEY, SECURITY_BADGE, BOLT_CUTTER
from player import Player
from room_navigation import RoomTrigger
from door import Door
from puzzle_clue import Puzzle, ClueL2 as Clue, show_puzzle_prompt, show_clue_prompt, show_popup, puzzle_screen, handle_puzzle_input 
from weapon import L2Weapons, Weapons, use_weapon, show_prompt, draw_traps, place_salt, draw_salt, pieces_collected, unlock_sound, mw_sound, active_traps
from inventory_bar import draw_inventory, handle_inventory_click 
from janitor import Janitor
from object_interaction import ObjectInteraction
from scenes.hotelscene2 import on_chloe_saved, on_jay_saved, scene_manager
from gameover_system import GameOverSystem
from reset_save import reset_game

game_over_system = GameOverSystem(lives=3, spawn_point=(2160, 2160))  # maintenance room
heart_img = pygame.image.load("assets/heart.png").convert_alpha()
heart_img = pygame.transform.scale(heart_img, (50, 50))


# Weapon Popup system
weapon_popup = False
popup_start_time = 0
popup_duration = 1
popup_message = ""
main_weapon_unlocked = False
main_weapon_popup_shown = False

hint_popup = False
hint_popup_message = ""
hint_popup_start_time = 0
hint_popup_duration = 3000      # milliseconds

retry_mode = False

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

screen_width = 1280
screen_height = 720

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Level 2")

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
object_interaction = ObjectInteraction()

#Load inventory from save file
try:
    with open("save_inventory.json", "r") as f:
        save_data = json.load(f)

        inventory.items.clear()

        for item in save_data.get("items", []):
            inventory.items.append(item)

        for weapon_name, uses in save_data.get("uses", {}).items():
            if weapon_name in Weapons:
                Weapons[weapon_name]["uses"] = uses

        # Restore collected status
        for weapon_name, collected in save_data.get("collected", {}).items():
            if weapon_name in Weapons:
                Weapons[weapon_name]["collected"] = collected
            if weapon_name in L2Weapons:
                L2Weapons[weapon_name]["collected"] = collected

except (FileNotFoundError, json.JSONDecodeError):
    pass

# Preload portraits for dialogues
image_dict = {
    "chloe_front_detailed.png": pygame.image.load("assets/chloe_front_detailed.png"),
    "jay_front_detailed.png": pygame.image.load("assets/jay_front_detailed.png"),
    "mia_front_detailed.png": pygame.image.load("assets/mia_front_detailed.png"),
}

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
    2976,
    960,
    TILE_SIZE
)

enemies = [janitor]

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
    locked = True
)

# Load Level 2 save
try:
    with open("save_level2.json", "r") as f:
        level2_save = json.load(f)

except (FileNotFoundError, json.JSONDecodeError):
    level2_save = {
        "room206_unlocked": False,
        "room210_unlocked": False,
        "janitor_room_unlocked": False,
        "janitor_defeated": False,
        "stairs_unlocked": False,

        "room210_key_collected": False,
        "janitor_key_collected": False,
        "security_badge_collected": False,

        "locker_unlocked": False
    }

# Restore doors
room206_door.locked = not level2_save["room206_unlocked"]
room210_door.locked = not level2_save["room210_unlocked"]
janitor_door.locked = not level2_save["janitor_room_unlocked"]

# Restore janitor state
janitor.defeat = level2_save["janitor_defeated"]

# Restore stairs state
stairs_trigger.locked = not level2_save["stairs_unlocked"]

# Restore locker state
locker_unlocked = level2_save.get("locker_unlocked", False)

# Restore collected objects
object_interaction.zones["toolbox"]["collected"] = level2_save.get(
    "toolbox_collected",
    False
)

object_interaction.zones["stool"]["collected"] = level2_save.get(
    "stool_collected",
    False
)

object_interaction.zones["box"]["collected"] = level2_save.get(
    "box_collected",
    False
)

object_interaction.zones["locker"]["collected"] = level2_save.get(
    "locker_collected",
    False
)

Puzzle["Treadmill"]["collected"] = level2_save.get(
    "treadmill_completed",
    False
)

# Save Level 2 progress
def save_level2():
    data = {
        "room206_unlocked": not room206_door.is_locked(),
        "room210_unlocked": not room210_door.is_locked(),
        "janitor_room_unlocked": not janitor_door.is_locked(),
        "janitor_defeated": janitor.defeat,
        "stairs_unlocked": not stairs_trigger.locked,
        
        "room210_key_collected": room210_key_collected,
        "janitor_key_collected": janitor_key_collected,
        "security_badge_collected": security_badge_collected,

        "locker_unlocked": locker_unlocked,

        "toolbox_collected": object_interaction.zones["toolbox"]["collected"],
        "stool_collected": object_interaction.zones["stool"]["collected"],
        "box_collected": object_interaction.zones["box"]["collected"],
        "locker_collected": object_interaction.zones["locker"]["collected"],

        "treadmill_completed": Puzzle["Treadmill"]["collected"]
    }

    with open("save_level2.json", "w") as f:
        json.dump(data, f, indent=4)

# Spawn position logic

# Default when first playing
spawn_mode = "maintenance"

# Coming back from level 1
try:
    if len (sys.argv) > 1:
        spawn_mode = sys.argv[1]
except:
    pass

if spawn_mode == "maintenance":
    player.x = 2160
    player.y = 2160
elif spawn_mode == "stairs":
    # Place the player right at the stairs trigger
    player.x = 2589
    player.y = 2765

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
# Restore collected items
room210_key_collected = level2_save.get("room210_key_collected", False)
janitor_key_collected = level2_save.get("janitor_key_collected", False)
security_badge_collected = level2_save.get("security_badge_collected", False)
object_interaction.zones["locker"]["collected"] = security_badge_collected

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
go_to_level1 = False

while running:

    clock.tick(60)

    # Camera System
    camera_x = player.x - screen_width // 2
    camera_y = player.y - screen_height // 2

    # Player collision rect
    player_rect = pygame.Rect(
        player.x - 30,
        player.y - 60,
        60,
        60
    )  

    # Events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            result = game_over_system.handle_click(event.pos, player, inventory, Weapons, object_interaction, Puzzle, Clue)

            if result == "retry":
                retry_mode = True
                reset_game() # reset all save files and restart the game
                pygame.quit()  # close current window game
                subprocess.run(["python", "level2_map.py"])  # restart level 2 
                sys.exit()  # exit the current script

            elif result == "quit":
                reset_game() # reset all save files and restart the game
                pygame.quit()
                import sys
                subprocess.run([sys.executable, "main.py"])
                sys.exit()
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:

                # Open puzzle
                if(
                    player_rect.colliderect(Puzzle["Treadmill"]["zone"])
                    and not Puzzle["Treadmill"]["collected"]    
                ):
                    Puzzle["Treadmill"]["active"] = True

                # Pick up Room 210 Key
                elif (
                    player_rect.colliderect(room210_key_rect)
                    and not room210_key_collected
                ):
                    inventory.add_item(ROOM_210_KEY)
                    room210_key_collected = True
                    save_level2()  # Save after picking up the key

                # Pick up Janitor Key
                elif (
                    player_rect.colliderect(janitor_key_rect)
                    and not janitor_key_collected
                ):
                    inventory.add_item(JANITOR_KEY)
                    janitor_key_collected = True
                    save_level2()  # Save after picking up the key
                    
                # Pick up Security Badge
                elif (
                    player_rect.colliderect(object_interaction.zones["locker"]["zone"])
                    and locker_unlocked
                    and not security_badge_collected
                ):
                    # Show obtained popup
                    object_interaction.trigger(SECURITY_BADGE)
                    security_badge_collected = True
                    object_interaction.zones["locker"]["collected"] = True
                    save_level2()  # Save after picking up the key

                # Go to level 1 after stairs are unlocked
                elif stairs_trigger.check_collision(player_rect):
                    if not stairs_trigger.locked:
                        print("Going to Level 1...")
                        # Close level 2 and open level 1

                        # save inventory before quitting
                        import json
                        if not retry_mode: 
                            save_data = {
                                "items": inventory.items,
                                "uses": {
                                    name: Weapons[name].get("uses", None)
                                    for name in Weapons
                                },
                                "collected":{
                                    name: Weapons[name]["collected"]
                                    for name in Weapons
                                }
                            }
                            with open("save_inventory.json", "w") as f:
                                 json.dump(save_data, f)

                        save_level2()

                        go_to_level1 = True
                        running = False
                        break
                    else:
                        print("The stairs are locked. Find a way to unlock them.")

                # Object interaction
                else: 
                    object_interaction.try_interact(
                        player_rect
                    )
                
            if event.key == pygame.K_ESCAPE:
                object_interaction.hide()

            # close puzzle when press C
            if event.key == pygame.K_c and active_puzzle and active_puzzle["active"]:
                active_puzzle["active"] = False

            if event.key == pygame.K_SPACE:
                scene_manager.update()

        # to find coordinates
        if event.type == pygame.MOUSEBUTTONDOWN:
            world_x = event.pos[0] + camera_x
            world_y = event.pos[1] + camera_y
            print(f"World Coordinates: ({world_x}, {world_y})")

            mouse_x, mouse_y = event.pos
            for i, weapon_name in enumerate(inventory.items):
                rect = pygame.Rect(50 + i*60, screen_height-60, 50, 50)
                if rect.collidepoint(mouse_x, mouse_y):
                   selected_index = i

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            handle_inventory_click(event.pos, player, inventory, screen_height)
        # puzzle 
        if active_puzzle and active_puzzle["active"]:
            handle_puzzle_input(event, active_puzzle, inventory, object_interaction)

        # Save immediately after the puzzle is completed
        if active_puzzle and active_puzzle["collected"]:
            save_level2()  # Save after completing the puzzle

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
                weapon_collected = False
                for name, weapon in L2Weapons.items():
                    if weapon["zone"] is not None and player_rect.colliderect(weapon["zone"]) and not weapon["collected"]:
                        weapon["collected"] = True
                        Weapons[name]["collected"] = True
                        unlock_sound.play()
                        inventory.add_item(name)
                        weapon_collected = True

                        if pieces_collected() == 3 and not main_weapon_unlocked:
                            main_weapon_unlocked = True
                            Weapons["MWfull"]["collected"] = True
                            for piece in ["MWpiece1", "MWpiece2", "MWpiece3"]:
                                if piece in inventory.items:
                                    inventory.remove_item(piece)
                            inventory.add_item("MWfull")
                            main_weapon_popup_shown = True
                            popup_start_time = pygame.time.get_ticks()
                            mw_sound.play()
                        else:
                            weapon_popup = True
                            popup_start_time = pygame.time.get_ticks()
                            popup_message = weapon["popup_text"]

                        break

                if not weapon_collected:
                    object_interaction.try_interact(player_rect)

                        # Use currectly selected weapons
            if event.key == pygame.K_w:
                if event.key == pygame.K_w and player.held_weapon:
                    use_weapon(
                        player.held_weapon,
                        player,
                        player_rect,
                        enemies,
                        player.direction,
                        inventory
                    )

    # Player Movement
    # STOP GAME IF GAME OVER
    if game_over_system.is_game_over():
        keys = None
    else:
        keys = pygame.key.get_pressed()

    # Active collision walls
    active_walls = normal_walls.copy()

    if stairs_trigger.locked:
        active_walls += stairs_walls

    # Locked room walls    
    if room210_door.is_locked():
        active_walls += room210_walls

    if janitor_door.is_locked():
        active_walls += janitor_walls

    if room206_door.is_locked():
        active_walls += room206_walls

    # Move player
    if keys is not None:
        player.update(keys, active_walls)

    # Convert collision rectangles into blocked grid tiles
    blocked = set()

    for wall in active_walls:
        
        left = wall.left // TILE_SIZE
        right = (wall.right - 1) // TILE_SIZE

        top = wall.top // TILE_SIZE
        bottom = (wall.bottom- 1) // TILE_SIZE

        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                blocked.add((x, y))

    # Now pass blocked instead of active_walls
    if not janitor.defeat:
       janitor.update(
        player.x, 
        player.y,
        blocked,
        active_walls,
        )



    # GAME OVER CHECK (janitor collision)
    if not janitor.defeat and janitor.rect.colliderect(player_rect):
        game_over_system.on_caught(player)


    # Unlock stairs when janitor is defeated
    if janitor.defeat:
        if stairs_trigger.locked:
            stairs_trigger.locked = False
            save_level2()

    # ===========================
    # GAME OVER SCREEN
    # ===========================
    if game_over_system.is_game_over():

        game_over_system.draw(screen)

        # handle events (NO pygame.event.get() here)
        mouse_clicked = False
        mouse_pos = (0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
                mouse_pos = event.pos

        if mouse_clicked:
            result = game_over_system.handle_click(mouse_pos, player, inventory, Weapons, object_interaction, Puzzle, Clue)

            if result == "retry":
                retry_mode = True
                reset_game()
                pygame.quit()
                subprocess.run([sys.executable, "level2_map.py"])
                sys.exit()

            elif result == "quit":
                pygame.quit()
                import sys

                subprocess.run([sys.executable, "main.py"])
                exit()

        pygame.display.flip()
        continue

    # Draw everything
    screen.fill((0, 0, 0))

    # Draw map
    draw_map(screen, camera_x, camera_y)

    # Draw Janitor
    if not janitor.defeat:
       janitor.draw(screen, camera_x, camera_y)

    # Draw player 
    player.draw(screen, camera_x, camera_y)

    for i in range(game_over_system.lives):
        screen.blit(heart_img, (20 + i * 35,20))

# WEAPON PART
    # hide popup
    if weapon_popup and (pygame.time.get_ticks()- popup_start_time > popup_duration * 5000):
        weapon_popup = False

        # Effect when main weapon shows
    if weapon_popup or (main_weapon_unlocked and main_weapon_popup_shown):
        dark_overlay = pygame.Surface((screen_width, screen_height))
        dark_overlay.set_alpha(180) # darkens the bg and makes the weapon stands out 
        dark_overlay.fill((0,0,0))
        screen.blit(dark_overlay, (0,0))

        # popup box
    if weapon_popup:
        popup_width = 400
        popup_height = 200
        popup_x =(screen_width - popup_width) //2 
        popup_y = (screen_height - popup_height) //2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

            #draw popup box
        pygame.draw.rect(screen, (255,255,255), popup_rect)
        pygame.draw.rect(screen, (153, 204, 255), popup_rect, 2)
        draw_text(screen, popup_message, popup_rect, font, (0,0,0))

    if main_weapon_unlocked and main_weapon_popup_shown:
        MWimage = Weapons["MWfull"]["image"]
        MW_rect = MWimage.get_rect(center=(screen_width//2, screen_height//2))
        screen.blit(MWimage, MW_rect)

        if pygame.time.get_ticks() - popup_start_time > 1000:
            main_weapon_popup_shown = False
            weapon_popup = True
            popup_start_time = pygame.time.get_ticks()
            popup_message = Weapons["MWfull"]["popup_text"]

    # Draw image of weapons
    for name, weapon in L2Weapons.items():
        if weapon["zone"] is not None and not weapon["collected"]:
            screen.blit(weapon["image"],( weapon["zone"].x - camera_x, weapon["zone"].y - camera_y))
        show_prompt(screen, font, player_rect, weapon, camera_x, camera_y)

    # draw use weapon
    draw_traps(screen, camera_x, camera_y)
    draw_salt(screen, camera_x, camera_y)

    # show R for objects when not picked
    for name, data in object_interaction.zones.items():
        zone = data["zone"]
        collected = data.get("collected", False)

        # Don't show R on the locker until it's unlocked
        if name == "locker":
            if not locker_unlocked:
                continue

            if security_badge_collected:
                continue

        object_interaction.show_object_prompt(screen, font, zone, player_rect, camera_x, camera_y, collected)    

        # draw inventory
    draw_inventory(screen, inventory, Weapons, object_interaction, screen_width, screen_height)
        
        
    # Show R interaction prompt for level 1 stairs
    if stairs_trigger.check_collision(player_rect):

        if not stairs_trigger.locked:
            text = font.render("R", True, (0, 0, 0))

            text_rect = text.get_rect(
                center = (
                    stairs_trigger.rect.centerx - camera_x,
                    stairs_trigger.rect.y - camera_y - 20
                )
            )

            screen.blit(text, text_rect)

    # Press E to unlock Room 210 (Jay's room)
    if room_210.check_collision(player_rect):

        # Only try to unlock if the player actually has the key
        if (
            ROOM_210_KEY in inventory.items
            and keys[pygame.K_e]
            and room210_door.is_locked()
        ):
            inventory.use_item(
                ROOM_210_KEY,
                room210_door
            )

            save_level2()

            # Trigger Jay's cutscene
            on_jay_saved()

    # Press E to unlock Janitor Room
    if janitor_room.check_collision(player_rect):
        
        if (
            JANITOR_KEY in inventory.items
            and keys[pygame.K_e]
            and janitor_door.is_locked()
        ):
            inventory.use_item(
                JANITOR_KEY,
                janitor_door
            )

            save_level2()

            hint_popup = True
            hint_popup_message = "There's something in the locker..."
            hint_popup_start_time = pygame.time.get_ticks()

    # Press E to unlock Locker
    locker_zone = object_interaction.zones["locker"]["zone"]

    if player_rect.colliderect(locker_zone):
        if (
            BOLT_CUTTER in inventory.items
            and keys[pygame.K_e]
            and not locker_unlocked
        ):
            inventory.remove_item(BOLT_CUTTER)

            locker_unlocked = True

            save_level2()
    
    # Press E to unlock Room 206 (Chloe's room)
    if room_206.check_collision(player_rect):
        
        if (
            ROOM_206_KEY in inventory.items
            and keys[pygame.K_e]
            and room206_door.is_locked()
        ):
            inventory.use_item(
                ROOM_206_KEY,
                room206_door
            )

            save_level2()

            # Trigger Chloe's cutscene
            on_chloe_saved()

    # Sync trigger status with door status
    room_210.locked = room210_door.is_locked()
    janitor_room.locked = janitor_door.is_locked()
    room_206.locked = room206_door.is_locked()

    # Room labels
    for room in room_triggers:

        # puzzle trigger 
        treadmill_puzzle = Puzzle["Treadmill"]

        if not treadmill_puzzle["collected"]:
            if player_rect.colliderect(treadmill_puzzle["zone"]):
                if keys[pygame.K_r]:
                    treadmill_puzzle["active"] = True
                    active_puzzle = treadmill_puzzle

            # puzzle prompt
        show_puzzle_prompt(screen,font, player_rect, treadmill_puzzle, treadmill_puzzle["zone"].centerx, treadmill_puzzle["zone"].centery, camera_x, camera_y)

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
                
                # Room 210
                if room == room_210:
                    if ROOM_210_KEY in inventory.items:
                        message = "Room 210 is locked. Press E to unlock."
                    else:
                        message = "Room 210 is locked. Please find the Room 210 key."

                # Room 206
                elif room == room_206:
                    if ROOM_206_KEY in inventory.items:
                        message = "Room 206 is locked. Press E to unlock."
                    else:
                        message = "Room 206 is locked. Please find the Room 206 key."

                # Janitor room
                elif room == janitor_room:
                    if JANITOR_KEY in inventory.items:
                        message = "Janitor Room is locked. Press E to unlock."
                    else:
                        message = "Janitor Room is locked. Please find the Janitor key."

            else:
                message = room.message

            text_surface = font.render(
                message,
                True,
                (255, 255, 255)
            )

            screen.blit(text_surface, (20, 20))

    # Locker message
    locker_zone = object_interaction.zones["locker"]["zone"]

    if player_rect.colliderect(locker_zone):

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

        if not locker_unlocked:
            if BOLT_CUTTER in inventory.items:
                message = "Locker is locked. Press E to unlock."
            else:
                message = "Locker is locked. Please find the bolt cutter."
        else:
            if not security_badge_collected:
                message = "Press R to collect the Security Badge."
            else:
                message = "Locker is empty."

        text_surface = font.render(
            message,
            True,
            (255, 255, 255)
        )

        screen.blit(text_surface, (20, 20))

    object_interaction.draw(screen)

    # Draw dialogue cutscenes if active
    scene_manager.draw(screen, font, image_dict)

    # Show janitor popup if active
    if hasattr(janitor, "popup_message") and janitor.popup_message:
        if pygame.time.get_ticks() - janitor.popup_start_time < janitor.popup_duration:
            popup_width = 600
            popup_height = 150
            popup_x = (screen_width - popup_width) // 2
            popup_y = (screen_height - popup_height) // 2
            popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

            pygame.draw.rect(screen, (255,255,255), popup_rect)
            pygame.draw.rect(screen, (0,0,0), popup_rect, 2)

            text_surface = font.render(janitor.popup_message, True, (0,0,0))
            text_rect = text_surface.get_rect(center=popup_rect.center)
            screen.blit(text_surface, text_rect)
        else:
            janitor.popup_message = None

    # Locker hint popup
    if hint_popup:
        if pygame.time.get_ticks() - hint_popup_start_time < hint_popup_duration:
            popup_width = 500
            popup_height = 120
            popup_x = (screen_width - popup_width) // 2
            popup_y = 80
            popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

            pygame.draw.rect(screen, (255,255,255), popup_rect)
            pygame.draw.rect(screen, (0,0,0), popup_rect, 3)

            text = font.render(hint_popup_message, True, (0,0,0))
            text_rect = text.get_rect(center=popup_rect.center)
            screen.blit(text, text_rect)
        else:
            hint_popup = False

    pygame.display.flip()

pygame.quit()

if go_to_level1:
    subprocess.run([sys.executable, "level1_map.py", "stairs"])