import pygame
import random
import numpy as np
from collections import defaultdict

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
        self.falling_speed = 1

    def move(self, jump=False):
        # check top border
        if self.y + self.falling_speed <= 0:
            self.falling_speed = 0

        # check bottom border
        if self.y > HEIGHT and self.falling_speed > 0:
            self.falling_speed = 0

        if jump:
            self.jump()

        self.y += self.falling_speed
        self.falling_speed += 0.2

    def jump(self):
        self.falling_speed = -8

    def draw(self, window):
        pygame.draw.circle(window, RED, (self.x, self.y), 20)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.y = random.randint(10, 590)
        self.width = 50
        self.gap_height = 200

    def move(self):
        self.x -= 3
        if self.x <= -self.width:
            self.x = 850
            self.y = random.randint(10, 590)

    def bird_collision(self, bird):
        if self.x < bird.x < self.x + self.width:
            if not (self.y < bird.y < self.y + self.gap_height):
                return True
        return False

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
        return self.bird.x, self.bird.y, self.bird.falling_speed, self.next_pipe.x, self.next_pipe.y

    def step(self, action):
        for pipe in self.pipes:
            pipe.move()
        self.bird.move(action)

        if not self.next_pipe == self.__get_next_pipe():
            self.next_pipe = self.__get_next_pipe()
            self.score += 1

        collision = self.next_pipe.bird_collision(self.bird)
        reward = 1

        if collision:
            self.done = True
            reward = -100

        state = (round(self.bird.x), round(self.bird.y), round(self.bird.falling_speed), self.next_pipe.x, self.next_pipe.y)

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
        

epsilon = 0.7

class Agent:

    def __init__(self):
        self.env = Game()
        self.done = self.env.done
        self.episodes = 10000
        self.q = defaultdict(lambda: [0, 0])

    def train(self):
        global epsilon
        rewards = [0 for _ in range(self.episodes)]
        for episode in range(self.episodes):
            state = self.env.reset()
            done = False
            while not done:
               
                epsilon -= 0.001
                old_state = state
                action = self.__get_action(state, epsilon)
                state, reward, done = self.env.step(action == 0)
                

                update_value = reward + self.q[old_state][action] * 0.9
                self.q[state][action] += update_value


                rewards[episode] += reward

            print(rewards[episode], episode)
        print(rewards[np.argmax(rewards)])
        print(epsilon)
        

    def __get_action(self, state, epsilon):
        if random.uniform(0, 1) > epsilon:
            return np.argmax(self.q[state])
        else:
            return np.random.choice([True, False], p=[0.01, 0.99])

agent = Agent()
agent.train()