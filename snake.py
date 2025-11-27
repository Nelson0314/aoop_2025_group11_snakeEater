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
        self.length = 5
        self.direction = pygame.Vector2(1, 0)
        self.speed = 1

    def draw(self, screen, cameraX, cameraY):
        for tile in self.body:
            screenCenterX = tile.centerx - cameraX
            screenCenterY = tile.centery - cameraY

            pygame.draw.circle(screen, self.color, (screenCenterX, screenCenterY), 20, 0)

    def move(self):
        head = self.body[0]
        
        newX = head.centerx + self.direction.x * self.speed
        newY = head.centery + self.direction.y * self.speed

        radius = TILE_SIZE // 2
        
        if newX < radius:
            newX = radius
        elif newX > MAP_WIDTH - radius:
            newX = MAP_WIDTH - radius
            
        # 限制 Y 軸
        if newY < radius:
            newY = radius
        elif newY > MAP_HEIGHT - radius:
            newY = MAP_HEIGHT - radius

        newHead = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
        newHead.center = (newX, newY)
        self.body.insert(0, newHead)
        self.head = newHead
        if len(self.body) > self.length:
            self.body.pop()

class playerSnake(Snake):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

    def updateDirectionByMouse(self):
        mouseX, mouseY = pygame.mouse.get_pos()

        dirX = mouseX - WIDTH / 2
        dirY = mouseY - HEIGHT / 2
        length = (dirX ** 2 + dirY ** 2) ** 0.5
        if length > 0:
            dirX = dirX / length
            dirY = dirY / length

        self.direction = pygame.Vector2(dirX, dirY)