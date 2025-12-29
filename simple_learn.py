import os
import pygame
import time
import signal
import sys

# Set SDL to use the dummy video driver (No window) - DISABLED for Visual Mode
# os.environ["SDL_VIDEODRIVER"] = "dummy"

# Import settings and game classes
from src.settings import *
from src.game import GAME
from src.snake import ComputerSnake, playerSnake
from src.mlAgent import config
from src.mlAgent.simple_agent import SimpleQLearningAgent
from src.mlAgent.simple_utils import getSimpleState

# --- Subclass GAME to override logic without touching src/game.py ---
class SimpleGAME(GAME):
    def __init__(self, screen, clock=None):
        # Call parent init with 'learn' mode to get basic setup
        super().__init__(screen, mode='learn', clock=clock)
        
        # OVERRIDE the agent with our Simple Agent
        print("Overriding Agent with SimpleQLearningAgent (4-State)...")
        # Reuse same actions [0..5]
        self.agent = SimpleQLearningAgent(actions=[0, 1, 2, 3, 4, 5])
        self.agent.loadModel() # Load simple_qTable.pkl
        
    def update(self):
        # Copy of the simplified update logic, but specifically using getSimpleState
        
        if self.state != 'playing':
            return

        # Auto-save model
        if not hasattr(self, 'frameCount'):
            self.frameCount = 0
        self.frameCount += 1
        if self.frameCount % config.MODEL_SAVE_INTERVAL == 0:
            self.agent.saveModel()

        # Update Spatial Grid
        self.spatialGrid.clear()
        for snake in self.snakes:
            self.spatialGrid.insert(snake)

        for snake in self.snakes:
            if isinstance(snake, playerSnake):
                snake.updateDirectionByMouse()
            elif isinstance(snake, ComputerSnake):
                # RL: Observe State using SIMPLE STATE
                snake.stateOld = getSimpleState(snake, self.snakes, self.food, MAP_WIDTH, MAP_HEIGHT)
                
                snake.scoreOld = snake.score
                # RL: Choose Action
                snake.action = self.agent.chooseAction(snake.stateOld)
                snake.performAction(snake.action)
            
            self.checkCollision(snake)
            snake.move()
            
        # Camera Update Logic (match game.py)
        if self.mode == 'learn': # Effectively always true here
            if len(self.snakes) > 0:
                 if self.cameraMode == 'god':
                     targetZoom = self.godViewZoom
                     self.zoom += (targetZoom - self.zoom) * 0.05
                     self.cameraX = MAP_WIDTH/2 - (SCREEN_WIDTH / self.zoom) / 2
                     self.cameraY = MAP_HEIGHT/2 - (SCREEN_HEIGHT / self.zoom) / 2
                 else: # Follow Mode
                     if self.spectatorSnake not in self.snakes:
                         self.spectatorSnake = self.snakes[0]
                     
                     targetSnake = self.spectatorSnake
                     targetZoom = 0.8
                     self.zoom += (targetZoom - self.zoom) * 0.05
                     self.cameraX = targetSnake.head.centerx - (SCREEN_WIDTH / self.zoom) / 2
                     self.cameraY = targetSnake.head.centery - (SCREEN_HEIGHT / self.zoom) / 2
            else:
                self.spectatorSnake = None
            
        # Snapshot snakes before death check to know who died
        snakes_before = set(self.snakes)
        self.checkDeaths()
        snakes_after = set(self.snakes)
        dead_snakes = snakes_before - snakes_after
        
        # RL: Learning Step
        
        # 1. Handle Dead Snakes (Terminal State)
        for snake in dead_snakes:
             if isinstance(snake, ComputerSnake) and hasattr(snake, 'stateOld') and hasattr(snake, 'action'):
                 # Death Reward
                 reward = config.REWARD_DEATH
                 snake.stateNew = snake.stateOld 
                 self.agent.learn(snake.stateOld, snake.action, reward, snake.stateNew)

        # 2. Handle Living Snakes
        for snake in self.snakes:
            if isinstance(snake, ComputerSnake) and hasattr(snake, 'stateOld'):
                # Reward Calculation
                reward = config.REWARD_SURVIVAL # +0.1
                if snake.score > snake.scoreOld:
                    reward = config.REWARD_EAT_FOOD # +50
                
                if snake.isBoosting:
                    reward += config.REWARD_BOOST_PENALTY

                # Wall Penalty Check (Crucial for preventing sticking)
                # Since move() clamps position, check if at boundary
                head = snake.head
                r = snake.radius
                if head.centerx <= r + 5 or head.centerx >= MAP_WIDTH - r - 5 or \
                   head.centery <= r + 5 or head.centery >= MAP_HEIGHT - r - 5:
                    reward += config.REWARD_WALL # -300

                # Learning
                if hasattr(snake, 'action'): # Ensure action was taken
                    # Observe New State
                    stateNew = getSimpleState(snake, self.snakes, self.food, MAP_WIDTH, MAP_HEIGHT)
                    
                    self.agent.learn(snake.stateOld, snake.action, reward, stateNew)

# ------------------------------------------------------------------

def main():
    print("Initializing Snake Agent Training (SIMPLE MODE - VISUAL)...")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Eater - Simple Learning Mode (4-State)")
    clock = pygame.time.Clock()
    
    # Use our Subclass
    game = SimpleGAME(screen, clock=clock)
    
    print(f"Game Initialized. Map Size: {MAP_WIDTH}x{MAP_HEIGHT}")
    print("Starting SIMPLE training loop...")
    
    frames = 0
    start_time = time.time()
    running = True

    def signal_handler(sig, frame):
        print("\nCtrl+C detected! Saving simple model and exiting...")
        game.agent.saveModel()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)

    try:
        while running:
            # Handle Events
            # We must pump the event queue or window will freeze
            # However, game.handleEvent() processes all events in queue effectively clearing it
            # So we should call it. But we also want to catch QUIT here if game doesn't?
            # game.handleEvent() handles QUIT by calling sys.exit(). Let's use it.
            
            game.handleEvent()
            
            game.update() # Uses our overridden simple update
            
            game.draw()   # Draw the game
            pygame.display.flip() # Update display
            clock.tick(60) # Cap FPS
            
            frames += 1
            if frames % 600 == 0: # Print less frequently
                elapsed = time.time() - start_time
                fps = frames / elapsed
                living = len(game.snakes)
                scores = [s.score for s in game.snakes]
                print(f"[SIMPLE] Frame {frames} | FPS: {fps:.1f} | Snakes: {living} | Max: {max(scores) if scores else 0}")
            
    except Exception as e:
        print(f"Error: {e}")
        game.agent.saveModel()
        raise
    except SystemExit:
        print("Exiting...")
        game.agent.saveModel()

if __name__ == "__main__":
    main()
