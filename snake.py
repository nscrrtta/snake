from constants import *
import pygame
import random


lite_green = (0, 255, 0)
dark_green = (0, 127, 0)


class Snake:

    def reset(self):
        # Starting square
        x = random.randint(0, COLS - 1) * SQUARE_SIZE
        y = random.randint(0, ROWS - 1) * SQUARE_SIZE
        self.head = x, y

        # The snake's body is drawn as a collection of squares.
        # Each (x, y) coordinate in self.body is the
        # top-left of coordinate of that square.
        #
        # self.head is always the first item in self.body
        self.body = [self.head]

        # Starting direction
        self.dx = random.choice([-1, 0, 1])
        self.dy = random.choice([-1, 1]) if self.dx == 0 else 0

        # Direction queue (only ever one direction in queue at a time)
        self.queue: list[tuple[int, int]] = []

    def move(self):
        x, y = self.head

        # Only change direction when head is at a multiple of SQUARE_SIZE.
        # This ensures the snake remains aligned to the grid.
        if self.queue and x % SQUARE_SIZE == y % SQUARE_SIZE == 0:
            self.dx, self.dy = self.queue.pop()

        x += self.dx * SNAKE_SPEED
        y += self.dy * SNAKE_SPEED

        # Update position of head (keep coordinates in bounds)
        self.head = x % PLAY_AREA_WIDTH, y % PLAY_AREA_HEIGHT

        self.body.insert(0, self.head)
        self.body.pop()

    def queue_direction(self, direction: tuple[int, int]):
        if direction != (-self.dx, -self.dy):
            self.queue = [direction]

    def grow(self):
        self.body.extend([self.body[-1]] * STEPS)

    def bit_itself(self) -> bool:
        return self.head in self.body[1:]

    def ate_apple(self, x: int, y: int) -> bool:
        return self.head == (x, y)

    def draw(self, window: pygame.Surface):
        for x, y in self.body[STEPS::STEPS]:
            self._draw_wrapping_square(window, x, y, False)
        self._draw_wrapping_square(window, *self.head, True)

    def _draw_wrapping_square(self, window: pygame.Surface, x: int, y: int, head: bool):
        self._draw_square(window, x, y, head)

        xi, yi = x, y
        if xi > PLAY_AREA_WIDTH - SQUARE_SIZE:
            xi -= PLAY_AREA_WIDTH
        if yi > PLAY_AREA_HEIGHT - SQUARE_SIZE:
            yi -= PLAY_AREA_HEIGHT

        if xi != x or yi != y:
            self._draw_square(window, xi, yi, head)

    def _draw_square(self, window: pygame.Surface, x: int, y: int, head: bool):
        colour = dark_green if head else lite_green
        width = height = SQUARE_SIZE - 2

        rect = pygame.Rect(x + 1, y + 1, width, height)
        pygame.draw.rect(window, colour, rect, border_radius=3)
