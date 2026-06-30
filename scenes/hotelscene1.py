
import pytmx

from player import Player
from janitor import Janitor
from scenes.base_scene import BaseScene
from scenes.dialogue_scene import DialogueScene
from dialogues import JANITOR_DIALOGUE


class HotelScene1(BaseScene):
    def __init__(self):
        super().__init__()

        print("HOTELSCENE1 CREATED")


        # MAP
        self.tmx_data = pytmx.load_pygame("level2_map.tmx")
        self.tile_size = self.tmx_data.tilewidth

        # PLAYER
        self.player = Player()
        self.player.x = 1056
        self.player.y = 1442

        # CAMERA
        self.camera_x = 0
        self.camera_y = 0

        # DIALOGUE
        self.dialogue = DialogueScene(JANITOR_DIALOGUE)
        self.dialogue.dialogue_box.scene = self

        # MOVEMENT
        self.path = []
        self.step = 0
        self.moving = False
        self.speed = 8

        # JANITOR
        self.janitor = None



    # COMMANDS
    def start_path(self, path):
        self.path = path
        self.step = 0
        self.moving = True

    def spawn_janitor(self, pos):
         print("SPAWNING JANITOR:", pos) 
         self.janitor = Janitor(pos[0], pos[1],self.tile_size)
         self.player.direction = "back" 
         self.player.image = self.player.idle_back

    def update(self): 
        self.camera_x = self.player.x - 800 // 2 
        self.camera_y = self.player.y - 600 // 2

        if self.moving: 
            self.move()
        else: 
            self.dialogue.update()

        if self.janitor: 
            self.janitor.update( self.player.x, self.player.y, [],[])

        if self.dialogue.is_finished() and not self.moving:
            self.finished = True


    def move(self):
        if not self.moving:
            return

        tx, ty = self.path[self.step]

        dx = tx - self.player.x
        dy = ty - self.player.y

        if abs(dx) > self.speed:
            self.player.x += self.speed if dx > 0 else -self.speed
            self.player.image = self.player.animate(
                self.player.walk_right if dx > 0 else self.player.walk_left
            )

        elif abs(dy) > self.speed:
            self.player.y += self.speed if dy > 0 else -self.speed
            self.player.image = self.player.animate(
                self.player.walk_front if dy > 0 else self.player.walk_back
            )

        else:
            self.step += 1

            if self.step >= len(self.path):
                self.moving = False
                return

    def draw(self, screen):
        screen.fill((0, 0, 0))

        self.draw_map(screen)

        self.player.draw(screen, self.camera_x, self.camera_y)

        if self.janitor:

            print(
                "JANITOR:",
                self.janitor.x,
                self.janitor.y
            )

            self.janitor.draw(
                screen,
                self.camera_x,
                self.camera_y
            )

        self.dialogue.draw(screen)

    def draw_map(self, surface):
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(
                            tile,
                            (x * self.tile_size - self.camera_x,
                             y * self.tile_size - self.camera_y)
                        )



    def handle_events(self, events):
        self.dialogue.handle_events(events)
