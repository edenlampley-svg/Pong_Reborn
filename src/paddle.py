import pygame
from src.settings import SCREEN_HEIGHT

WHITE = (255, 255, 255)


class Paddle:
    def __init__(self, x, y, width=20, height=100, speed=6):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def move_up(self):
        self.rect.y -= self.speed
        if self.rect.top < 0:
            self.rect.top = 0

    def move_down(self):
        self.rect.y += self.speed
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)