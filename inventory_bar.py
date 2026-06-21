import pygame 

selected_index = 0 

def draw_inventory(screen, inventory, Weapons, screen_height, screen_width):

    bar_rect = pygame.Rect(10, screen_height - 70, screen_width - 20,60)
    pygame.draw.rect(screen, (253,253,253), bar_rect)
    pygame.draw.rect(screen, (200,200,200), bar_rect, 2)

    x_offset = 20
    y_offset = screen_height - 65
    for i, weapon_name in enumerate(inventory.items):
        weapon = Weapons[weapon_name]
        if not weapon or "image" not in weapon:
            continue 

        img = pygame.transform.scale(weapon["image"], (50,50))
        rect = img.get_rect(topleft=(x_offset, y_offset))
        screen.blit(img, rect)

        # show uses if weapon has them 
        if "uses" in weapon:
            font = pygame.font.Font(None, 24)
            text = font.render(str(weapon["uses"]), True, (255,255,255))
            screen.blit(text, (x_offset, y_offset + 50))

        # Yellow box to show which item is selected

        if i == selected_index:
            pygame.draw.rect(screen, (255, 255, 0), rect, 2)

        x_offset += 100

def handle_inventory_click(mouse_pos, player, inventory, screen_height):
    global selected_index
    x_offset = 20
    y_offset = screen_height - 110

    for i, weapon_name in enumerate(inventory.items):
        rect = pygame.Rect(x_offset, y_offset, 90, 90)
        if rect.collidepoint(mouse_pos):
            selected_index = i
            player.held_weapon = weapon_name
        x_offset += 100