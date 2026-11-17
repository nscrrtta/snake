from constants import SQUARE_SIZE, ROWS, COLS
import pygame
import random


red = (255, 0, 0)


class Apple:

    def move(self, snake_body: list[tuple[int, int]]):
        self.x, self.y = snake_body[0]
        while (self.x, self.y) in snake_body:
            self.x = random.randint(0, COLS - 1) * SQUARE_SIZE
            self.y = random.randint(0, ROWS - 1) * SQUARE_SIZE

    def draw(self, window: pygame.Surface):
        width = height = SQUARE_SIZE - 2
        rect = pygame.Rect(self.x + 1, self.y + 1, width, height)
        pygame.draw.rect(window, red, rect, border_radius=3)
