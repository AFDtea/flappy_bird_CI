

import gymnasium as gym
import flappy_bird_gymnasium
from stable_baselines3 import PPO
import os
import numpy as np



env = gym.make("LunarLander-v2", render_mode="rgb_array")
env.reset()
check_env(env)

models_dir = "models/PPO"
model_path = (f"{models_dir}/210000.zip")

model = PPO.load(model_path, env = env)

#make sure it is in eval

episodes = 10


for ep in range(episodes):
    obs = env.reset()
    done = False
    print(f"Episode {ep + 1}")
    while not done:
        env.render()
        model.predict(obs)
    #     print(f"Action: {action}")
        
    #     obs, reward, done, info = env.step(action)
    #     print(f"Observation: {obs}")
    #     print(f"Reward: {reward}")
    # print("Episode finished\n")

    # Enjoy trained agent



env.close()
