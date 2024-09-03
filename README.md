# Super Mario AI

## Overview
The Super Mario AI project focuses on developing an intelligent agent that can navigate and complete levels in the classic Super Mario game. The AI is built using Genetic Algorithms, which evolve the neural network parameters over time to optimize Mario's behavior and decision-making strategies.

## Features
- **Genetic Algorithms**: The core of the project is the implementation of Genetic Algorithms, which evolve the neural network controlling Mario. This approach allows the AI to learn and adapt to the complexities of each level by optimizing its performance through generations.
- **Neural Network Evolution**: The AI's neural network parameters, such as weights and biases, are evolved over multiple generations, improving Mario's ability to navigate complex environments and avoid obstacles.
- **Fitness Function**: A custom fitness function evaluates Mario's performance based on various criteria, including the distance traveled, enemies defeated, and time taken to complete the level. The fitness function guides the evolution process by selecting the most successful strategies for reproduction.
- **Complex Level Navigation**: The AI is designed to handle various levels of increasing difficulty, adapting its strategies to overcome new challenges, such as more complex terrain, enemies, and level designs.

## Project Structure
- `genetic_algorithm.py`: Contains the implementation of the Genetic Algorithm, including selection, crossover, and mutation processes.
- `neural_network.py`: Defines the neural network architecture used by the AI to control Mario's movements and actions.
- `fitness_evaluation.py`: Implements the fitness function that evaluates the performance of each AI agent during gameplay.
- `mario_simulation.py`: The main script that runs the simulation, applying the evolved neural network parameters to control Mario in the game environment.
- `level_data.py`: Stores the data for different levels, including terrain, enemy placement, and other game elements that Mario must navigate.
