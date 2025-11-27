import pygame
import math
from settins import MAP_HEIGHT, MAP_WIDTH, TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class Snake():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.head = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.body = [self.head]
        self.length = 5
        self.direction = pygame.Vector2(1, 0)
        self.speed = 40

    def draw(self, screen, cameraX, cameraY):
        for tile in self.body:
            screenCenterX = tile.centerx - cameraX
            screenCenterY = tile.centery - cameraY

            pygame.draw.circle(screen, self.color, (screenCenterX, screenCenterY), 20, 0)

    def move(self):
        head = self.body[0]
        
        newX = head.centerx + self.direction.x * self.speed
        newY = head.centery + self.direction.y * self.speed
        finalX = head.centerx
        finalY = head.centery
        radius = TILE_SIZE // 2
        if newX - radius > 0 and newX + radius < MAP_WIDTH:
            finalX = newX
        if newY - radius > 0 and newY + radius < MAP_HEIGHT:
            finalY = newY
        newHead = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
        newHead.center = (finalX, finalY)
        self.body.insert(0, newHead)
        self.head = newHead
        if len(self.body) > self.length:
            self.body.pop()

class playerSnake(Snake):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

    def updateDirectionByMouse(self):
        mouseX, mouseY = pygame.mouse.get_pos()

        dirX = mouseX - SCREEN_WIDTH / 2
        dirY = mouseY - SCREEN_HEIGHT / 2
        length = (dirX ** 2 + dirY ** 2) ** 0.5
        if length > 0:
            dirX = dirX / length
            dirY = dirY / length

        self.direction = pygame.Vector2(dirX, dirY)