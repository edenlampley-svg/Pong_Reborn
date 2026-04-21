import pygame
from src.settings import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT


class Ball:
    def __init__(self, x, y, size=20, speed_x=6, speed_y=6):
        self.rect = pygame.Rect(x, y, size, size)
        self.start_x = x
        self.start_y = y

        self.speed_x = speed_x
        self.speed_y = speed_y

        self.base_speed_x = abs(speed_x)
        self.base_speed_y = speed_y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.speed_x = -self.speed_x / abs(self.speed_x) * self.base_speed_x
        self.speed_y = self.base_speed_y

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)