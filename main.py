import pygame
import random

SIZE = (WIDTH, HEIGHT) = 600, 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


class Bird:
    def __init__(self):
        self.x = WIDTH * 0.2
        self.y = HEIGHT * 0.4
        self.falling_speed = 1

    def move(self, jump=False):
        if self.y + self.falling_speed <= 0:
            self.falling_speed = 0

        if self.y > HEIGHT and self.falling_speed > 0:
            self.falling_speed = 0

        self.y += self.falling_speed
        if jump:
            self.jump()
        self.falling_speed += 0.2

    def jump(self):
        self.falling_speed = -8

    def draw(self, window):
        pygame.draw.circle(window, RED, (self.x, self.y), 20)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.y = random.randint(10, 590)

    def move(self):
        self.x -= 3
        if self.x <= -50:
            self.x = 850
            self.y = random.randint(10, 590)

    def bird_collision(self, x, y):
        if self.x < x < self.x + 50:
            if not (self.y < y < self.y + 200):
                return True
        return False

    def draw(self, window):
        pygame.draw.rect(window, GREEN, (self.x, 0, 50, self.y))
        pygame.draw.rect(window, GREEN, (self.x, self.y + 200, 50, HEIGHT))


class Game:

    def __init__(self):
        pygame.font.init()
        pygame.display.set_caption("Flappy Bird")
        self.WINDOW = pygame.display.set_mode(SIZE)
        self.bird = Bird()
        self.pipes = [Pipe(400), Pipe(700), Pipe(1000)]
        self.score = 0
        self.next_pipe = self.pipes[0]
        self.done = False

    def reset(self):
        self.bird = Bird()
        self.pipes = [Pipe(400), Pipe(700), Pipe(1000)]
        self.score = 0
        self.next_pipe = self.pipes[0]
        self.done = False
        return self.bird.x, self.bird.y, self.bird.falling_speed, self.next_pipe.x, self.next_pipe.y

    def step(self, action):
        for pipe in self.pipes:
            pipe.move()
        self.bird.move(action)

        if not self.next_pipe == self.__get_next_pipe():
            self.next_pipe = self.__get_next_pipe()
            self.score += 1

        collision = self.next_pipe.bird_collision(self.bird.x, self.bird.y)
        reward = 1

        if collision:
            self.done = True
            reward = -100

        state = (self.bird.x, self.bird.y, self.bird.falling_speed, self.next_pipe.x, self.next_pipe.y)

        return state, reward

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
