import sys
import pygame
from src.game import GAME

WIDTH = 1280
HEIGHT = 720
FPS = 60
WINDOW_TITLE = "Slither"

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    
    # Start Screen / Menu
    from src import ui
    # Import Game Classes
    from simple_learn import SimpleGAME
    from strategy_demo import StrategyGAME
    
    # Loop to allow returning to menu (optional, but good UX)
    while True:
        # Show Menu and get selection
        mode = ui.show_menu(screen)
        
        game = None
        if mode == 'play':
             game = GAME(screen, mode='play', clock=pygame.time.Clock())
        elif mode == 'learn':
             game = GAME(screen, mode='learn', clock=pygame.time.Clock())
        elif mode == 'simple_learn':
             game = SimpleGAME(screen, clock=pygame.time.Clock())
        elif mode == 'demo':
             game = StrategyGAME(screen, clock=pygame.time.Clock())
        elif mode == 'QUIT':
             pygame.quit()
             sys.exit()
        
        if game:
            # Run Game Loop
            running = True
            clock = pygame.time.Clock()
            while running:
                # We need to catch QUIT or ESC inside game to break potentially
                # But game.handleEvent handles QUIT by sys.exit usually.
                # Let's trust game loop.
                try:
                    game.handleEvent()
                    game.update()
                    game.draw()
                    pygame.display.flip()
                    clock.tick(FPS)
                except SystemExit:
                    # If game exits, we might want to just quit or return to menu
                    # For now, let it exit fully as per original design
                    pygame.quit()
                    sys.exit()
                except Exception as e:
                    print(f"Game Loop Error: {e}")
                    running = False # Go back to menu on error?

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()