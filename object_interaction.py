import pygame
from inventory import game_inventory as inventory
from inventory import JANITOR_KEY, ROOM_210_KEY, SECURITY_BADGE, ROOM_206_KEY, ROOM116_KEY, BOLT_CUTTER

class ObjectInteraction:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("arial",32) 
        self.visible = False
        self.current_item = None
        self.popup_start_time = 0
        self.popup_duration = 5000

        # =========================
        # INTERACTION ZONES (TEMP)
        # =========================
        
        self.zones = {
            "box": {
                "zone": pygame.Rect(291, 2350, 56, 48) , "collected": False # 210 key 
            },
            "toolbox": {
                "zone": pygame.Rect(2572, 2210, 211, 169), # maintanence room
                "collected": False
            },
            "locker": {
                "zone": pygame.Rect(3062, 2186, 120,120 ), "collected": False # badge in janitor's locker
            },
            "stool": {
                "zone": pygame.Rect(1387, 445, 64, 63),"collected": False   # janitor key in gym
            }
        }

        # =========================
        # ITEM MAPPING
        # =========================
        self.items = {
            "box": ROOM_210_KEY,
            "toolbox": BOLT_CUTTER, #level2
            "stool": JANITOR_KEY 
        }

        # =========================
        # LOAD IMAGES
        # =========================
        self.images = {
            BOLT_CUTTER: self.load("assets/bolt_cutter.png"),
            ROOM_210_KEY: self.load("assets/210key.png"),
            "116key": self.load("assets/116key.png"),
            ROOM116_KEY: self.load("assets/116key.png"),
            JANITOR_KEY: self.load("assets/janitorkey.png"),
            SECURITY_BADGE: self.load("assets/badge.png"),
            ROOM_206_KEY: self.load("assets/206key.png")
        }

        self.visible = False
        self.current_item = None
    # -------------------------
    # LOAD IMAGE
    # -------------------------
    def load(self, path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (220, 220))

    # -------------------------
    # INTERACTION CHECK
    # -------------------------
    def try_interact(self, player_rect):
        for name, data in self.zones.items():

            zone = data["zone"]

            if player_rect.colliderect(zone):

                if name in self.items:
                    self.trigger(self.items[name], name)

    # -------------------------
    # SHOW ITEM
    # -------------------------
    def trigger(self, item_name, zone_name= None):
        self.visible = True
        self.current_item = item_name
        self.popup_start_time = pygame.time.get_ticks()

        # add item into inventory
        if isinstance(item_name, list):
            for item in item_name:
                if item not in inventory.items:
                   inventory.add_item(item)

        else:
            if item_name not in inventory.items:
                inventory.add_item(item_name)

        if zone_name: 
            self.zones[zone_name]["collected"] = True
    def hide(self):
        self.visible = False
        self.current_item = None

    # -------------------------
    # DRAW POPUP
    # -------------------------
    def draw(self, screen):
        if not self.visible:
            return
        
        if pygame.time.get_ticks() - self.popup_start_time > self.popup_duration:
            self.hide()
            return

        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        img = self.images[self.current_item]
        rect = img.get_rect(center=(screen.get_width() // 2, 280))
        screen.blit(img, rect)

        text = self.font.render(
            f"Obtained: {self.current_item}",
            True,
            (255, 255, 255)
        )

        screen.blit(text, text.get_rect(center=(screen.get_width() // 2, 460)))

    def show_object_prompt( self, screen, font, zone, player_rect, camera_x=0, camera_y=0, collected= False):
        if collected:
            return
        
        # show r above zone
        draw_x = zone.centerx - camera_x 
        draw_y = zone.top - camera_y - 30

              # Draw circle around R
        pygame.draw.circle(screen, (153,204,255), (draw_x, draw_y), 20)

        text = font.render("R", True, (0,0,0))
        text_rect = text.get_rect(center=(draw_x, draw_y))
        screen.blit(text, text_rect)


#level 2 boltcutter for janitor's locker to get security badge, janitorkey- unlock janitor's room, 210key- unlock jay's room
#level 1 coordinates for fusebox-screwdriver, exit key in recetionist locker - trigger ending scene, room 117- bathroom mirror