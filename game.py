import pygame
from snake import Snake, playerSnake
from food import Food
import random
from settings import *
import math


class GAME():
    def __init__(self, screen):
        self.screen = screen
        self.snakes = []
        self.food = []
        self.cameraX = 0
        self.cameraY = 0
        self.font = pygame.font.SysFont(None, 18)

        self.setUp()

    def setUp(self):
        xcentre = SCREEN_WIDTH / 2
        ycentre = SCREEN_HEIGHT / 2
        player = playerSnake(xcentre, ycentre, WHITE)
        self.snakes.append(player)

        for foodType, count in FOOD_COUNTS.items():
            for _ in range(count):
                self.spawnFood(foodType)

    def spawnFood(self, foodType):
        x = random.randint(20, MAP_WIDTH - 20)
        y = random.randint(20, MAP_HEIGHT - 20)
        
        newFood = Food(x, y, foodType)
        self.food.append(newFood)

    def handleEvent(self):
        pass

    def update(self):
        for snake in self.snakes:
            if isinstance(snake, playerSnake):
                snake.updateDirectionByMouse()
            self.checkCollision(snake)
            snake.move()

        self.cameraX = self.snakes[0].head.centerx - SCREEN_WIDTH / 2
        self.cameraY = self.snakes[0].head.centery - SCREEN_HEIGHT / 2

    def checkCollision(self, snake):
        for i in range(len(self.food) - 1, -1, -1):
            food = self.food[i]
            
            # 計算蛇頭跟食物的距離
            dx = snake.head.centerx - food.x
            dy = snake.head.centery - food.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            
            # 判斷標準：距離 < (蛇頭半徑 + 食物半徑)
            # TILE_SIZE//2 是蛇頭半徑
            if distance < (TILE_SIZE // 2) + food.radius:
                
                # 1. 蛇變長
                snake.grow(food.growth_value)
                
                # 2. 記錄這個食物的類型 (為了重生)
                eatenType = food.type
                
                # 3. 移除這個食物
                self.food.pop(i)
                
                # 4. 立刻補充一個同類型的食物，保持總量平衡
                self.spawnFood(eatenType)
    
    def drawGrid(self):
        """
        高效繪製網格背景。只繪製螢幕可見範圍內的網格。
        """
        # 計算螢幕左上角在世界座標中的哪個「行 (row)」和「列 (col)」開始
        # 這裡多減 1 是為了確保邊緣不會有閃爍的空隙
        start_col = int(self.cameraX // GRID_SIZE) - 1
        start_row = int(self.cameraY // GRID_SIZE) - 1

        # 計算螢幕需要畫多少行和列才能填滿
        cols_to_draw = SCREEN_WIDTH // GRID_SIZE + 4
        rows_to_draw = SCREEN_HEIGHT // GRID_SIZE + 4

        # 開始雙重迴圈繪製網格
        for row in range(start_row, start_row + rows_to_draw):
            for col in range(start_col, start_col + cols_to_draw):
                
                # 計算這個網格的世界座標 (左上角)
                tile_world_x = col * GRID_SIZE
                tile_world_y = row * GRID_SIZE

                # 【關鍵】檢查這個網格是否在 10000x10000 的地圖範圍內
                # 如果超出範圍，就不畫 (顯示底下的純黑色背景)
                if 0 <= tile_world_x < MAP_WIDTH and 0 <= tile_world_y < MAP_HEIGHT:
                    
                    # 計算螢幕座標
                    tile_screen_x = tile_world_x - self.cameraX
                    tile_screen_y = tile_world_y - self.cameraY
                    
                    # 決定顏色：黑灰相間的邏輯
                    # 如果 行號+列號 是偶數用顏色1，奇數用顏色2
                    if (row + col) % 2 == 0:
                        color = BLACK
                    else:
                        color = GRAY
                        
                    # 畫出這個網格矩形
                    pygame.draw.rect(self.screen, color, 
                                     (tile_screen_x, tile_screen_y, GRID_SIZE, GRID_SIZE))

    def draw(self):
        self.screen.fill(BLACK)
        self.drawGrid()
        for food in self.food:
            food.draw(self.screen, self.cameraX, self.cameraY)
        for snake in self.snakes:
            snake.draw(self.screen, self.cameraX, self.cameraY)
        
        playerHead = self.snakes[0].head
        coord = f"World: ({int(playerHead.centerx)}, {int(playerHead.centery)})"
        textSurface = self.font.render(coord, True, WHITE)
        self.screen.blit(textSurface, (10, 10))