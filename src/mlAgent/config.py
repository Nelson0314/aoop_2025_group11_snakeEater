# Machine Learning Configuration

import os

# Q-Learning Hyperparameters
LEARNING_RATE = 0.15       # alpha: How much new information overrides old information (0.0 = nothing, 1.0 = full override)
DISCOUNT_FACTOR = 0.9     # gamma: Importance of future rewards (0.0 = short-sighted, 1.0 = long-term planning)
EPSILON = 0.1             # epsilon: Exploration rate (probability of choosing a random action)

# Rewards
REWARD_SURVIVAL = 0.1     # Reward for every frame the snake survives
REWARD_EAT_FOOD = 50      # Reward for eating food
REWARD_DEATH = -200      # Penalty for hitting another snake
REWARD_WALL = -300       # Penalty for hitting the wall
REWARD_KILL = 0        # Reward for causing another snake to die
REWARD_BOOST_PENALTY = -0.05 # Penalty for using boost (score decrease)

# Training settings
MODEL_SAVE_INTERVAL = 600 # Save the Q-table every N frames
MODEL_SAVE_FILE = os.path.join("mlAgent", "qTable.pkl")
MODEL_LOAD_FILE = os.path.join("mlAgent", "qTable_trained.pkl")

# Action settings
TURN_ANGLE = 15           # Degrees to turn left or right per action
