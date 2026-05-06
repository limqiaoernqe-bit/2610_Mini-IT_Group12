import pygame
import pytmx

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Level 2 Map")

clock = pygame.time.Clock()

# Load Map
tmx_data = pytmx.load_pygame("level2_map.tmx")
TILE_SIZE = tmx_data.tilewidth

# Collision Layer
collision_layer = [
    "wall",
    "object",
    "guest room border",
    "Collision",    
]

walls = []

# Create Collision Rectangles
for layer in tmx_data.visible_layers:
    if isinstance(layer, pytmx.TiledTileLayer):
        if layer.name in collision_layer:
            for x, y, gid in layer:
                if gid != 0:
                    wall_rect = pygame.Rect(
                        x * TILE_SIZE, 
                        y * TILE_SIZE, 
                        TILE_SIZE, 
                        TILE_SIZE
                    )
                    walls.append(wall_rect)

# Draw Map 
def draw_map(surface):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    surface.blit(
                        tile, 
                        (x * TILE_SIZE, y * TILE_SIZE)
                    )

# OPTIONAL: SHOW COLLISION BOXES
# (For testing only)
# --------------------
show_collision = False

def draw_collision(surface):
    for wall in walls:
        pygame.draw.rect(surface, (255, 0, 0), wall, 1)


# Main Game Loop
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

         # Press C to show / hide collision boxes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                show_collision = not show_collision

    # Draw Everything
    screen.fill((0, 0, 0))
    draw_map(screen)

     # Show collision boxes if enabled
    if show_collision:
        draw_collision(screen)

    pygame.display.flip()

pygame.quit()
