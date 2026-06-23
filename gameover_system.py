class GameOverSystem:
    def __init__(self, lives=3, spawn_point=(100, 300)):
        self.max_lives = lives
        self.lives = lives
        self.spawn_point = spawn_point

        self.last_checkpoint = spawn_point
        self.game_over = False

    # called when player gets caught
    def on_caught(self, player):
        if self.game_over:
            return

        self.lives -= 1

        if self.lives > 0:
            # respawn at last checkpoint
            player.rect.topleft = self.last_checkpoint
        else:
            self.game_over = True

    # save checkpoint
    def set_checkpoint(self, pos):
        self.last_checkpoint = pos

    # reset full game
    def reset(self, player):
        self.lives = self.max_lives
        self.game_over = False
        player.rect.topleft = self.spawn_point
        self.last_checkpoint = self.spawn_point

    # helper
    def is_game_over(self):
        return self.game_over

# when qiaoqiao finish testing enemy movement, can finish this.