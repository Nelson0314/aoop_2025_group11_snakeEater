import pygame
import math
TILE_SIZE = 20
WIDTH = 1280
HEIGHT = 720

class Snake():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.head = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.body = [self.head]
        self.length = 1

    def draw(self, screen):
        for tile in self.body:
            pygame.draw.circle(screen, self.color, tile.center, 20, 0)

    def move(self):
        pass


class playerSnake(Snake):
    pass