import pygame
import pytmx

from player import Player
from room_navigation import RoomTrigger

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

#Collision layers
collision_layers = [
    "Collision",
    "stairs collision",
    "rooms collision"
]

walls = []

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

                    walls.append(wall_rect)

# Create Player
player = Player()

# Room Triggers
# Replace these coordinates later
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
    "Room 206"
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
    room_211
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

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player Movement
    keys = pygame.key.get_pressed()
    
    player.update(keys, walls) 

    # Camera System
    camera_x = player.x - SCREEN_WIDTH // 2
    camera_y = player.y - SCREEN_HEIGHT // 2

    # Draw everything
    screen.fill((0, 0, 0))

    # Draw map
    draw_map(screen, camera_x, camera_y)

    # Draw player 
    player.draw(screen, camera_x, camera_y)

    # Player collision rect
    player_rect = pygame.Rect(
        player.x - 20, 
        player.y - 40,
        40,
        40
    )

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

            if room.locked:
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
