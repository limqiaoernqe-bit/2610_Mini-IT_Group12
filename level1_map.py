import pygame
import pytmx
import subprocess
from gameover_system import GameOverSystem

from inventory import game_inventory as inventory, SECURITY_BADGE, ROOM116_KEY, ROOM117_KEY, ROOM116_117_CODE, EXIT_DOOR_KEY
from ghost import Ghost
from receptionist import Receptionist
from player import Player
from door import Door
from room_navigation import RoomTrigger
from weapon import L1Weapons, Weapons, use_weapon, show_prompt, draw_traps, place_salt, draw_salt, pieces_collected, unlock_sound, mw_sound, active_traps, salt_line
from inventory_bar import draw_inventory, handle_inventory_click
from object_interaction import ObjectInteraction
object_interaction = ObjectInteraction()
from puzzle_clue import ClueL1 as Clue, show_clue_prompt, show_popup, PuzzleL1, show_puzzle_prompt, puzzle_screen, handle_puzzle_input
import json
try:
    with open("save_inventory.json", "r") as f:
        save_data = json.load(f)
 
        if save_data.get("items") or save_data.get("uses"):
           
           inventory.items.clear()

           for item in save_data.get("items", []):
               inventory.items.append(item)

           for name, uses in save_data.get("uses", {}).items():
               if name in Weapons and uses is not None:
                Weapons[name]["uses"] = uses

        else:
            save_data = {}

except (FileNotFoundError, json.JSONDecodeError):
    save_data = {}

# Load level 1 save
try:
    with open("save_level1.json", "r") as f:
        level1_save = json.load(f)

except (FileNotFoundError, json.JSONDecodeError):
    level1_save = {
        "security_room_unlocked": False,
        "room116_unlocked": False,
        "room117_unlocked": False,
        "connecting_door_unlocked": False,
        "exit_door_unlocked": False,
        "receptionist_defeated": False,
        "ghost_defeated": False
    }

heart_img = pygame.image.load("assets/heart.png").convert_alpha()
heart_img = pygame.transform.scale(heart_img, (50, 50))




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

from scenes.hotelscene2 import on_mark_saved, on_james_saved, on_game_end, scene_manager

screen_width = 1280
screen_height = 720

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
mirror_img = pygame.image.load("assets/mirror.png").convert()
mirror_img = pygame.transform.scale(mirror_img, (screen_width, screen_height))
pygame.display.set_caption("Level 1")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Preload portraits for dialogues
image_dict = {
    "james_front_detailed.png": pygame.image.load("assets/james_front_detailed.png"),
    "mark_front_detailed.png": pygame.image.load("assets/mark_front_detailed.png"),
    "mia_front_detailed.png": pygame.image.load("assets/mia_front_detailed.png"),
}

# Load map
tmx_data = pytmx.load_pygame("level1_map.tmx")
TILE_SIZE = tmx_data.tilewidth

# Level 1 Collision layers
collision_layers = [
    "Collision",
    "security collision",
    "room116 collision",
    "room117 collision",
    "room116_117 collision",
    "exit collision"
]

normal_walls = []
security_walls = []
room116_walls = []
room117_walls = []
room116_117_walls = []
exit_door_walls = []

# Create collision rectangles
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

                    elif layer.name == "security collision":
                        security_walls.append(wall_rect)

                    elif layer.name == "room116 collision":
                        room116_walls.append(wall_rect)

                    elif layer.name == "room117 collision":
                        room117_walls.append(wall_rect)

                    elif layer.name == "room116_117 collision":
                        room116_117_walls.append(wall_rect)

                    elif layer.name == "exit collision":
                        exit_door_walls.append(wall_rect)


# Create player
player = Player()

game_over_system = GameOverSystem(lives=3, spawn_point=(1776, 2784))

# Receptionist spawn position
receptionist = Receptionist(
    2776, 
    1963,
    TILE_SIZE
)

# Ghost spawn position
ghost = Ghost(
    864,
    864
)

receptionist.defeat = level1_save["receptionist_defeated"]
ghost.defeat = level1_save["ghost_defeated"]

# Level 1 enemies
enemies = [
    receptionist,
    ghost
]

# Spawn position
player.x = 1776
player.y = 2784

