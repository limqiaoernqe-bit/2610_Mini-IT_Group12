import pygame
from gameover_system import GameOverSystem

# import your own classes
from player import Player
from janitor import Janitor


class GameScene:
    def __init__(self):
        self.player = Player()
        self.janitor = Janitor(600, 300)

        self.gameover = GameOverSystem(
            lives=3,
            spawn_point=(100, 300)
        )

        self.game_over = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:

                # checkpoint
                if event.key == pygame.K_SPACE:
                    self.gameover.set_checkpoint(self.player.rect.topleft)

                # restart
                if self.game_over and event.key == pygame.K_r:
                    self.gameover.reset(self.player)
                    self.game_over = False

    def update(self):
        if not self.game_over:
            keys = pygame.key.get_pressed()

            self.player.update(keys)
            self.janitor.update(
                self.player.rect.x,
                self.player.rect.y
                )

            if self.player.rect.colliderect(self.janitor.rect):
                self.gameover.on_caught(self.player)

            if self.gameover.is_game_over():
                self.game_over = True

    def draw(self, screen):
        screen.fill((0, 0, 0))

        self.player.draw(screen)
        self.janitor.draw(screen)

        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Lives: {self.gameover.lives}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        if self.game_over:
            big = pygame.font.SysFont(None, 80).render("GAME OVER", True, (255, 0, 0))
            screen.blit(big, (400, 300))