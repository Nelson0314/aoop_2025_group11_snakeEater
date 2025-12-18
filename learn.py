import sys
import pygame
from game import GAME

WIDTH = 1280
HEIGHT = 720
FPS = 60
WINDOW_TITLE = "Slither AI Training - Spectator Mode"

def main():
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
            status = f"Spectating: Snake {game.spectatorIndex} (A/D to switch)"
        else:
            status = "God View (G to toggle)"
            
        caption = f"{WINDOW_TITLE} | {status} | FPS: {int(clock.get_fps())}"
        pygame.display.set_caption(caption)

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