# Level 1 Door Objects
security_door = Door(
    "Security Room",
    SECURITY_BADGE
)

room116_door = Door(
    "Room 116",
    ROOM116_KEY
)

room117_door = Door(
    "Room 117",
    ROOM117_KEY
)

room116_117_door = Door(
    "Connecting Door",
    ROOM116_117_CODE
)

exit_door = Door(
    "Exit Door",
    EXIT_DOOR_KEY
)

# Save level 1 progress
def save_level1():
    data = {
        "security_room_unlocked": not security_door.is_locked(),
        "room116_unlocked": not room116_door.is_locked(),
        "room117_unlocked": not room117_door.is_locked(),
        "connecting_door_unlocked": not room116_117_door.is_locked(),
        "exit_door_unlocked": not exit_door.is_locked(),

        "receptionist_defeated": receptionist.defeat,
        "ghost_defeated": ghost.defeat
    }

    with open("save_level1.json", "w") as f:
        json.dump(data, f, indent=4)


# Restore doors
security_door.locked = not level1_save["security_room_unlocked"]
room116_door.locked = not level1_save["room116_unlocked"]
room117_door.locked = not level1_save["room117_unlocked"]
room116_117_door.locked = not level1_save["connecting_door_unlocked"]
exit_door.locked = not level1_save["exit_door_unlocked"]

# Level 1 Room Triggers
security_room = RoomTrigger(
    pygame.Rect(2305, 2037, 48, 168),
    "Security Room",
    locked=True
)

lobby = RoomTrigger(
    pygame.Rect(2685, 2590, 33, 148),
    "Lobby"
)

receptionist_area = RoomTrigger(    
    pygame.Rect(2638, 1774, 74, 337),
    "Receptionist Area"
)

restaurant_top = RoomTrigger(
    pygame.Rect(3214, 1318, 98, 73),
    "Restaurant"
)

restaurant_bottom = RoomTrigger(
    pygame.Rect(1098, 956, 21, 148),
    "Restaurant"
)

kitchen = RoomTrigger(
    pygame.Rect(2823, 283, 34, 102),
    "Kitchen"
)

room_112 = RoomTrigger(
    pygame.Rect(1095, 2159, 29, 98),
    "Room 112"
)

room_113 = RoomTrigger(
    pygame.Rect(1088, 1533, 39, 147),
    "Room 113"
)

room_114 = RoomTrigger(
    pygame.Rect(673, 2111, 24, 96),
    "Room 114"
)

room_115 = RoomTrigger(
    pygame.Rect(672, 1582, 30, 98),
    "Room 115"
)

room_116 = RoomTrigger(
    pygame.Rect(672, 911, 55, 97),
    "Room 116",
    locked=True
)

room_117 = RoomTrigger(
    pygame.Rect(673, 238, 67, 100),
    "Room 117",
    locked=True
)

room116_117 = RoomTrigger(
    pygame.Rect(306, 622, 103, 125),
    "Connecting Door",
    locked=True
)

exit_trigger = RoomTrigger(
    pygame.Rect(3782, 2157, 57, 145),
    "Exit Door",
    locked=True
)

# Stairs back to level 2
stairs_to_level2 = RoomTrigger(
    pygame.Rect(1760, 2768, 220, 94),
    "Stairs"
)


# Static item hitboxes (keys placed at fixed map coordinates)
exit_key_rect = pygame.Rect(
    2492,
    1752,
    39,
    37
)

# james mirror puzzle code
room113_mirror_rect = pygame.Rect(
    1403,
    1352,
    110,   # width (adjust if needed)
    150    # height (adjust if needed)
)

# Key collection status
exit_key_collected = False
# Mirror status
mirror_active = False



room_triggers = [
    security_room,
    lobby,
    receptionist_area,
    restaurant_top,
    restaurant_bottom,
    kitchen,
    room_112,
    room_113,
    room_114,
    room_115,
    room_116,
    room_117,
    room116_117,
    exit_trigger,
    stairs_to_level2
]

# Draw Map function
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
active_puzzle = None

