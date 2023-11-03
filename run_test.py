import gym
# Register your custom environment
from gym.envs.registration import register

from stable_baselines3 import PPO

import gameenv

register(
    id='FlappyGame-v0',  # Unique identifier for your environment
    entry_point='gameenv:GameEnv',
)

# Create an instance of your custom environment
env = gym.make('FlappyGame-v0')

# Initialize the environment
observation = env.reset()

terminated = False

for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, terminated, info = env.step(action)

env.close()

# done = False
# while not done:
#     # Replace with your own logic for choosing actions
#     action = env.action_space.sample()  # Random action for demonstration

#     # Take a step in the environment
#     observation, reward, done, info, score = env.step(action)

#     # Optionally, render the environment for visualization
#     env.render()


# # Close the environment when you're done
# env.close()

# # Create an instance of your custom environment
# env = gym.make('FlappyGame-v0')

# model = PPO("MlpPolicy", env, verbose=1)  # Adjust policy and hyperparameters as needed

# # Train the model for 50,000 timesteps
# model.learn(total_timesteps=50000)

# # Save the trained model
# model.save("PPO_path")
