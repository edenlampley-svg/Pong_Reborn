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

        self.player_speed = 6
        self.ai_start_speed = 4
        self.ai_speed = self.ai_start_speed
        self.ai_max_speed = self.player_speed - 1

        self.ai_ramp_active = False
        self.ai_acceleration = 0.01

        self.game_started = False
        self.game_over = False
        self.winner = ""

        self.start_time = None

        self.font = pygame.font.Font(None, 48)

        self.winning_score = 10

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
                    if self.start_time is None:
                        self.start_time = pygame.time.get_ticks()

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

        if self.ball.rect.colliderect(self.left_paddle.rect) and self.ball.speed_x < 0:
            self._handle_paddle_bounce(self.left_paddle, moving_right=True)

        if self.ball.rect.colliderect(self.right_paddle.rect) and self.ball.speed_x > 0:
            self._handle_paddle_bounce(self.right_paddle, moving_right=False)

        if self.ball.rect.left <= 0:
            self.scoreboard.right_score += 1
            self.ball.reset()

        if self.ball.rect.right >= SCREEN_WIDTH:
            self.scoreboard.left_score += 1
            self.ball.reset()

        if self.scoreboard.left_score >= 2:
            self.ai_ramp_active = True

        if self.start_time is not None:
            elapsed_time = pygame.time.get_ticks() - self.start_time
            if elapsed_time >= 20000:
                self.ai_ramp_active = True

        if self.ai_ramp_active and self.ai_speed < self.ai_max_speed:
            self.ai_speed += self.ai_acceleration
            if self.ai_speed > self.ai_max_speed:
                self.ai_speed = self.ai_max_speed

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
        self.ai_speed = self.ai_start_speed
        self.ai_ramp_active = False
        self.start_time = None
    
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

    def _handle_paddle_bounce(self, paddle, moving_right):
        ball_center = self.ball.rect.centery
        paddle_center = paddle.rect.centery

        relative_intersect = ball_center - paddle_center
        normalized_intersect = relative_intersect / (paddle.rect.height / 2)

        max_bounce_speed = 6
        self.ball.speed_y = normalized_intersect * max_bounce_speed

        current_speed = abs(self.ball.speed_x)
        new_speed = min(current_speed + 0.5, 12)

        if moving_right:
            self.ball.speed_x = new_speed
            self.ball.rect.left = paddle.rect.right
        else:
            self.ball.speed_x = -new_speed
            self.ball.rect.right = paddle.rect.left