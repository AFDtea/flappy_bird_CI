import torch
import random
import numpy as np
from collections import deque
from game import FlappyGame
#from model import Linear_QNet, QTrainer
#from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 10
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = None # TODO
        self.trainer = None # TODO 


    def get_state(self, game):
        bird_pos = game.playerMidPos
        m_pipe_pos = game.pipeMidPos
        bird_x = game.horizontal
        pipe_x = game.pipe[0]['x']

        state = [
            # below lower pipe
            bird_pos > m_pipe_pos,

            # above upper pipe
            bird_pos < m_pipe_pos,

            # Danger ground
            (bird_pos > 335),

            # Danger pipe
            pipe_x < (bird_x + 30),

            # Flapped
            game.bird_flapped
            ]

        return np.array(state, dtype=int)

    # def remember(self, state, action, reward, next_state, done):
    #     self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    # def train_long_memory(self):
    #     if len(self.memory) > BATCH_SIZE:
    #         mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
    #     else:
    #         mini_sample = self.memory

    #     states, actions, rewards, next_states, dones = zip(*mini_sample)
    #     self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    # def train_short_memory(self, state, action, reward, next_state, done):
    #     self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        if random.randint(0 , 1) == 0:
            final_move = 0
        else:
            final_move = 1

        return 1


# def train():
#     plot_scores = []
#     plot_mean_scores = []
#     total_score = 0
#     record = 0
#     agent = Agent()
#     game = FlappyGame()
#     while True:
#         # get old state
#         state_old = agent.get_state(game)

#         # get move
#         final_move = agent.get_action(state_old)

#         # perform move and get new state
#         reward, done, score = game.play_step(final_move)
#         state_new = agent.get_state(game)

#         # train short memory
#         agent.train_short_memory(state_old, final_move, reward, state_new, done)

#         # remember
#         agent.remember(state_old, final_move, reward, state_new, done)

#         if done:
#             # train long memory, plot result
#             game.reset()
#             agent.n_games += 1
#             agent.train_long_memory()

#             if score > record:
#                 record = score
#                 # agent.model.save()

#             print('Game', agent.n_games, 'Score', score, 'Record:', record)

            # plot_scores.append(score)
            # total_score += score
            # mean_score = total_score / agent.n_games
            # plot_mean_scores.append(mean_score)
            # plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    agent = Agent()
    game = FlappyGame()

    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        # print(agent.get_state(game))