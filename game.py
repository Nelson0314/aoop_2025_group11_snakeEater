from mlAgent.qAgent import QLearningAgent
from mlAgent.utils import getState
from mlAgent import config
import pygame
import random
import os
from settings import *


class GAME():
    def __init__(self, screen, mode='play'):
        self.screen = screen
        self.mode = mode # 'play' or 'learn'
        
        self.snakes = []
        self.food = []
        self.cameraX = 0
        self.cameraY = 0
        self.font = pygame.font.SysFont(None, 18)
        self.largeFont = pygame.font.SysFont(None, 72)
        
        self.state = 'playing'
        self.zoom = 1.0

        # RL Agent
        # Actions: 0=Straight, 1=Left, 2=Right
        self.agent = QLearningAgent(actions=[0, 1, 2])
        if mode == 'play':
             # In play mode, we might want to load model but NOT save it
             # Or just load it to have smart enemies
             self.agent.loadModel()
        else:
             self.agent.loadModel()

        # Spectator / Camera Settings
        self.spectatorIndex = 0 # Index of snake to follow in learn mode
        self.cameraMode = 'follow' # 'follow' or 'god'
        self.godViewZoom = 0.1 # Zoom level for God View (Seeing approx 1/3 of map)

        self.setUp()

    def setUp(self):
        # Create Player ONLY in 'play' mode
        if self.mode == 'play':
            xCentre = SCREEN_WIDTH / 2
            yCentre = SCREEN_HEIGHT / 2
            player = playerSnake(xCentre, yCentre, WHITE)
            self.snakes.append(player)

        # Create Computer Snakes
        # In learn mode, we might want MORE snakes to speed up training?
        count = 20 if self.mode == 'learn' else 10 # More snakes in learn mode
        
        for _ in range(count):
            cx = random.randint(100, MAP_WIDTH - 100)
            cy = random.randint(100, MAP_HEIGHT - 100)
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
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit()
             
             # Spectator Controls (Single Press)
             if event.type == pygame.KEYDOWN and self.mode == 'learn':
                 if event.key == pygame.K_a:
                     self.spectatorIndex -= 1
                     self.cameraMode = 'follow'
                 elif event.key == pygame.K_d:
                     self.spectatorIndex += 1
                     self.cameraMode = 'follow'
                 elif event.key == pygame.K_g:
                     if self.cameraMode == 'god':
                         self.cameraMode = 'follow'
                     else:
                         self.cameraMode = 'god'
        
        # Handle wraparound for spectator index safely later in update
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

        # Auto-save model (Only in learn mode)
        if self.mode == 'learn':
            if not hasattr(self, 'frameCount'):
                self.frameCount = 0
            self.frameCount += 1
            if self.frameCount % config.MODEL_SAVE_INTERVAL == 0:
                self.agent.saveModel()

        for snake in self.snakes:
            if isinstance(snake, playerSnake):
                snake.updateDirectionByMouse()
            elif isinstance(snake, ComputerSnake):
                # RL: Observe State
                snake.stateOld = getState(snake, self.snakes, self.food, MAP_WIDTH, MAP_HEIGHT)
                snake.scoreOld = snake.score
                # RL: Choose Action
                snake.action = self.agent.chooseAction(snake.stateOld)
                snake.performAction(snake.action)
            
            self.checkCollision(snake)
            snake.move()
        
        # Camera Update Logic
        if self.mode == 'play':
            player = self.snakes[0] # Assuming player is always [0]
            if isinstance(player, playerSnake):
                snakeLengthWorld = player.length * player.spacing
                targetVirtualWidth = max(snakeLengthWorld * 3, 100)
                targetZoom = SCREEN_WIDTH / targetVirtualWidth
                self.zoom += (targetZoom - self.zoom) * 0.05
                self.cameraX = player.head.centerx - (SCREEN_WIDTH / self.zoom) / 2
                self.cameraY = player.head.centery - (SCREEN_HEIGHT / self.zoom) / 2
        
        elif self.mode == 'learn':
            if len(self.snakes) > 0:
                 if self.cameraMode == 'god':
                     # Desired: See a good chunk of map but not all (too laggy)
                     # Let's say we want to see 3000x3000 area
                     targetVirtualWidth = 3000
                     targetZoom = SCREEN_WIDTH / targetVirtualWidth
                     self.zoom += (targetZoom - self.zoom) * 0.05
                     # Center of map
                     self.cameraX = MAP_WIDTH/2 - (SCREEN_WIDTH / self.zoom) / 2
                     self.cameraY = MAP_HEIGHT/2 - (SCREEN_HEIGHT / self.zoom) / 2
                 
                 else: # Follow Mode
                     # Wrap index
                     self.spectatorIndex %= len(self.snakes)
                     targetSnake = self.snakes[self.spectatorIndex]
                     
                     # Simple fixed zoom for spectator for clarity
                     targetZoom = 0.8
                     self.zoom += (targetZoom - self.zoom) * 0.05
                     
                     self.cameraX = targetSnake.head.centerx - (SCREEN_WIDTH / self.zoom) / 2
                     self.cameraY = targetSnake.head.centery - (SCREEN_HEIGHT / self.zoom) / 2
            else:
                self.spectatorIndex = 0

        self.checkDeaths()

        # RL: Learning Step (Only in learn mode)
        if self.mode == 'learn':
            for snake in self.snakes:
                if isinstance(snake, ComputerSnake) and hasattr(snake, 'stateOld'):
                    # Reward Logic
                    reward = config.REWARD_SURVIVAL 
                    if snake.score > snake.scoreOld:
                        reward = config.REWARD_EAT_FOOD
                    
                    if snake.hasKilled:
                        reward += config.REWARD_KILL
                        snake.hasKilled = False

                    snake.stateNew = getState(snake, self.snakes, self.food, MAP_WIDTH, MAP_HEIGHT)
                    self.agent.learn(snake.stateOld, snake.action, reward, snake.stateNew)

    def checkCollision(self, snake):
        for i in range(len(self.food) - 1, -1, -1):
            food = self.food[i]
            
            # 計算蛇頭跟食物的距離
            dx = snake.head.centerx - food.x
            dy = snake.head.centery - food.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            
            # 判斷標準：距離 < (蛇頭半徑 + 食物半徑)
            # 使用動態半徑 snake.radius
            if distance < snake.radius + food.radius:
                
                # 1. 蛇變長
                snake.grow(food.growthValue)
                
                # 2. 記錄這個食物的類型 (為了重生)
                eatenType = food.type
                
                # 3. 移除這個食物
                self.food.pop(i)
                
                # 4. 立刻補充一個同類型的食物，保持總量平衡
                self.spawnFood(eatenType)
    
    def drawGrid(self, surface, zoom):
        """
        高效繪製網格背景。只繪製螢幕可見範圍內的網格。
        """
        # 計算螢幕可見的世界範圍
        # World Visible Width = SCREEN_WIDTH / zoom
        worldVisibleWidth = SCREEN_WIDTH / zoom
        worldVisibleHeight = SCREEN_HEIGHT / zoom
        
        # 計算可見範圍的左上角 Grid 索引
        startCol = int(self.cameraX // GRID_SIZE)
        startRow = int(self.cameraY // GRID_SIZE)

        # 計算需要畫多少格
        colsToDraw = int(worldVisibleWidth // GRID_SIZE) + 2
        rowsToDraw = int(worldVisibleHeight // GRID_SIZE) + 2

        # 限制範圍，不要畫到負數索引
        # 其實不用限制，因為 world 座標檢查會處理
        
        # 開始雙重迴圈繪製網格
        for row in range(startRow, startRow + rowsToDraw):
            for col in range(startCol, startCol + colsToDraw):
                
                # 計算這個網格的世界座標 (左上角)
                tileWorldX = col * GRID_SIZE
                tileWorldY = row * GRID_SIZE

                # 【關鍵】檢查這個網格是否在 10000x10000 的地圖範圍內
                if 0 <= tileWorldX < MAP_WIDTH and 0 <= tileWorldY < MAP_HEIGHT:
                    
                    # 計算螢幕座標 (Coordinate Transformation)
                    # ScreenX = (WorldX - CameraX) * Zoom
                    tileScreenX = (tileWorldX - self.cameraX) * zoom
                    tileScreenY = (tileWorldY - self.cameraY) * zoom
                    
                    # 計算網格在螢幕上的大小
                    gridSizeScreen = GRID_SIZE * zoom
                    # 避免浮點數縫隙，稍微加一點點或者用 ceil? 通常不用，pygame.draw.rect 接受 float 會取整
                    # 為了效能和畫面正確性，稍微重疊一點點無所謂，或是直接畫線
                    
                    # 決定顏色
                    if (row + col) % 2 == 0:
                        color = BLACK
                    else:
                        color = GRAY
                        
                    # 畫出這個網格矩形
                    # 為了避免浮點數導致的細微縫隙 (Moire pattern 或 gap)，可以使用 ceil 或者 +1
                    pygame.draw.rect(surface, color, 
                                     (tileScreenX, tileScreenY, gridSizeScreen + 1, gridSizeScreen + 1))

    def checkDeaths(self):
        # 檢查每一條蛇是否撞到別條蛇
        # 注意：要倒序遍歷，因為可能會移除元素
        for i in range(len(self.snakes) - 1, -1, -1):
            snake = self.snakes[i]
            killer = self.getKiller(snake)
            if killer:
                
                # RL: Death Penalty for victim
                if isinstance(snake, ComputerSnake) and hasattr(snake, 'stateOld'):
                    self.agent.learn(snake.stateOld, snake.action, config.REWARD_DEATH, snake.stateOld)
                
                # RL: Kill Reward for killer
                if killer and isinstance(killer, ComputerSnake):
                    killer.hasKilled = True # Flag to be picked up in the update loop

                self.killSnake(snake)
                self.snakes.pop(i)
                
                # 如果是電腦蛇死掉，就重生一條新的，保持場上熱鬧
                if isinstance(snake, ComputerSnake):
                    cx = random.randint(100, MAP_WIDTH - 100)
                    cy = random.randint(100, MAP_HEIGHT - 100)
                    newSnake = ComputerSnake(cx, cy, (255, 0, 0))
                    self.snakes.append(newSnake)
                # 如果是玩家死掉，這裡暫時不重生 (或者可以重生，看需求)
                elif isinstance(snake, playerSnake):
                    self.state = 'game_over'
                    # 玩家死掉不自動重生，等待玩家按 R 重玩

    def getKiller(self, snake):
        # 檢查 snake 是否撞到 OTHER snakes 的 body
        # 回傳造成撞擊的蛇 (killer)，如果沒撞到或是撞牆則回傳 True (代表死但無兇手) 或 None (活著)
        # 為了相容邏輯：
        # Return snake instance: Killed by snake
        # Return True: Killed by wall
        # Return False/None: Alive
        
        headRadius = snake.radius
        headX = snake.head.centerx
        headY = snake.head.centery

        # 1. 檢查牆壁
        if headX < headRadius or headX > MAP_WIDTH - headRadius or \
           headY < headRadius or headY > MAP_HEIGHT - headRadius:
            return True # Killed by Wall

        # 2. 檢查其他蛇
        for otherSnake in self.snakes:
            if otherSnake == snake:
                continue
            
            # 遍歷對方的身體
            for bodyPart in otherSnake.body:
                dx = headX - bodyPart.centerx
                dy = headY - bodyPart.centery
                dist = math.sqrt(dx**2 + dy**2)
                
                if dist < snake.radius + otherSnake.radius:
                    return otherSnake # Killed by otherSnake
        
        return None # Alive

    def killSnake(self, snake):
        # 將蛇的身體轉換成食物
        # 為了避免食物太多，可以每隔幾個身體節點生成一個
        step = 3 
        for i in range(0, len(snake.body), step):
            rect = snake.body[i]
            # 隨機產生這坨肉是什麼等級的食物
            # 大部分是 medium，偶爾 large
            randVal = random.random()
            if randVal < 0.7:
                fType = 'medium'
            else:
                fType = 'large'
            
            food = Food(rect.centerx, rect.centery, fType)
            self.food.append(food)

    def draw(self):
        # 1. 計算 Camera 位置 (讓蛇頭在螢幕中心)
        # CameraX = HeadX - (ScreenW / Zoom) / 2
        # 這一步其實在 update 做過了，但這裡是 rendering 階段，確保最新
        # self.cameraX 已經是 World 座標
        
        # 2. 直接畫在 self.screen 上，不需要 virtual surface
        self.screen.fill(BLACK) # 清空螢幕
        
        # 3. 畫網格 (傳入 zoom)
        self.drawGrid(self.screen, self.zoom)
        
        # 4. 畫食物
        for food in self.food:
            food.draw(self.screen, self.cameraX, self.cameraY, self.zoom)
            
        # 5. 畫蛇
        for snake in self.snakes:
            snake.draw(self.screen, self.cameraX, self.cameraY, self.zoom)
        
        # 6. UI 文字
        playerHead = self.snakes[0].head
        coord = f"Score: {self.snakes[0].score} World: ({int(playerHead.centerx)}, {int(playerHead.centery)}) L:{self.snakes[0].length} Z:{self.zoom:.2f}"
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
        titleText = self.large_font.render("GAME OVER", True, (255, 50, 50))
        titleRect = titleText.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        self.screen.blit(titleText, titleRect)
        
        # Restart 提示
        hintText = self.font.render("Press 'R' to Restart", True, WHITE)
        hintRect = hintText.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20))
        self.screen.blit(hintText, hintRect)