import os
import pygame
import time
import signal
import sys

# Set SDL to use the dummy video driver (No window)
# This MUST be set before pygame.init()
os.environ["SDL_VIDEODRIVER"] = "dummy"

# Import settings and game classes
# Assuming this script is in the root directory of the project
from src.settings import *
from src.game import GAME
from src.mlAgent import config

def main():
    print("Initializing Headless Snake Agent Training...")

    # Initialize Pygame
    pygame.init()
    
    # Initialize a dummy screen (needed for some pygame internals even if not shown)
    # Using the dimensions from settings.py
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Initialize Clock (used for internal FPS counting in game.py, but we won't wait on it)
    clock = pygame.time.Clock()
    
    # Initialize Game in 'learn' mode
    # This sets up the agents, food, etc.
    game = GAME(screen, mode='learn', clock=clock)
    
    print(f"Game Initialized. Map Size: {MAP_WIDTH}x{MAP_HEIGHT}")
    print(f"Number of agents: {len(game.snakes)}")
    print("Starting training loop (Press Ctrl+C to stop)...")
    
    frames = 0
    start_time = time.time()
    
    running = True

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\nCtrl+C detected! Saving model and exiting...")
        game.agent.saveModel()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)

    try:
        while running:
            # 1. Handle basic events (Keep pygame event queue clear)
            # Necessary because some inputs might pile up, though in dummy mode likely minimal
            game.handleEvent()
            
            # 2. Update Game State
            # This handles movement, collision, AI logic, and learning steps
            game.update()
            
            # 3. NO DRAWING
            # We explicitly skip game.draw() to maximize speed
            
            # 4. Metrics & Logging
            frames += 1
            
            # Log progress every 1000 frames
            if frames % 10 == 0:
                elapsed = time.time() - start_time
                fps = frames / elapsed
                
                # Get some stats
                living_snakes = len(game.snakes)
                scores = [s.score for s in game.snakes]
                max_score = max(scores) if scores else 0
                avg_score = sum(scores) / len(scores) if scores else 0
                
                print(f"[Frame {frames}] FPS: {fps:.2f} | Snakes: {living_snakes} | "
                      f"Max Score: {max_score:.1f} | Avg Score: {avg_score:.1f}")
                
            # Optional: Automatic Save Backup handled inside game.update() via config.MODEL_SAVE_INTERVAL
            
    except Exception as e:
        print(f"An error occurred: {e}")
        game.agent.saveModel()
        raise

if __name__ == "__main__":
    main()
