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
        self.scoreboard = Scoreboard()

        self.left_paddle = Paddle(30, SCREEN_HEIGHT // 2 - 50)
        self.right_paddle = Paddle(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 50)
        self.ball = Ball(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10)

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

    def _update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.left_paddle.move_up()
        if keys[pygame.K_s]:
            self.left_paddle.move_down()

        if keys[pygame.K_UP]:
            self.right_paddle.move_up()
        if keys[pygame.K_DOWN]:
            self.right_paddle.move_down()

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

    def _draw(self):
        self.screen.fill(BG_COLOR)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.scoreboard.draw(self.screen)
        pygame.display.flip()