import pygame


class GameOverSystem:
    def __init__(self, lives=3, spawn_point=(100, 300)):

        self.max_lives = lives
        self.lives = lives

        self.spawn_point = spawn_point
        self.last_checkpoint = spawn_point

        self.game_over = False

        # Buttons
        self.try_again_button = pygame.Rect(435, 433, 410, 82)
        self.quit_button = pygame.Rect(435, 551, 410, 82)

        # Load background SAFELY (inside init)
        self.gameover_bg = pygame.image.load(
            "assets/game_over.png"
        ).convert_alpha()

    def reset_player(self, player):
        player.x, player.y = self.spawn_point

    # ---------------------------
    # GAME LOGIC
    # ---------------------------
    def on_caught(self, player):
        self.lives -= 1

        if self.lives <= 0:
            self.game_over = True
            return

        self.reset_player(player)

    def set_checkpoint(self, pos):
        self.last_checkpoint = pos

    def reset(self, player, inventory=None, weapons=None, objects=None, puzzles= None, clues=None):
        self.lives = self.max_lives
        self.game_over = False
        self.last_checkpoint = self.spawn_point
        player.x, player.y = self.spawn_point

        if inventory:
            inventory.items.clear()

            # clear file so retry mode starts fresh
            import json
            with open("save_inventory.json", "w") as f:
                json.dump({"items": [], "uses": {}}, f)

        if weapons:
            for name, weapon in weapons.items():
                weapon["collected"] = False
                if "uses" in weapon:
                    if name in ["BananaPeel", "CleaningSpray", "Salt"]:
                      weapon["uses"] = 3
                    else:
                      weapon["uses"] = 0
        # Reset object
        if objects:
            for zone in objects.zones.values():
                if "collected" in zone:
                    zone["collected"] = False

        # Reset Puzzle
        if puzzles:
            for puzzle in puzzles.values():
                puzzle["collected"] = False
                puzzle["answer"] = "" 
                puzzle["active"] = False
                puzzle["end_message"]= "" 

        # Reset Clue
        if clues:
            for clue in clues.values():
                clue["active"] = True
                clue["show_prompt"] = False
                clue["show_popup"] = False

    def is_game_over(self):
        return self.game_over

    # ---------------------------
    # INPUT
    # ---------------------------
    def handle_click(self, pos, player, inventory=None, weapons=None, objects=None, puzzles=None, clues=None ):
        if self.try_again_button.collidepoint(pos):
            globals()["retry_mode"] = True
            self.reset(player, inventory, weapons, objects, puzzles, clues)
            return "retry"

        if self.quit_button.collidepoint(pos):
            return "quit"

        return None

    # ---------------------------
    # DRAW
    # ---------------------------
    def draw(self, screen):
        screen.blit(self.gameover_bg, (0, 0))