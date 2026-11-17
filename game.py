from constants import *
from apple import Apple
from snake import Snake
import pygame


bg_colour = (20, 20, 20)
white = (255, 255, 255)


class Game:

    def __init__(self):
        self.apple = Apple()
        self.snake = Snake()

        self.font = pygame.font.Font(None, FONT_SIZE)

        self.paused_text = self.font.render('Paused', True, white)
        self.paused_rect = self.paused_text.get_rect(midright=MIDRIGHT)

        self.game_over_text = self.font.render('Game Over!', True, white)
        self.game_over_rect = self.game_over_text.get_rect(midright=MIDRIGHT)

        self.new_game()

    def new_game(self):
        self.snake.reset()
        self.apple.move(self.snake.body)

        self.update_score(0)

        self.game_over = False
        self.paused = False

    def move_snake(self):
        if self.game_over or self.paused:
            return

        self.snake.move()

        if self.snake.bit_itself():
            self.game_over = True
            return

        if self.snake.ate_apple(self.apple.x, self.apple.y):
            self.snake.grow()
            self.update_score(self.score + 1)
            if self.score == MAX_SCORE:
                self.game_over = True
                return
            self.apple.move(self.snake.body)

    def update_score(self, score: int):
        self.score_text = self.font.render(f'Score: {score}/{MAX_SCORE}', True, white)
        self.score_rect = self.score_text.get_rect(midleft=MIDLEFT)
        self.score = score

    def draw(self, window: pygame.Surface):
        window.fill(bg_colour)

        self.apple.draw(window)
        self.snake.draw(window)

        #
        # Below playing area
        #

        top = PLAY_AREA_HEIGHT + 1
        rect = pygame.Rect(0, top, WINDOW_WIDTH, 1)
        pygame.draw.rect(window, white, rect)

        top += 1
        rect = pygame.Rect(0, top, WINDOW_WIDTH, WINDOW_HEIGHT - top)
        pygame.draw.rect(window, bg_colour, rect)

        window.blit(self.score_text, self.score_rect)

        if self.paused:
            window.blit(self.paused_text, self.paused_rect)
        elif self.game_over:
            window.blit(self.game_over_text, self.game_over_rect)
