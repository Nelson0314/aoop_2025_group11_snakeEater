import pygame
from snake import Snake, playerSnake
import random

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class GAME():
    def __init__(self, screen):
        self.screen = screen
        self.snakes = []
        self.cameraX = 0
        self.cameraY = 0
        self.font = pygame.font.SysFont(None, 18)

        self.setUp()

    def setUp(self):
        xcentre = SCREEN_WIDTH / 2
        ycentre = SCREEN_HEIGHT / 2
        player = playerSnake(xcentre, ycentre, WHITE)
        self.snakes.append(player)

    def spawnFood(self):
        pass

    def handleEvent(self):
        pass

    def update(self):
        for snake in self.snakes:
            if isinstance(snake, playerSnake):
                snake.updateDirectionByMouse()
            
            snake.move()

        self.cameraX = self.snakes[0].head.centerx - SCREEN_WIDTH / 2
        self.cameraY = self.snakes[0].head.centery - SCREEN_HEIGHT / 2

    def checkCollision(self):
        pass

    def draw(self):
        self.screen.fill(BLACK)    
        for snake in self.snakes:
            snake.draw(self.screen, self.cameraX, self.cameraY)
        
        playerHead = self.snakes[0].head
        coord = f"World: ({int(playerHead.centerx)}, {int(playerHead.centery)})"
        textSurface = self.font.render(coord, True, WHITE)
        self.screen.blit(textSurface, (10, 10))