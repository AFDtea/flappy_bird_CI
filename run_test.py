import gym
# Register your custom environment
from gym.envs.registration import register

from stable_baselines3 import PPO

register(
    id='FlappyGame-v0',  # Unique identifier for your environment
    entry_point='gameenv:GameEnv',
)

# Create an instance of your custom environment
env = gym.make('FlappyGame-v0')

model = PPO("MlpPolicy", env, verbose=1)  # Adjust policy and hyperparameters as needed

# Train the model for 50,000 timesteps
model.learn(total_timesteps=50000)

# Save the trained model
model.save("PPO_path")

# Close the environment when you're done
env.close()
