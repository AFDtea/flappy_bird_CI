import gym
from gym import spaces
import numpy as np
from game import FlappyGame
import pygame

class GameEnv(gym.Env):
    def __init__(self):
        self.render_mode = None
        self.action_space  = spaces.Discrete(1)
        # Third value is bird_x which technically doesn't change
        self.observation_space = spaces.Box(low=np.array([115, 0, 0, 0]), high=np.array([125, 800, 800, 800]), dtype=np.float32)
        self.game = FlappyGame()
   
    def step(self, action):
        observation, reward, done, info, score = self.game.play_step(action)
        if(score > 1):
            print(score)
        return observation, reward, done, info
    
    def reset(self):
        observation, info = self.game.reset()
        print(observation)
        return observation, info

    def close(self):
        pygame.quit()



# need to make the observation part in game.py
    # need to add it to the init, play_step, and reset

# Need to add a render function to work with gym

# Youtube comment on how to run it
    # I just tried and understood, first you should train it with:

    # env.render_mode = None
    # model.learn(total_timesteps=50000)

    # then you should save the model with:

    # model.save(PPO_path)

    # and after that to see how it trained you can use same: 

    # env.render_mode = 'human'
    # model.learn(total_timesteps=200)