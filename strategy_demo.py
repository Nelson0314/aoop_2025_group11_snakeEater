import os
import pygame
import sys
import random

# Import settings and game classes
from src.settings import *
from src.game import GAME
from src.snake import ComputerSnake, playerSnake
from src.strategies import RandomStrategy, SimpleAIStrategy, AdvancedAIStrategy

# --- Subclass GAME to use Strategy Pattern ---
class StrategyGAME(GAME):
    def __init__(self, screen, clock=None):
        # Initialize as 'learn' mode but we will override agent logic
        super().__init__(screen, mode='learn', clock=clock)
        
        # Instantiate Strategies (Flyweight / Singleton-ish usage)
        self.strat_random = RandomStrategy()
        self.strat_simple = SimpleAIStrategy()
        self.strat_advanced = AdvancedAIStrategy()
        
        print("\n--- Strategy Pattern Demo ---")
        print("RED Snake   = Random Strategy (Dumb)")
        print("BLUE Snake  = Simple AI Strategy (4-State)")
        print("GREEN Snake = Advanced AI Strategy (12-State)")
        
        # Override Snakes with Strategy Assignment
        self.snakes = []
        self.spawn_strategy_snakes()

    def spawn_strategy_snakes(self):
        # Clears old snakes and spawns new ones with specific strategies
        self.snakes = []
        
        # 1. Advanced AI (Green) - The "Smart" one
        for _ in range(15):
             s = ComputerSnake(random.randint(100, MAP_WIDTH-100), random.randint(100, MAP_HEIGHT-100), (0, 255, 0)) # Green
             s.strategy = self.strat_advanced
             if self.assets['skins']:
                 # Pick a random skin to look nice
                 skin_idx = random.randint(0, len(self.assets['skins'])-1)
                 s.set_skin(self.assets['skins'][skin_idx][0], self.assets['skins'][skin_idx][1])
             self.snakes.append(s)
             
        # 2. Simple AI (Blue) - The "Learning" one
        for _ in range(15):
             s = ComputerSnake(random.randint(100, MAP_WIDTH-100), random.randint(100, MAP_HEIGHT-100), (0, 100, 255)) # Blue
             s.strategy = self.strat_simple
             if self.assets['skins']:
                 skin_idx = random.randint(0, len(self.assets['skins'])-1)
                 s.set_skin(self.assets['skins'][skin_idx][0], self.assets['skins'][skin_idx][1])
             self.snakes.append(s)
             
        # 3. Random AI (Red) - The "Dumb" one
        for _ in range(15):
             s = ComputerSnake(random.randint(100, MAP_WIDTH-100), random.randint(100, MAP_HEIGHT-100), (255, 50, 50)) # Red
             s.strategy = self.strat_random
             if self.assets['skins']:
                 skin_idx = random.randint(0, len(self.assets['skins'])-1)
                 s.set_skin(self.assets['skins'][skin_idx][0], self.assets['skins'][skin_idx][1])
             self.snakes.append(s)

        # Clear spatial grid to be safe
        self.spatialGrid.clear()
        for s in self.snakes:
            self.spatialGrid.insert(s)

    def update(self):
        # Override update to use Strategy Pattern
        if self.state != 'playing':
            return
            
        # Update Spatial Grid
        self.spatialGrid.clear()
        for snake in self.snakes:
            self.spatialGrid.insert(snake)
            
        game_context = (self.snakes, self.food, self.spatialGrid)

        for snake in self.snakes:
            if isinstance(snake, ComputerSnake):
                # STRATEGY PATTERN IN ACTION:
                # Delegate decision making to the strategy object
                if hasattr(snake, 'strategy'):
                    snake.action = snake.strategy.decide_action(snake, game_context)
                    snake.performAction(snake.action)
                else:
                    # Fallback for any unassigned snake
                    pass 
            
            # Physics & Movement (Common to all)
            self.checkCollision(snake)
            snake.move()
            
            # Wall Penalty Check (Borrowed from simple_learn fixes)
            head = snake.head
            r = snake.radius
            if head.centerx <= r + 5 or head.centerx >= MAP_WIDTH - r - 5 or \
               head.centery <= r + 5 or head.centery >= MAP_HEIGHT - r - 5:
                # Apply penalty? Strategy usually doesn't handle reward in execution phase
                # But for demo visuals, we just want them to move.
                pass 

        # Handling Deaths
        self.checkDeaths()
        
        # Camera Update Logic (Borrowed from simple_learn / game.py)
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
            
        # Replenish snakes if they die out, to keep the demo alive?
        # Let's simple check count. If low, spawn more.
        if len(self.snakes) < 10:
             self.spawn_strategy_snakes()


def main():
    print("Initializing Strategy Pattern Demo Class...")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Eater - Strategy Pattern Demo (Red=Random, Blue=Simple, Green=Smart)")
    clock = pygame.time.Clock()
    
    # Use StrategyGAME
    game = StrategyGAME(screen, clock=clock)
    
    print("Starting Strategy Demo loop...")
    
    running = True
    try:
        while running:
            # Handle Events
            # GAME.handleEvent already processes the event queue.
            # We catch QUIT inside handleEvent or can check if game exits.
            # But game.handleEvent exits sys directly on QUIT, so we are fine.
            
            game.handleEvent() # Main event pump
            game.update()
            game.draw()
            pygame.display.flip()
            clock.tick(60)
            
    except Exception as e:
        print(f"Error: {e}")
        raise

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
