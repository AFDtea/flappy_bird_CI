# flappy_bird_CI

This repository implements the Stable-Baselines3 API with a Flappy Bird game compaitble with Gymnasium used in flappy-bird-gym by @Talendar.

There are two scripts, one containing the code to train a model and the other containing code to run a specified model.

##Usage
Complete all of the necessary installs for Gymnasium, Stable-Baselines3, and flappy-bird-gym. After which you can run the train script with a 
specified number of timesteps and run the load scriptdepending on where the training found the best reward. This can be done with the tensorboard --logs= 
and the name of the file containing the logs acquired while training the model.
