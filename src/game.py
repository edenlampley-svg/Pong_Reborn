import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR
from src.paddle import Paddle
from src.ball import Ball
from src.scoreboard import Scoreboard


class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong Reborn")
        self.clock = pygame.time.Clock()
        self.running = True

        self.left_paddle = Paddle(30, SCREEN_HEIGHT // 2 - 50)
        self.right_paddle = Paddle(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 50)
        self.ball = Ball(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10)

        self.scoreboard = Scoreboard()
        self.ai_speed = 4

        self.game_started = False
        self.font = pygame.font.Font(None, 48)

        self.winning_score = 5
        self.game_over = False
        self.winner = ""

    def run(self):
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.game_started = True

                if event.key == pygame.K_RETURN and self.game_over:
                    self._reset_game()

    def _update(self):
        if not self.game_started or self.game_over:
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.left_paddle.move_up()
        if keys[pygame.K_s]:
            self.left_paddle.move_down()

        if self.ball.rect.centery < self.right_paddle.rect.centery:
            self.right_paddle.rect.y -= self.ai_speed
        elif self.ball.rect.centery > self.right_paddle.rect.centery:
            self.right_paddle.rect.y += self.ai_speed

        if self.right_paddle.rect.top < 0:
            self.right_paddle.rect.top = 0
        if self.right_paddle.rect.bottom > SCREEN_HEIGHT:
            self.right_paddle.rect.bottom = SCREEN_HEIGHT

        self.ball.move()

        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.ball.speed_y *= -1

        if self.ball.rect.colliderect(self.left_paddle.rect):
            self.ball.speed_x *= -1

        if self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.speed_x *= -1

        if self.ball.rect.left <= 0:
            self.scoreboard.right_score += 1
            self.ball.reset()

        if self.ball.rect.right >= SCREEN_WIDTH:
            self.scoreboard.left_score += 1
            self.ball.reset()

        if self.scoreboard.left_score >= self.winning_score:
            self.game_over = True
            self.winner = "Player Wins!"

        if self.scoreboard.right_score >= self.winning_score:
            self.game_over = True
            self.winner = "Bot Wins!"

    def _reset_game(self):
        self.scoreboard.left_score = 0
        self.scoreboard.right_score = 0
        self.left_paddle.rect.y = SCREEN_HEIGHT // 2 - 50
        self.right_paddle.rect.y = SCREEN_HEIGHT // 2 - 50
        self.ball.reset()
        self.game_started = False
        self.game_over = False
        self.winner = ""
    
    def _draw(self):
        self.screen.fill(BG_COLOR)

        pygame.draw.line(
            self.screen,
            (255, 255, 255),
            (SCREEN_WIDTH // 2, 0),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT),
            4
        )

        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.scoreboard.draw(self.screen)

        if self.game_over:
            win_text = self.font.render(self.winner, True, (255, 255, 255))
            restart_text = self.font.render("Press ENTER to Restart", True, (255, 255, 255))

            win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))

            self.screen.blit(win_text, win_rect)
            self.screen.blit(restart_text, restart_rect)

        elif not self.game_started:
            start_text = self.font.render("Press SPACE to Start", True, (255, 255, 255))
            controls_text = self.font.render("Use W and S keys to move", True, (255, 255, 255))

            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))

            self.screen.blit(start_text, start_rect)
            self.screen.blit(controls_text, controls_rect)

        pygame.display.flip()