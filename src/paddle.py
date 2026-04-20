import pygame

WHITE = (255, 255, 255)


class Paddle:
    def __init__(self, x, y, width=20, height=100):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)