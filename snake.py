import pygame
import math
from settins import MAP_HEIGHT, MAP_WIDTH, TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class Snake():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.head = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.length = 20 
        self.body = []
        for i in range(self.length):
            self.body.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
        self.head = self.body[0]
        self.direction = pygame.Vector2(1, 0)
        self.speed = 5
        self.spacing = 15

    def draw(self, screen, cameraX, cameraY):
        for tile in self.body:
            screenCenterX = tile.centerx - cameraX
            screenCenterY = tile.centery - cameraY

            pygame.draw.circle(screen, self.color, (screenCenterX, screenCenterY), 10, 0)

    def move(self):
        head = self.body[0]
        
        newX = head.centerx + self.direction.x * self.speed
        newY = head.centery + self.direction.y * self.speed
        radius = TILE_SIZE // 2
        if newX - radius < 0: 
            newX = radius
        elif newX + radius > MAP_WIDTH: 
            newX = MAP_WIDTH - radius
        if newY - radius < 0: 
            newY = radius
        elif newY + radius > MAP_HEIGHT: 
            newY = MAP_HEIGHT - radius
        head.center = (newX, newY)

        while len(self.body) < self.length:
            self.body.append(pygame.Rect(head.x, head.y, TILE_SIZE, TILE_SIZE))

        for i in range(1, len(self.body)):
            leader = self.body[i-1]
            follower = self.body[i]

            dx = leader.centerx - follower.centerx
            dy = leader.centery - follower.centery
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 0:
                scale = self.spacing / dist
                target_x = leader.centerx - dx * scale
                target_y = leader.centery - dy * scale
                follower.centerx = target_x
                follower.centery = target_y

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