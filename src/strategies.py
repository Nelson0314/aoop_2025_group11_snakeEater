import random
import pygame
from .mlAgent.simple_agent import SimpleQLearningAgent
from .mlAgent.simple_utils import getSimpleState
from .mlAgent.qAgent import QLearningAgent
from .mlAgent.utils import getState
from .mlAgent import config
from .settings import MAP_WIDTH, MAP_HEIGHT

# --- Interface (Abstract Base Class) ---
class SnakeStrategy:
    def decide_action(self, snake, game_context):
        """
        Given the snake and game context (snakes, food, grid),
        decide the next action (0-5).
        """
        raise NotImplementedError

# --- Concrete Strategy 1: Random (Dumb) ---
class RandomStrategy(SnakeStrategy):
    def decide_action(self, snake, game_context):
        # 0: Straight, 1: Left, 2: Right (Ignore Boost 3-5 for dumb snake)
        return random.randint(0, 2)

# --- Concrete Strategy 2: Simple AI (4-State) ---
class SimpleAIStrategy(SnakeStrategy):
    def __init__(self):
        self.agent = SimpleQLearningAgent(actions=[0, 1, 2, 3, 4, 5])
        self.agent.loadModel() # Load simple_qTable.pkl
        
    def decide_action(self, snake, game_context):
        snakes, food, spatial_grid = game_context
        # Use Simple State Observation
        state = getSimpleState(snake, snakes, food, MAP_WIDTH, MAP_HEIGHT)
        snake.stateOld = state # Store for potential learning (if we were learning)
        return self.agent.chooseAction(state)

# --- Concrete Strategy 3: Advanced AI (12-State) ---
class AdvancedAIStrategy(SnakeStrategy):
    def __init__(self):
        self.agent = QLearningAgent(actions=[0, 1, 2, 3, 4, 5])
        self.agent.loadModel() # Load qTable_trained.pkl
        
    def decide_action(self, snake, game_context):
        snakes, food, spatial_grid = game_context
        # Use Advanced State Observation
        state = getState(snake, snakes, food, MAP_WIDTH, MAP_HEIGHT, spatial_grid)
        snake.stateOld = state
        return self.agent.chooseAction(state)
