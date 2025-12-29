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
        
        # 繪製發光效果
        # Glow radius should be larger than food
        glow_radius = int(radius * 2.0)
        glow_size = glow_radius * 2
        glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            
        # Draw a soft glow using the food's color
        r, g, b = self.color
        pygame.draw.circle(glow_surf, (r, g, b, 60), (glow_radius, glow_radius), glow_radius)
        pygame.draw.circle(glow_surf, (r, g, b, 100), (glow_radius, glow_radius), int(glow_radius * 0.6))

        glow_rect = glow_surf.get_rect(center=(int(screenX), int(screenY)))
        screen.blit(glow_surf, glow_rect, special_flags=pygame.BLEND_ADD)

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