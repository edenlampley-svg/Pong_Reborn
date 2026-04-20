import pygame
from src.settings import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT


class Ball:
    def __init__(self, x, y, size=20, speed_x=5, speed_y=5):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.start_speed_x = speed_x
        self.start_speed_y = speed_y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x *= -1
        self.speed_y = self.start_speed_y

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)