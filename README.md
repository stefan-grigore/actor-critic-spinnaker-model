# SpiNNaker Demonstration

----

This repository contains an actor-critic implementation of a spiking neural network learning agent at different stages of development. The network was configured to solve a Gridworld inspired problem: the levels of a commercially available platform game, Super Meat Boy.

## randomSpikesDemonstration.py

This file contains one of the earliest versions of the implementation, which just executes actions randomly, each action being in a separate thread to the simulation thread.

## visionDemonstration.py

This file demonstrates the computer vision algorithm used for the environment, by highlighting where the character and the goal are located.

## spikesWithVisionInputDemonstration.py

This file contains the previous implementation, with the addition of the input from the environment, in the form of the location of the agent and the goal, which dictate what actions the agent should take.

## synchronousDemonstration.py

This file contains all components of the actor-critic model, with the implementation sending all spikes to the event database at the beginning of the simulation in the form of callbacks, restarting the simulation to get the weights of the actions and decide the next action after each learning episode.

## asynchronousDemonstration.py

This file contains the final implementation of the model, which runs the model and simulation in separate threads and decodes the actions by using first spike coding rather than stopping the simulation and reading the weights after each learning episode.
