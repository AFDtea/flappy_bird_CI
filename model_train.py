import gymnasium as gym
import flappy_bird_gymnasium
from stable_baselines3 import A2C
import os

# creating folders for the logs and models
models_dir = "models/A2C"
logdir = "logs"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

# loading flappybird environment
env = gym.make("FlappyBird-v0")

# defining the model to be trained
model = A2C("MlpPolicy", env, verbose=1, tensorboard_log=logdir)

# training the model for the specified timesteps
TIMESTEPS = 10000
for i in range(1,130):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="A2C")
    model.save(f"{models_dir}/{TIMESTEPS*i}")


