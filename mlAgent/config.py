# Machine Learning Configuration

import os

# Q-Learning Hyperparameters
LEARNING_RATE = 0.15       # alpha: How much new information overrides old information (0.0 = nothing, 1.0 = full override)
DISCOUNT_FACTOR = 0.9     # gamma: Importance of future rewards (0.0 = short-sighted, 1.0 = long-term planning)
EPSILON = 0.1             # epsilon: Exploration rate (probability of choosing a random action)

# Rewards
REWARD_SURVIVAL = 0.1     # Reward for every frame the snake survives
REWARD_EAT_FOOD = 50      # Reward for eating food
REWARD_DEATH = -100       # Penalty for hitting a wall or another snake
REWARD_KILL = 250         # Reward for causing another snake to die

# Training settings
MODEL_SAVE_INTERVAL = 500 # Save the Q-table every N frames
MODEL_FILE_NAME = os.path.join("mlAgent", "qTable.pkl")

# Action settings
TURN_ANGLE = 15           # Degrees to turn left or right per action