while running:

    clock.tick(60)

    # Player collision rect
    player_rect = pygame.Rect(
        player.x - 20, 
        player.y - 40,
        40,
        40
    )

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # OPEN MIRROR
            if event.key == pygame.K_r:

                if player_rect.colliderect(room113_mirror_rect):
                    mirror_active = True
                    #mirror
                    print("Mirror activated")

            # CLOSE MIRROR
            if event.key == pygame.K_ESCAPE:
                if mirror_active:
                    mirror_active = False
                
                
                # Pick up exit door key
                if (
                    player_rect.colliderect(exit_key_rect)
                    and not exit_key_collected
                ):
                    inventory.add_item(EXIT_DOOR_KEY)
                    exit_key_collected = True


                # Go back to level 2                
                if stairs_to_level2.check_collision(player_rect):
                    print("Going back to Level 2...")

                    # Close level 1 and open level 2
                    save_level1()

                    save_data = {
                        "items": inventory.items,
                        "uses": {
                            name: Weapons[name].get("uses", None)
                            for name in inventory.items
                            if name in Weapons
                        }
                    }

                    with open("save_inventory.json", "w") as f:
                        json.dump(save_data, f)

                    pygame.quit()
                    subprocess.run(["python", "level2_map.py", "stairs"])
                    running = False
                else:                
                    object_interaction.try_interact(player_rect)

                # puzzle
                if player_rect.colliderect(PuzzleL1["KeyArea"]["zone"]):
                    PuzzleL1["KeyArea"]["active"] = True
                    active_puzzle = PuzzleL1["KeyArea"]
        
                # clue 
                for clue in Clue.values():
                    if clue["show_prompt"] and clue ["active"]:
                        clue["show_popup"] = True
                        clue["active"] = False
            if event.key == pygame.K_c:
                for clue in Clue.values():
                    if clue ["show_popup"]:
                        clue["show_popup"] = False

            # close puzzle when C
            if event.key == pygame.K_c and active_puzzle and active_puzzle["active"]:
                active_puzzle["active"] = False

            if active_puzzle and active_puzzle["active"]:
                handle_puzzle_input(event, active_puzzle, inventory, object_interaction)

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

        if event.type == pygame.KEYDOWN:

        # Collect Weapons
           if event.key == pygame.K_r:
              weapon_collected = False
              for name, weapon in Weapons.items():
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
              if not weapon_collected:
                    object_interaction.try_interact(player_rect)        

                    if player_rect.colliderect(PuzzleL1["KeyArea"]["zone"]) and not PuzzleL1["KeyArea"]["collected"]:
                       PuzzleL1["KeyArea"]["active"] = True
                       active_puzzle = PuzzleL1["KeyArea"]

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
                    if player.held_weapon == "Salt":
                       salt_rect = pygame.Rect(player.x - 50, player.y, 100, 13)
                       salt_line.append({"rect": salt_rect, 
                                      "placed_time": pygame.time.get_ticks()})                        


    # Player Movement
    if game_over_system.is_game_over():
        keys = None
    else:
        keys = pygame.key.get_pressed()

    # Active collision walls
    active_walls = normal_walls.copy()

    if security_door.is_locked():
        active_walls += security_walls

    if room116_door.is_locked():
        active_walls += room116_walls

    if room117_door.is_locked():
        active_walls += room117_walls

    if room116_117_door.is_locked():
        active_walls += room116_117_walls

    if exit_door.is_locked():
        active_walls += exit_door_walls

            # Player Movement
    if game_over_system.is_game_over():
        keys = None
    else:
        keys = pygame.key.get_pressed()
    
    if not game_over_system.is_game_over():
        keys = pygame.key.get_pressed()
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

    

    # Move recepionist and ghost
    if not game_over_system.is_game_over():
        if not receptionist.defeat:
           receptionist.update(
            player.x,
            player.y,
            blocked,
            active_walls,
        )

    # Move ghost
    if not ghost.defeat:
       ghost.update(
        player.x,
        player.y
    )

    # GAME OVER CHECK (ghost collision)
    ghost_rect = pygame.Rect(
    ghost.x - 40,
    ghost.y - 40,
    80,
    80
    )

    receptionist_rect = pygame.Rect(
        receptionist.x - 20,
        receptionist.y - 40,
        40,
        40
    )

    if not game_over_system.is_game_over():

        if not ghost.defeat and ghost_rect.colliderect(player_rect):
            game_over_system.on_caught(player)

    if not receptionist.defeat and receptionist.rect.colliderect(player_rect):
        game_over_system.on_caught(player)

    # Give Exit Key after both enemies are defeated
    if(
        receptionist.defeat
        and ghost.defeat
        and EXIT_DOOR_KEY not in inventory.items
    ):
        inventory.add_item(EXIT_DOOR_KEY)

        pop_up_message = "You got the Exit Key!"
        weapon_popup = True
        popup_start_time = pygame.time.get_ticks()

        save_level1()  # Save after defeating enemies and getting the exit key

    # Camera System
    camera_x = player.x - screen_width // 2
    camera_y = player.y - screen_height // 2

    # Draw everything
    screen.fill((0, 0, 0))

    # Draw map
    draw_map(screen, camera_x, camera_y)

    # Draw receptionist
    if not receptionist.defeat:
       receptionist.draw(
        screen,
        camera_x,
        camera_y
    )

    # Draw ghost
    if not ghost.defeat:
       ghost.draw(
        screen,
        camera_x,
        camera_y
    )
    for enemy in [receptionist, ghost]:
        if hasattr(enemy, "popup_message") and enemy.popup_message:
            if pygame.time.get_ticks() - enemy.popup_start_time < enemy.popup_duration:
               popup_rect = pygame.Rect(400, 300, 300, 100)
               pygame.draw.rect(screen, (255,255,255), popup_rect)
               pygame.draw.rect(screen, (0,0,0), popup_rect, 2)
               text_surface = font.render(enemy.popup_message, True, (0,0,0))
               text_rect = text_surface.get_rect(center=popup_rect.center)
               screen.blit(text_surface, text_rect)
            else:
               enemy.popup_message = None  

    # Draw player 
    player.draw(screen, camera_x, camera_y)

    for i in range(game_over_system.lives):
        screen.blit(heart_img, (20 + i * 55, 20))

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
    for name, weapon in L1Weapons.items():
        if weapon["zone"] is not None and not weapon["collected"]:
            screen.blit(weapon["image"],( weapon["zone"].x - camera_x, weapon["zone"].y - camera_y))
        show_prompt(screen, font, player_rect, weapon, camera_x, camera_y)

    # draw use weapon
    draw_traps(screen, camera_x, camera_y)
    #removed salt lines aftrer 40 seconds
    current_time = pygame.time.get_ticks()
    salt_line[:] = [s for s in salt_line if current_time - s["placed_time"] < 40000]
    for salt in salt_line:
        screen_rect = pygame.Rect(
            salt["rect"].x - camera_x,
            salt["rect"].y - camera_y,
            salt["rect"].width,
            salt["rect"].height 
        )
        pygame.draw.rect(screen, (255, 255, 255), screen_rect)

        # draw inventory
    draw_inventory(screen, inventory, Weapons, object_interaction, screen_width, screen_height)

            # puzzle prompt
    show_puzzle_prompt(screen,font, PuzzleL1["KeyArea"], PuzzleL1["KeyArea"]["zone"].centerx, PuzzleL1["KeyArea"]["zone"].centery,camera_x, camera_y)

    if active_puzzle and active_puzzle["active"]:
        puzzle_screen(active_puzzle, screen, font, screen_width, screen_height)

    if active_puzzle and active_puzzle["collected"]:
        if pygame.time.get_ticks() - active_puzzle.get("correct_start", 0) > 3000:  # Show message for 3 seconds
            active_puzzle["active"] = False

            # clue go_to_
    for clue in Clue.values():
        if not (active_puzzle and active_puzzle["active"]):
            if "image" in clue:
                screen.blit(clue["image"], (clue["zone"].x  - camera_x, clue["zone"].y - camera_y))
            show_clue_prompt(screen, font, player_rect, clue, camera_x, camera_y)

        if clue["show_popup"]:
            show_popup(screen, font, clue)


    # Show R interaction prompt above stairs
    if stairs_to_level2.check_collision(player_rect):

        text = font.render("R", True, (0, 0, 0))

        text_rect = text.get_rect(
            center = (
                stairs_to_level2.rect.centerx - camera_x,
                stairs_to_level2.rect.y - camera_y - 20
            )
        )

        screen.blit(text, text_rect)

    # Press E to unlock Security Room
    if security_room.check_collision(player_rect):
        
        if keys[pygame.K_e]:
            inventory.use_item(
                SECURITY_BADGE,
                security_door
            )

            # save after unlocking security room
            save_level1()

    # Press E to unlock Room 116 (Mark's room)
    if room_116.check_collision(player_rect):
        
        if(
            ROOM116_KEY in inventory.items
            and keys[pygame.K_e] 
            and room116_door.is_locked()
        ):
            inventory.use_item(
                ROOM116_KEY,
                room116_door
            )

            # save after unlocking room 116
            save_level1()

            # Trigger Mark's cutscene
            on_mark_saved()

    # Press E to unlock Room 117 (James's room)
    if room_117.check_collision(player_rect):
        
        if(
            ROOM117_KEY in inventory.items
            and keys[pygame.K_e] 
            and room117_door.is_locked()
        ):
            inventory.use_item(
                ROOM117_KEY,
                room117_door
            )

            # save after unlocking room 117
            save_level1()

            # Trigger James's cutscene
            on_james_saved()

     # Press E to unlock Connecting Door
    if room116_117.check_collision(player_rect):
        
        if(
            ROOM116_117_CODE in inventory.items
            and keys[pygame.K_e]
        ):
            inventory.use_item(
                ROOM116_117_CODE,
                room116_117_door
            )

            save_level1()

    # Press E to unlock Exit Door
    if exit_trigger.check_collision(player_rect):
        
        if(
            EXIT_DOOR_KEY in inventory.items
            and keys[pygame.K_e] 
            and exit_door.is_locked()
        ):
            inventory.use_item(
                EXIT_DOOR_KEY,
                exit_door
            )


            save_level1()

    # Sync trigger status with door status
    security_room.locked = security_door.is_locked()
    room_116.locked = room116_door.is_locked()
    room_117.locked = room117_door.is_locked()
    room116_117.locked = room116_117_door.is_locked()
    exit_trigger.locked = exit_door.is_locked()

    # Room labels
    for room in room_triggers:

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

            if room == room116_117 and room.locked:
                message = "The door is locked. Please input a code to unlock."

            elif room == security_room and room.locked:

                if SECURITY_BADGE in inventory.items:
                    message = "Security Room is locked. Press E to unlock."
                else:
                    message = "Security Room is locked. Find a Security Badge."

            elif room == room_116 and room.locked:
                if ROOM116_KEY in inventory.items:
                    message = "Room 116 is locked. Press E to unlock."
                else:
                    message = "Room 116 is locked. Please find the Room 116 key."

            elif room == exit_trigger and room.locked:

                if EXIT_DOOR_KEY in inventory.items:
                    message = "The exit is locked. Press E to unlock."
                else:
                    message = "The exit is locked. Please find the exit key to escape."

            elif room == stairs_to_level2:
                message = "Press R to return to Level 2"

            elif room.locked:
                message = f"{room.message} is locked."

            else:
                message = room.message

            text_surface = font.render(
                message,
                True,
                (255, 255, 255)
            )
            
            screen.blit(text_surface, (20, 20))

    object_interaction.draw(screen)

    # Draw dialogue cutscenes if active
    scene_manager.draw(screen, font, image_dict)

    if game_over_system.is_game_over():

        game_over_system.draw(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                result = game_over_system.handle_click(event.pos, player, inventory, Weapons, object_interaction, PuzzleL1, Clue)

                if result == "retry":
                    player.x, player.y = game_over_system.spawn_point

                elif result == "quit":
                    pygame.quit()
                    subprocess.run(["python3", "main.py"])
                    exit()

        pygame.display.flip()
        continue
# mirror
    if player_rect.colliderect(room113_mirror_rect):
       
        text = font.render("R", True, (0, 0, 0))
        text_rect = text.get_rect(
            center=(
                room113_mirror_rect.centerx - camera_x,
                room113_mirror_rect.y - camera_y + 10
            )
        )
        screen.blit(text, text_rect)

    # MIRROR MODE (PAUSES GAME RENDER)
    if mirror_active:
        screen.blit(mirror_img, (0, 0))

        text = font.render("Press ESC to close", True, (0, 0, 0))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height - 40))
        screen.blit(text, text_rect)

        pygame.display.flip()
        continue

    pygame.display.flip()

pygame.quit()