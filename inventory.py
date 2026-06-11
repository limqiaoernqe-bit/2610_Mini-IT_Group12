import pygame 

selected_index = 0 

def draw_inventory(screen):
    x_offset = 20
    y_offset = 740
    for i, weapon_name in enumerate(inventory):
        weapon = Weapons[weapon_name]
        img = weapon["image"]
        rect = img.get_rect(topleft=(x_offset, y_offset))
        screen.blit(img, rect)

        # show uses if weapon has them 
        if "uses" in weapon:
            font = pygame.font.Font(None, 24)
            text = font.render(str(weapon["uses"]), True, (255,255,255))
            screen.blit(text, (x_offset, y_offset + 60))

        # Yellow box to show which item is selected

        if i == selected_index:
            pygame.draw.rect(screen, (255, 255, 0), rect, 2)

        x_offset += 100

def handle_inventory_click(mouse_pos, player):
    global selected_index
    x_offset = 20
    y_offset = 740

    for i, weapon_name in enumerate(inventory):
        rect = pygame.Rect(x_offset, y_offset, 90, 90)
        if rect.collidepoint(mouse_pos):
            selected_index = i
            player.held_weapon = weapon_name
        x_offset += 100