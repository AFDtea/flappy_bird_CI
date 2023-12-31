import gymnasium as gym
import flappy_bird_gymnasium
from stable_baselines3 import PPO

# loading the FlappyBird environment
env = gym.make("FlappyBird-v0", render_mode="human")
env.reset()

# loading the model's weights with the best performance
models_dir = "models/palm_PPO_2"
model_path = (f"{models_dir}/7990000.zip")

model = PPO.load(model_path, env = env)

# displaying the model running 10 times
episodes = 10
for ep in range(episodes):
    obs, info = env.reset()
    terminated = False
    print(f"Episode {ep + 1}")
    while not terminated:
        env.render()
        action, _ = model.predict(obs)
        
        obs, reward, terminated, truncated, info = env.step(action)
    print("Episode finished\n")

env.close()
