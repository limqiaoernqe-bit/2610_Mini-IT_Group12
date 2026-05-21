import pygame
import pytmx

from player import Player

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Camera Test")

clock = pygame.time.Clock()

# Load Map
tmx_data = pytmx.load_pygame("level2_map.tmx")
TILE_SIZE = tmx_data.tilewidth

# Create Player
player = Player()

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
    
    player.update(keys)

    # Camera System
    camera_x = player.x - SCREEN_WIDTH // 2
    camera_y = player.y - SCREEN_HEIGHT // 2

    # Draw everything
    screen.fill((0, 0, 0))

    # Draw map
    draw_map(screen, camera_x, camera_y)

    # Draw player 
    player.draw(screen, camera_x, camera_y)

    pygame.display.flip()

pygame.quit()
