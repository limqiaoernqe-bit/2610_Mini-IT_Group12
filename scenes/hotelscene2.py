# room 206 (successfully solved puzzle at the gym): 
# chloe: mia...jay isnt gone. i heard him.. hes in the room near the gym.

# room 210 (use room key in janitor's room): 
# mia: Go hide with chloe. I'm gona save the others. jay: okay..

# room 116 mark: oh my god, mia! whats happening? mia:Shh..get to a room and hide with the others.
# mia: once i find james, then we'll get out of here together. james: SOMEBODY HELP!

# room 117 (successfully input code at bathroom mirror):
# james: Mia, im so glad youre okay! Wheres everyone else? mia: No time to explain. 
# mia: we have to go right now! 

# ending scene triggers
# =========================
# SCENE STATE TRACKER
# =========================

class HotelSceneManager2:
    def __init__(self):
        self.active = False
        self.dialogue = []
        self.index = 0

        self.finished = {
            "chloe": False,
            "jay": False,
            "mark": False,
            "james": False,
            "ending": False
        }

    # -------------------------
    # TRIGGER FUNCTIONS
    # -------------------------

    def trigger_chloe(self):
        if self.finished["chloe"]:
            return
        self._start(SAVECHLOE_DIALOGUE)
        self.finished["chloe"] = True

    def trigger_jay(self):
        if self.finished["jay"]:
            return
        self._start(SAVEJAY_DIALOGUE)
        self.finished["jay"] = True

    def trigger_mark(self):
        if self.finished["mark"]:
            return
        self._start(SAVEMARK_DIALOGUE)
        self.finished["mark"] = True

    def trigger_james(self):
        if self.finished["james"]:
            return
        self._start(SAVEJAMES_DIALOGUE)
        self.finished["james"] = True

    def trigger_ending(self):
        if self.finished["ending"]:
            return
        self._start(ENDING_DIALOGUE)
        self.finished["ending"] = True

    # -------------------------
    # CORE SYSTEM
    # -------------------------

    def _start(self, dialogue):
        self.active = True
        self.dialogue = dialogue
        self.index = 0

    def update(self):
        """Call when player presses SPACE / ENTER"""
        if not self.active:
            return

        self.index += 1

        if self.index >= len(self.dialogue):
            self.active = False  # resume gameplay

    def get_current_line(self):
        if not self.active:
            return None
        return self.dialogue[self.index]

    def draw(self, screen, font, image_dict):
        """
        image_dict = {
            "chloe_front_detailed.png": pygame.image,
            ...
        }
        """
        if not self.active:
            return

        name, img, text = self.get_current_line()

        # dark overlay
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # portrait
        if img and img in image_dict:
            screen.blit(image_dict[img], (50, 100))

        # text box
        box = pygame.Rect(50, screen.get_height() - 180,
                           screen.get_width() - 100, 130)
        pygame.draw.rect(screen, (20, 20, 20), box)

        # render text
        if name:
            name_surf = font.render(name + ":", True, (255, 255, 0))
            screen.blit(name_surf, (70, screen.get_height() - 170))

        text_surf = font.render(text, True, (255, 255, 255))
        screen.blit(text_surf, (70, screen.get_height() - 130))


# =========================
# GLOBAL INSTANCE
# =========================

scene_manager = HotelSceneManager2()


# =========================
# EASY TRIGGER FUNCTIONS
# (CALL THESE FROM YOUR GAME)
# =========================

def on_chloe_saved():
    scene_manager.trigger_chloe()

def on_jay_saved():
    scene_manager.trigger_jay()

def on_mark_saved():
    scene_manager.trigger_mark()

def on_james_saved():
    scene_manager.trigger_james()

def on_game_end():
    scene_manager.trigger_ending()
