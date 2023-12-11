# flappy_bird_CI

This repository implements the [Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/) API with a Flappy Bird environment compatible with [Gymnasium](https://gymnasium.farama.org/index.html) used in [flappy-bird-gym](https://github.com/Talendar/flappy-bird-gym/tree/main) by [@Talendar](https://github.com/Talendar).

There are two scripts, one containing the code to train a model and the other containing code to run a specified model.

## Usage
Complete all of the necessary installs for Gymnasium, Stable-Baselines3, and flappy-bird-gym. After which you can run the train script with a 
specified number of timesteps and run the load script depending on where the training found the best reward. This can be done with the 
tensorboard --logs=(name of log file). The log file is created during the training and the name can be modified in the first script.
