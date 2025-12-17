import pygame
from snake import Snake, playerSnake, ComputerSnake
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
        self.large_font = pygame.font.SysFont(None, 72) # 大字體用於標題
        
        self.state = 'playing' # 'playing' or 'game_over'
        self.zoom = 1.0

        self.setUp()

    def setUp(self):
        xcentre = SCREEN_WIDTH / 2
        ycentre = SCREEN_HEIGHT / 2
        player = playerSnake(xcentre, ycentre, WHITE)
        self.snakes.append(player)

        # 這裡加入電腦蛇 (紅色的)
        for _ in range(10):
            # 隨機位置
            cx = random.randint(100, MAP_WIDTH - 100)
            cy = random.randint(100, MAP_HEIGHT - 100)
            # 紅色
            computer = ComputerSnake(cx, cy, (255, 0, 0))
            self.snakes.append(computer)

        for foodType, count in FOOD_COUNTS.items():
            for _ in range(count):
                self.spawnFood(foodType)

    def spawnFood(self, foodType):
        x = random.randint(20, MAP_WIDTH - 20)
        y = random.randint(20, MAP_HEIGHT - 20)
        
        newFood = Food(x, y, foodType)
        self.food.append(newFood)

    def handleEvent(self):
        keys = pygame.key.get_pressed()
        if self.state == 'game_over':
            if keys[pygame.K_r]:
                self.restartGame()

    def restartGame(self):
        self.snakes = []
        self.food = []
        self.state = 'playing'
        self.setUp()

    def update(self):
        if self.state != 'playing':
            return

        for snake in self.snakes:
            if isinstance(snake, playerSnake):
                snake.updateDirectionByMouse()
            elif isinstance(snake, ComputerSnake):
                snake.updateDirection()
            self.checkCollision(snake)
            snake.move()
        
            self.checkCollision(snake)
            snake.move()
        
        # 根據玩家蛇長度動態調整 Zoom
        # 長度越長，Zoom 越小 (看越廣)
        # 假設長度每增加 10，zoom 減少 0.01，最低 0.5
        player = self.snakes[0]
        if isinstance(player, playerSnake):
            target_zoom = max(0.5, 1.0 - (player.length - 10) * 0.002)
            # 平滑過度
            self.zoom += (target_zoom - self.zoom) * 0.05
        
        self.checkDeaths()

        # 這裡的 cameraX, cameraY 要對應 "虛擬" 座標
        # 螢幕中心在虛擬空間中的位置 = 玩家頭部位置
        # 因為我們要畫在一個 virtual_width x virtual_height 的畫布上
        virtual_width = SCREEN_WIDTH / self.zoom
        virtual_height = SCREEN_HEIGHT / self.zoom
        
        self.cameraX = self.snakes[0].head.centerx - virtual_width / 2
        self.cameraY = self.snakes[0].head.centery - virtual_height / 2

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
    
    def drawGrid(self, surface):
        """
        高效繪製網格背景。只繪製螢幕可見範圍內的網格。
        """
        # 計算虛擬畫面需含蓋的範圍
        virtual_width = SCREEN_WIDTH / self.zoom
        virtual_height = SCREEN_HEIGHT / self.zoom
        
        start_col = int(self.cameraX // GRID_SIZE) - 1
        start_row = int(self.cameraY // GRID_SIZE) - 1

        cols_to_draw = int(virtual_width // GRID_SIZE) + 4
        rows_to_draw = int(virtual_height // GRID_SIZE) + 4

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
                    pygame.draw.rect(surface, color, 
                                     (tile_screen_x, tile_screen_y, GRID_SIZE, GRID_SIZE))

    def checkDeaths(self):
        # 檢查每一條蛇是否撞到別條蛇
        # 注意：要倒序遍歷，因為可能會移除元素
        for i in range(len(self.snakes) - 1, -1, -1):
            snake = self.snakes[i]
            if self.isDead(snake):
                self.killSnake(snake)
                self.snakes.pop(i)
                
                # 如果是電腦蛇死掉，就重生一條新的，保持場上熱鬧
                if isinstance(snake, ComputerSnake):
                    cx = random.randint(100, MAP_WIDTH - 100)
                    cy = random.randint(100, MAP_HEIGHT - 100)
                    new_snake = ComputerSnake(cx, cy, (255, 0, 0))
                    self.snakes.append(new_snake)
                # 如果是玩家死掉，這裡暫時不重生 (或者可以重生，看需求)
                elif isinstance(snake, playerSnake):
                    self.state = 'game_over'
                    # 玩家死掉不自動重生，等待玩家按 R 重玩

    def isDead(self, snake):
        # 檢查 snake 是否撞到 OTHER snakes 的 body
        # 蛇頭半徑
        head_radius = TILE_SIZE // 2
        
        for other_snake in self.snakes:
            if other_snake == snake:
                continue
            
            # 遍歷對方的身體
            for body_part in other_snake.body:
                # 簡單的圓形/矩形碰撞檢查
                # 這裡用 center 距離比較準
                dx = snake.head.centerx - body_part.centerx
                dy = snake.head.centery - body_part.centery
                dist = math.sqrt(dx**2 + dy**2)
                
                # 如果距離小於兩者半徑之和 (TILE_SIZE)，就算碰撞
                if dist < TILE_SIZE:
                    return True
        return False

    def killSnake(self, snake):
        # 將蛇的身體轉換成食物
        # 為了避免食物太多，可以每隔幾個身體節點生成一個
        step = 3 
        for i in range(0, len(snake.body), step):
            rect = snake.body[i]
            # 隨機產生這坨肉是什麼等級的食物
            # 大部分是 medium，偶爾 large
            rand_val = random.random()
            if rand_val < 0.7:
                f_type = 'medium'
            else:
                f_type = 'large'
            
            food = Food(rect.centerx, rect.centery, f_type)
            self.food.append(food)

    def draw(self):
        # 1. 計算虛擬畫布大小
        virtual_width = int(SCREEN_WIDTH / self.zoom)
        virtual_height = int(SCREEN_HEIGHT / self.zoom)
        
        # 2. 建立虛擬畫布
        surface = pygame.Surface((virtual_width, virtual_height))
        surface.fill(BLACK)
        
        # 3. 所有的 draw 都要改畫在 surface 上
        self.drawGrid(surface) # drawGrid 需要這傳入 surface
        for food in self.food:
            food.draw(surface, self.cameraX, self.cameraY)
        for snake in self.snakes:
            snake.draw(surface, self.cameraX, self.cameraY)
        
        # 4. 縮放回螢幕大小並顯示
        scaled_surface = pygame.transform.smoothscale(surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(scaled_surface, (0, 0))
        
        playerHead = self.snakes[0].head
        coord = f"World: ({int(playerHead.centerx)}, {int(playerHead.centery)}) L:{self.snakes[0].length} Z:{self.zoom:.2f}"
        textSurface = self.font.render(coord, True, WHITE)
        self.screen.blit(textSurface, (10, 10))

        if self.state == 'game_over':
            self.drawGameOver()

    def drawGameOver(self):
        # 半透明黑色遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over 文字
        title_text = self.large_font.render("GAME OVER", True, (255, 50, 50))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        self.screen.blit(title_text, title_rect)
        
        # Restart 提示
        hint_text = self.font.render("Press 'R' to Restart", True, WHITE)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20))
        self.screen.blit(hint_text, hint_rect)