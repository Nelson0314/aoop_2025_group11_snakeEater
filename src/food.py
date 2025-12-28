import pygame
from .settings import FOOD_GROWTH, FOOD_RADIUS, FOOD_COLORS

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = 'generic'
        self.growthValue = 0
        self.radius = 0
        self.color = (255, 255, 255)

    def draw(self, screen, cameraX, cameraY, zoom):
        """
        畫出食物，當然也要減去鏡頭偏移量
        """
        screenX = (self.x - cameraX) * zoom
        screenY = (self.y - cameraY) * zoom
        
        radius = int(self.radius * zoom)
        # 避免半徑太小
        if radius < 1: radius = 1
        
        pygame.draw.circle(screen, self.color, (int(screenX), int(screenY)), radius)

class SmallFood(Food):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'small'
        self.growthValue = FOOD_GROWTH['small']
        self.radius = FOOD_RADIUS['small']
        self.color = FOOD_COLORS['small']

class MediumFood(Food):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'medium'
        self.growthValue = FOOD_GROWTH['medium']
        self.radius = FOOD_RADIUS['medium']
        self.color = FOOD_COLORS['medium']

class LargeFood(Food):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'large'
        self.growthValue = FOOD_GROWTH['large']
        self.radius = FOOD_RADIUS['large']
        self.color = FOOD_COLORS['large']