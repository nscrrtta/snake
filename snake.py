from random import randint
import threading
import pygame
import time


sqr_size = 20
width = 40*sqr_size
height = 32*sqr_size
running = True
paused = False


pygame.init()
font = pygame.font.Font(None, 40)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake by Nick Sciarretta')


class Snake:

    def new_game(self):

        # Start snake in center of screen moving down
        self.body = [(width//2, height//2)]
        self.dx, self.dy = 0, 1
        
        self.game_over = False 
        self.apples_eaten = 0
        self.dir_queue = []


    def eat_apple(self):

        self.apples_eaten += 1
        
        ########## Add <sqr_size> squares to body ##########
        x1, y1 = self.body[-1] # Tail of snake

        if len(self.body) == 1:
            dx, dy = self.dx, self.dy
        else:
            x2, y2 = self.body[-2]
            dx, dy = x2-x1, y2-y1

        if dx != 0:
            for i in range(x1-dx, x1-dx*(sqr_size+1), -dx):
                self.body.append((i, y1))

        if dy != 0:
            for j in range(y1-dy, y1-dy*(sqr_size+1), -dy):
                self.body.append((x1, j))
        ####################################################


    def move(self):

        x1, y1 = self.body[0] # Current head of snake
        x2, y2 = x1+self.dx, y1+self.dy # Next head of snake

        # Only change direction when head is at a multiple of sqr_size
        if x2%sqr_size==0 and y2%sqr_size==0 and self.dir_queue:
            self.dx, self.dy = self.dir_queue.pop(0)

        if (x2, y2) in self.body: self.game_over = True # bit itself
        if not 0*sqr_size <= x2 <= (width -sqr_size): self.game_over = True # out of bounds
        if not 2*sqr_size <= y2 <= (height-sqr_size): self.game_over = True # out of bounds
        
        if self.game_over: return

        self.body.insert(0, (x2,y2))
        self.body.pop(-1)


    def draw(self):

        for i, (x,y) in enumerate(self.body):
            if i%sqr_size: continue # Draw every <sqr_size> square in body
            rect = pygame.Rect(x+1, y+1, sqr_size-2, sqr_size-2)
            pygame.draw.rect(screen, (0,255,0), rect, border_radius=3)


class Apple:
    
    def move(self, snake: Snake):

        while not snake.game_over:
            self.x = randint(0, width //sqr_size-1)*sqr_size
            self.y = randint(2, height//sqr_size-1)*sqr_size
            if (self.x, self.y) not in snake.body: break


    def draw(self):

        rect = pygame.Rect(self.x+1, self.y+1, sqr_size-2, sqr_size-2)
        pygame.draw.rect(screen, (255,0,0), rect, border_radius=3)


snake = Snake()
apple = Apple()
snake.new_game()
apple.move(snake)


def draw():

    while running:

        screen.fill((0,0,0))
        apple.draw()
        snake.draw()

        pygame.draw.rect(screen, (255,255,255), pygame.Rect(-1,-1, width+2, 2*sqr_size+1), 1)
        screen.blit(font.render(f'Score: {snake.apples_eaten}', True, (255,255,255)), (7,7))

        if snake.game_over: screen.blit(font.render('Game Over!', True, (255,255,255)), (320,7))
        if paused: screen.blit(font.render('Paused', True, (255,255,255)), (690,7))

        pygame.display.update()


threading.Thread(target=draw).start()


while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_n:
                snake.new_game()
                apple.move(snake)

            elif snake.game_over: pass

            elif event.key == pygame.K_ESCAPE:
                paused = not paused

            elif paused: pass

            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dir_queue.append((0,-1))

            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dir_queue.append((0,1))

            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dir_queue.append((-1,0))

            elif event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dir_queue.append((1,0))

    time.sleep(0.005)
    
    if paused or snake.game_over: continue
    snake.move()
    
    if snake.body[0] == (apple.x, apple.y):
        snake.eat_apple()
        apple.move(snake)
    

pygame.quit()
