import pygame
from inventory import game_inventory as inventory
from inventory import JANITOR_KEY, ROOM_210_KEY, SECURITY_BADGE, ROOM_206_KEY

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
                "zone": pygame.Rect(3160, 2052, 56, 48)  # 210 key in janitor's room
            },
            "toolbox": {
                "zone": pygame.Rect(2631, 2213, 211, 169) # maitanence room
            },
            "flashlight": {
                "zone": pygame.Rect(2501, 2261, 129, 117) # maitanence room
            },
            "locker": {
                "zone": pygame.Rect(3021, 2041, 59,53 ) # badge in janitor's locker
            },
            "stool": {
                "zone": pygame.Rect(1407, 410, 64, 63) # janitor key in gym
            }
        }

        # =========================
        # ITEM MAPPING
        # =========================
        self.items = {
            "box": ROOM_210_KEY,
            "toolbox": [
                "toolbox", 
                "bolt_cutter", 
                "screwdriver"
            ],
            "flashlight": "flashlight",
            "stool": JANITOR_KEY ,
            "locker": SECURITY_BADGE #level2
        }

        # =========================
        # LOAD IMAGES
        # =========================
        self.images = {
            "bolt_cutter": self.load("assets/bolt_cutter.png"),
            "toolbox": self.load("assets/toolbox.png"),
            "flashlight": self.load("assets/flashlight.png"),
            "screwdriver": self.load("assets/screwdriver.png"),
            ROOM_210_KEY: self.load("assets/210key.png"),
            "116key": self.load("assets/116key.png"),
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
                    self.trigger(self.items[name])

    # -------------------------
    # SHOW ITEM
    # -------------------------
    def trigger(self, item_name):
        self.visible = True
        self.current_item = item_name
        self.popup_start_time = pygame.time.get_ticks()

        # add item into inventory
        if isinstance(item_name, list):
            for item in item_name:
                inventory.add_item(item)

        else:
            inventory.add_item(item_name)

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

#level 2 boltcutter for janitor's locker to get security badge, janitorkey- unlock janitor's room, 210key- unlock jay's room
#level 1 coordinates for fusebox-screwdriver, exit key in recetionist locker - trigger ending scene, room 117- bathroom mirror