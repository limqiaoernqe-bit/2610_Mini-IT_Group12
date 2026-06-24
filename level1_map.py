import pygame
import pytmx
import subprocess

from inventory import game_inventory as inventory
from ghost import Ghost
from receptionist import Receptionist
from weapon import barricade
from player import Player
from door import Door
from room_navigation import RoomTrigger
from weapon import L1Weapons, Weapons, use_weapon, show_prompt, draw_traps, place_salt, draw_salt, pieces_collected, unlock_sound, mw_sound, active_traps
from inventory_bar import draw_inventory, handle_inventory_click
from object_interaction import ObjectInteraction
object_interaction = ObjectInteraction()

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
pygame.display.set_caption("Level 1")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

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

# Receptionist spawn position
receptionist = Receptionist(
    2592,
    1872
)

# Ghost spawn position
ghost = Ghost(
    864,
    864
)
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

room_114 = RoomTrigger(
    pygame.Rect(1095, 2159, 29, 98),
    "Room 114"
)

room_113 = RoomTrigger(
    pygame.Rect(673, 2111, 24, 96),
    "Room 113"
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
    pygame.Rect(336, 572, 50, 49),
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

# Key collection status
exit_key_collected = False

room_triggers = [
    security_room,
    lobby,
    receptionist_area,
    restaurant_top,
    restaurant_bottom,
    kitchen,
    room_114,
    room_113,
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
            if event.key == pygame.K_r:
                
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
                    pygame.quit()
                    subprocess.run(["python", "level2_map.py.py", "stairs"])
                    running = False
                
                    object_interaction.try_interact(player_rect)


    
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

        if event.type == pygame.KEYDOWN:

        # Collect Weapons
           if event.key == pygame.K_r:
              for name, weapon in L1Weapons.items():
                if weapon["zone"] is not None and player_rect.colliderect(weapon["zone"]) and not weapon["collected"]:
                    weapon["collected"] = True
                    Weapons[name]["collected"] = True
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

    player.update(keys, active_walls)

    # Move recepionist
    receptionist.update(
    player.x,
    player.y,
    active_walls,
    barricade
    )

    # Move ghost
    ghost.update(
        player.x,
        player.y
    )

    # Camera System
    camera_x = player.x - SCREEN_WIDTH // 2
    camera_y = player.y - SCREEN_HEIGHT // 2

    # Draw everything
    screen.fill((0, 0, 0))

    # Draw map
    draw_map(screen, camera_x, camera_y)

    # Draw receptionist
    receptionist.draw(
        screen,
        camera_x,
        camera_y
    )

    # Draw ghost
    ghost.draw(
        screen,
        camera_x,
        camera_y
    )

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
    for name, weapon in L1Weapons.items():
        if weapon["zone"] is not None and not weapon["collected"]:
            screen.blit(weapon["image"],( weapon["zone"].x - camera_x, weapon["zone"].y - camera_y))
        show_prompt(screen, font, player_rect, weapon, camera_x, camera_y)

    # draw use weapon
    draw_traps(screen, camera_x, camera_y)
    draw_salt(screen, camera_x, camera_y)

        # draw inventory
    draw_inventory(screen, inventory, Weapons, object_interaction, SCREEN_HEIGHT, SCREEN_WIDTH)

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

    # Press E to unlock Room 116
    if room_116.check_collision(player_rect):
        
        if keys[pygame.K_e]:
            inventory.use_item(
                ROOM116_KEY,
                room116_door
            )

    # Press E to unlock Room 117
    if room_117.check_collision(player_rect):
        
        if keys[pygame.K_e]:
            inventory.use_item(
                ROOM117_KEY,
                room117_door
            )

     # Press E to unlock Connecting Door
    if room116_117.check_collision(player_rect):
        
        if keys[pygame.K_e]:
            inventory.use_item(
                ROOM116_117_CODE,
                room116_117_door
            )

    # Press E to unlock Exit Door
    if exit_trigger.check_collision(player_rect):
        
        if keys[pygame.K_e]:
            inventory.use_item(
                EXIT_DOOR_KEY,
                exit_door
            )

    # Sync trigger status with door status
    security_room.locked = security_door.is_locked()
    room_116.locked = room116_door.is_locked()
    room_117.locked = room117_door.is_locked()
    room116_117.locked = room116_117_door.is_locked()
    exit_trigger.locked = exit_door.is_locked()

    # Ending scene after exit the place
        



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
                message = "Security Room is locked. Find a Security Badge."

            elif room == exit_trigger and room.locked:
                message = "The exit is locked. Please find the exit key to escape."

            elif room == stairs_to_level2:
                message = "Press R to return to Level 2"

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

    object_interaction.draw(screen)

    pygame.display.flip()

pygame.quit()