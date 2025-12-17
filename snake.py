import pygame
import math
from settings import MAP_HEIGHT, MAP_WIDTH, TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
class Snake():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.head = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.score = 0
        self.direction = pygame.Vector2(1, 0)
        self.speed = 5
        # self.spacing = 15 (Removed, now a property)
        
        self.body = []
        for i in range(self.length):
            # 初始時讓身體往下方延伸，避免全部疊在一起
            spawnX = x 
            spawnY = y + i * self.spacing
            self.body.append(pygame.Rect(spawnX, spawnY, TILE_SIZE, TILE_SIZE))
        self.head = self.body[0]

    @property
    def length(self):
        # 蛇的長度改成 10 + sqrt(score)
        return 10 + int(math.sqrt(self.score))

    @property
    def radius(self):
        # 根據長度決定半徑: radius = length * 1.8
        # 設定一個最小值以免太小看不到 (例如 1)
        return int(max(1, self.length * 1.8))

    @property
    def spacing(self):
        # body每一節的間距也要動態調整成 radius
        return self.radius

    def draw(self, screen, cameraX, cameraY, zoom):
        for tile in self.body:
            screenCenterX = (tile.centerx - cameraX) * zoom
            screenCenterY = (tile.centery - cameraY) * zoom

            radius = int(self.radius * zoom)
            if radius < 1: radius = 1

            pygame.draw.circle(screen, self.color, (screenCenterX, screenCenterY), radius, 0)

    def grow(self, amount=1): 
        # 吃食物增加分數
        self.score += amount

    def move(self):
        head = self.body[0]
        
        newX = head.centerx + self.direction.x * self.speed
        newY = head.centery + self.direction.y * self.speed
        
        # 使用動態半徑進行邊界檢查
        radius = self.radius 
        
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
                targetX = leader.centerx - dx * scale
                targetY = leader.centery - dy * scale
                follower.centerx = targetX
                follower.centery = targetY

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

class ComputerSnake(Snake):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.angle = 0

    def updateDirection(self):
        # 簡單的原地轉圈邏輯
        self.angle += 5
        if self.angle >= 360:
            self.angle -= 360
        
        # 將角度轉換為方向向量
        rad = math.radians(self.angle)
        self.direction = pygame.Vector2(math.cos(rad), math.sin(rad))