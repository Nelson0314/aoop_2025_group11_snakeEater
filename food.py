import pygame
from settings import FOOD_GROWTH, FOOD_RADIUS, FOOD_COLORS

class Food:
    def __init__(self, x, y, food_type):
        """
        :param x, y: 世界座標
        :param food_type: 字串 'small', 'medium', 或 'large'
        """
        self.x = x
        self.y = y
        self.type = food_type
        
        # 根據類型，從 settings 載入對應的屬性
        self.growth_value = FOOD_GROWTH[food_type] # 增加的長度
        self.radius = FOOD_RADIUS[food_type]       # 半徑
        self.color = FOOD_COLORS[food_type]        # 顏色
        
        # 建立一個矩形 (主要用於碰撞偵測的範圍概算，雖然我們是用圓形偵測)
        # 這裡的寬高設為直徑 (半徑*2)
        self.rect = pygame.Rect(x - self.radius, y - self.radius, 
                                self.radius * 2, self.radius * 2)

    def draw(self, screen, cameraX, cameraY):
        """
        畫出食物，當然也要減去鏡頭偏移量
        """
        screen_x = self.x - cameraX
        screen_y = self.y - cameraY
        
        pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), self.radius)