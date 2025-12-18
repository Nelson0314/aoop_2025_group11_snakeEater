import sys
import os
import pygame
from game import GAME
from mlAgent import config

WIDTH = 1280
HEIGHT = 720
FPS = 240
WINDOW_TITLE = "Slither AI Training - Spectator Mode"

def main():
    # Remove existing model for fresh training
    if os.path.exists(config.MODEL_FILE_NAME):
        try:
            os.remove(config.MODEL_FILE_NAME)
            print(f"Deleted existing model: {config.MODEL_FILE_NAME}")
        except OSError as e:
            print(f"Error deleting model: {e}")

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    # Initialize Game in 'learn' mode
    # - No player snake
    # - AI snakes only
    # - Learning enabled
    # - Spectator camera
    game = GAME(screen, mode='learn')

    running = True
    while running:
        # Pass events to game for spectator controls
        
        # We need to handle quit here or inside game, 
        # but game.handleEvent handles quit too.
        # Let's keep main loop clean.
        
        game.handleEvent()
        game.update()
        game.draw()
        
        # Display instructions
        if game.cameraMode == 'follow':
            try:
                # Try to find current index for display, default to ? if trouble
                idx = game.snakes.index(game.spectatorSnake) if game.spectatorSnake in game.snakes else "?"
            except:
                idx = "?"
            status = f"Spectating: Snake {idx} (A/D to switch)"
        else:
            status = "God View (G to toggle)"
            
        # Calculate training interval
        current_interval = 0
        if hasattr(game, 'frameCount'):
            current_interval = game.frameCount // config.MODEL_SAVE_INTERVAL
            
        caption = f"{WINDOW_TITLE} | {status} | Interval: {current_interval} | FPS: {int(clock.get_fps())}"
        pygame.display.set_caption(caption)

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
