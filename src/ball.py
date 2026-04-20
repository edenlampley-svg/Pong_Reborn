import pygame

WHITE = (255, 255, 255)


class Ball:
    def __init__(self, x, y, size=20):
        self.rect = pygame.Rect(x, y, size, size)

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)