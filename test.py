import gym

env = gym.make("Mountain-Car-v0")
env.reset()

done = False

while not done:
    action = 2
    new_state, reward, done, = env.step(action)
    env.render()

env.close()