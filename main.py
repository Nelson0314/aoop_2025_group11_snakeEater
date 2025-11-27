import sys
import pygame
from game import GAME

WIDTH = 1280
HEIGHT = 720
FPS = 60
WINDOW_TITLE = "Slither"

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    game = GAME(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            game.handleEvent()
    
        game.update()
        game.drawGrid()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()