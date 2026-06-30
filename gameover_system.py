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

    def reset(self, player):
        self.lives = self.max_lives
        self.game_over = False
        self.last_checkpoint = self.spawn_point
        player.x, player.y = self.spawn_point

    def is_game_over(self):
        return self.game_over

    # ---------------------------
    # INPUT
    # ---------------------------
    def handle_click(self, pos, player):
        if self.try_again_button.collidepoint(pos):
            self.reset(player)
            return "retry"

        if self.quit_button.collidepoint(pos):
            return "quit"

        return None

    # ---------------------------
    # DRAW
    # ---------------------------
    def draw(self, screen):
        screen.blit(self.gameover_bg, (0, 0))