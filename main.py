import pygame
import numpy as np
from collections import defaultdict
import pickle
from FlappyBird import Game    

learning_rate = 0.9
FPS = 60

class Agent:

    def __init__(self):
        self.epsilon = 0.8
        self.env = Game()
        self.episodes = 1000000
        self.q = defaultdict(lambda: [0, 0])
        self.clock = pygame.time.Clock()


    def load(self):
        try: 
            with open("qlearning.b", "rb") as file:
                print("File was found")
                for key, value in pickle.load(file).items():
                    self.q[key] = value
        except FileNotFoundError:
            with open("qlearning.b", "w") as file:
                print("File was created")


    def train(self):
        self.load()
        scores = []
        for episode in range(self.episodes):
            
            done = False
            state = self.env.reset()
            while not done:
                action = self.__get_action(state)
                new_state, reward, done = self.env.step(action)

                current_q = self.q[state][action]
                next_max_q = np.max(self.q[new_state])
                new_q = current_q + learning_rate * (reward + 0.95 * next_max_q - current_q)

                self.q[state][action] = new_q

                state = new_state
            scores.append(self.env.score)
            if episode % 100 == 0:
                print(episode, ": ", np.mean(scores[-100:]))
            if episode % 1000 == 0:
                with open("qlearning.b", "wb") as file:
                    pickle.dump(dict(self.q), file)

                
    def test(self):
        done = False
        state = self.env.reset()
        self.epsilon = 0
        self.load()


        while not done:
            action = self.__get_action(state)
            new_state, reward, done = self.env.step(action)
            state = new_state
            self.clock.tick(FPS)
            self.env.render()

    def __get_action(self, state):
        self.epsilon -= 0.0001
        if np.random.uniform(0, 1) >  self.epsilon:
            return np.argmax(self.q[state])
        else:
            return np.random.choice([1, 0])

agent = Agent()
agent.train()
agent.test()