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
        pass

    def checkCollision(self):
        pass

    def draw(self):
        self.screen.fill(BLACK)

        for snake in self.snakes:
            snake.draw(self.screen)

    