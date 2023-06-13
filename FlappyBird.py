import pygame
import random

SIZE = (WIDTH, HEIGHT) = 600, 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
FPS = 60

class Bird:
    def __init__(self):
        self.x = WIDTH * 0.2 
        self.y = HEIGHT * 0.4
        self.velocity = 1

    def move(self, jump=False):
        self.y += self.velocity
        self.velocity += 0.2

        self.y = max(0, min(self.y, HEIGHT)) 

        if jump:
            self.jump()

    def jump(self):
        self.velocity = -8

    def draw(self, window):
        pygame.draw.circle(window, RED, (self.x, self.y), 20)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.y = random.randint(10, 590)
        self.width = 50
        self.gap_height = 200

    def move(self):
        self.x -= 2
        if self.x <= -self.width:
            self.x = 850
            self.y = random.randint(10, 590)

    def bird_collision(self, bird):
        obstacle_horizontal_range = self.x < bird.x < self.x + self.width
        obstacle_vertical_range = not (self.y < bird.y < self.y + self.gap_height)
        return obstacle_horizontal_range and obstacle_vertical_range

    def draw(self, window):
        pygame.draw.rect(window, GREEN, (self.x, 0, self.width, self.y))
        pygame.draw.rect(window, GREEN, (self.x, self.y + self.gap_height, self.width, HEIGHT))


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        self.WINDOW = pygame.display.set_mode(SIZE)
        self.bird = Bird()
        self.pipes = [Pipe(400), Pipe(700), Pipe(1000)]
        self.score = 0
        self.next_pipe = self.pipes[0]
        self.done = False
        self.clock = pygame.time.Clock()

    def reset(self):
        self.bird = Bird()
        self.pipes = [Pipe(400), Pipe(700), Pipe(1000)]
        self.score = 0
        self.next_pipe = self.pipes[0]
        self.done = False
        return self.bird.x, self.bird.y, self.bird.velocity, self.next_pipe.x, self.next_pipe.y

    def step(self, action):
        for pipe in self.pipes:
            pipe.move()
        self.bird.move(action==1)

        reward = 1

        if not self.next_pipe == self.__get_next_pipe():
            self.next_pipe = self.__get_next_pipe()
            self.score += 1

        collision = self.next_pipe.bird_collision(self.bird)
        
        if collision:
            self.done = True
            reward = -10000

        difference_y_pipe_bird = round((self.bird.y - self.next_pipe.y)/5) * 5 

        state = (difference_y_pipe_bird, self.bird.velocity, round(self.next_pipe.x/5)*5)

        return str(state), reward, self.done

    def render(self):
        self.WINDOW.fill(WHITE)
        for pipe in self.pipes:
            pipe.draw(self.WINDOW)
        self.bird.draw(self.WINDOW)

        # draw score
        font = pygame.font.SysFont(None, 40)
        text = font.render(str(self.score), False, BLACK)
        self.WINDOW.blit(text, (WIDTH / 2, HEIGHT * 0.2))

        pygame.display.update()

    def __get_next_pipe(self):
        front_of_bird_pipes = [pipe for pipe in self.pipes if pipe.x + 50 >= self.bird.x]
        next_pipe = sorted(front_of_bird_pipes, key=lambda pipe: pipe.x)[0]
        return next_pipe
    
    def play(self):
        while not self.done:
            jump = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        jump = True
            
            self.step(jump)
            self.render()
            self.clock.tick(FPS)