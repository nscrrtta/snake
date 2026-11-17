from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from game import Game
import pygame


pygame.init()
pygame.display.set_caption('Snake by Nick Sciarretta')

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

game = Game()
running = True

while running:
    window.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                game.new_game()
            elif game.game_over:
                pass
            elif event.key == pygame.K_ESCAPE:
                game.paused = not game.paused
            elif game.paused:
                pass
            elif event.key == pygame.K_UP:
                game.snake.queue_direction((0, -1))
            elif event.key == pygame.K_DOWN:
                game.snake.queue_direction((0, 1))
            elif event.key == pygame.K_LEFT:
                game.snake.queue_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:
                game.snake.queue_direction((1, 0))

    clock.tick(FPS)
    game.move_snake()
    game.draw(window)
    pygame.display.update()

pygame.quit()
