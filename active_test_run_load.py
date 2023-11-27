

import gymnasium as gym
import flappy_bird_gymnasium
from stable_baselines3 import PPO
import os
import numpy as np



env = gym.make("FlappyBird-v0", render_mode="human")
env.reset()

models_dir = "models/PPO"
model_path = (f"{models_dir}/200000.zip")

model = PPO.load(model_path, env = env)

#make sure it is in eval

episodes = 10


for ep in range(episodes):
    obs, info = env.reset()
    terminated = False
    print(f"Episode {ep + 1}")
    while not terminated:
        env.render()
        action, _ = model.predict(obs)
        # print(f"Action: {action}")
        
        obs, reward, terminated, truncated, info = env.step(action)
        # print(f"Observation: {obs}")
        # print(f"Reward: {reward}")
    print("Episode finished\n")

    # Enjoy trained agent



env.close()
