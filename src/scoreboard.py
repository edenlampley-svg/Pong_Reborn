import pygame
from src.settings import WHITE, SCREEN_WIDTH


class Scoreboard:
    def __init__(self):
        self.left_score = 0
        self.right_score = 0
        self.font = pygame.font.Font(None, 74)

    def draw(self, screen):
        left_text = self.font.render(str(self.left_score), True, WHITE)
        right_text = self.font.render(str(self.right_score), True, WHITE)

        screen.blit(left_text, (SCREEN_WIDTH // 4, 20))
        screen.blit(right_text, (SCREEN_WIDTH * 3 // 4, 20))