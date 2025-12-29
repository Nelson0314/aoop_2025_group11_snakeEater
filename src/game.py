from .mlAgent.qAgent import QLearningAgent
from .mlAgent.utils import getState
from .mlAgent import config
import pygame
import random
import os
import sys
from .settings import *
from .snake import playerSnake, ComputerSnake
from .food import Food, SmallFood, MediumFood, LargeFood
import math
import datetime

from .spatial import SpatialGrid

class GAME():
    def __init__(self, screen, mode='play', clock=None):
        self.screen = screen
        self.mode = mode # 'play', 'learn', '2player'
        self.clock = clock
        
        self.snakes = []
        self.food = []
        self.cameraX = 0
        self.cameraY = 0
        self.font = pygame.font.SysFont(None, 18)
        self.largeFont = pygame.font.SysFont(None, 72)
        
        self.state = 'playing'
        self.zoom = 1.0

        # RL Agent
        # Actions: 0-2 (Normal), 3-5 (Boost)
        self.agent = QLearningAgent(actions=[0, 1, 2, 3, 4, 5])
        if mode == 'play':
             # In play mode, we might want to load model but NOT save it
             # Or just load it to have smart enemies
             self.agent.loadModel()
        else:
             self.agent.loadModel()

        # Spectator / Camera Settings
        self.cameraMode = 'follow' # 'follow' or 'god'
        self.godViewZoom = 0.1 # Zoom level for God View (Seeing approx 1/3 of map)

        # Optimization: Spatial Grid
        # Use GRID_SIZE from settings (e.g. 300)
        self.spatialGrid = SpatialGrid(MAP_WIDTH, MAP_HEIGHT, GRID_SIZE)

        self.spectatorSnake = None # Restore missing attribute

        self.loadAssets()
        self.setUp()

    def loadAssets(self):
        try:
            self.assets = {
                'skins': [
                    (pygame.image.load("assets/skin_green_head.png"), pygame.image.load("assets/skin_green_body.png")),
                    (pygame.image.load("assets/skin_blue_head.png"), pygame.image.load("assets/skin_blue_body.png")),
                    (pygame.image.load("assets/skin_red_head.png"), pygame.image.load("assets/skin_red_body.png"))
                ],
                'grid': pygame.image.load("assets/grid_bg.png")
            }
        except FileNotFoundError:
            print("Assets not found. Please run generate_assets.py")
            self.assets = {'skins': [], 'grid': None}

        # Music
        bgm_path = os.path.join("assets", "bgm.mp3")
        if os.path.exists(bgm_path):
            try:
                # pygame.mixer is initialized by pygame.init()
                pygame.mixer.music.load(bgm_path)
                pygame.mixer.music.set_volume(0.3) # 30% volume
                pygame.mixer.music.play(-1) # Loop forever
                print(f"Playing BGM: {bgm_path}")
            except Exception as e:
                print(f"Error playing music: {e}")
        else:
            print(f"No BGM found at {bgm_path}")

        # Sound Effects
        eat_path = os.path.join("assets", "eat.mp3")
        self.eat_sound = None
        if os.path.exists(eat_path):
            try:
                self.eat_sound = pygame.mixer.Sound(eat_path)
                self.eat_sound.set_volume(0.5)
                print(f"Loaded SFX: {eat_path}")
            except Exception as e:
                print(f"Error loading SFX: {e}")

    def setUp(self):
        # Create Player ONLY in 'play' mode
        if self.mode == 'play':
            xCentre = SCREEN_WIDTH / 2
            yCentre = SCREEN_HEIGHT / 2
            player = playerSnake(xCentre, yCentre, WHITE)
            if self.assets['skins']:
                # Player gets Skin 0 (Green)
                h, b = self.assets['skins'][0]
                player.set_skin(h, b)
            self.snakes.append(player)

        elif self.mode == '2player':
             # Import locally to avoid circular import if needed (though top-level import is fine)
             from .snake import KeyboardSnake
             
             # P1: WASD (Green Skin)
             p1_ctrl = {'left': pygame.K_a, 'right': pygame.K_d, 'boost': pygame.K_w}
             x1 = MAP_WIDTH / 3
             y1 = MAP_HEIGHT / 2
             self.p1 = KeyboardSnake(x1, y1, (0, 255, 0), p1_ctrl)
             if self.assets['skins']:
                 self.p1.set_skin(self.assets['skins'][0][0], self.assets['skins'][0][1])
             self.snakes.append(self.p1)
             
             # P2: Arrows (Blue Skin)
             p2_ctrl = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'boost': pygame.K_UP}
             x2 = 2 * MAP_WIDTH / 3
             y2 = MAP_HEIGHT / 2
             self.p2 = KeyboardSnake(x2, y2, (0, 100, 255), p2_ctrl)
             if self.assets['skins']:
                 # Use skin 1 (Blue)
                 self.p2.set_skin(self.assets['skins'][1][0], self.assets['skins'][1][1])
             self.snakes.append(self.p2)

        # Create Computer Snakes
        # In learn mode, we might want MORE snakes to speed up training?
        count = 50 if self.mode == 'learn' else 45 # More snakes in learn mode
        
        for i in range(count):
            cx = random.randint(100, MAP_WIDTH - 100)
            cy = random.randint(100, MAP_HEIGHT - 100)
            computer = ComputerSnake(cx, cy, (255, 0, 0))
            if self.assets['skins']:
                # Random skin 1 or 2 for enemies (or 0 too)
                skin_idx = random.randint(0, 2)
                h, b = self.assets['skins'][skin_idx]
                computer.set_skin(h, b)
            self.snakes.append(computer)

        for foodType, count in FOOD_COUNTS.items():
            for _ in range(count):
                self.spawnFood(foodType)

    def spawnFood(self, foodType):
        x = random.randint(20, MAP_WIDTH - 20)
        y = random.randint(20, MAP_HEIGHT - 20)
        
        if foodType == 'small':
            newFood = SmallFood(x, y)
        elif foodType == 'medium':
            newFood = MediumFood(x, y)
        elif foodType == 'large':
            newFood = LargeFood(x, y)
        else:
            newFood = Food(x, y) # Should not happen

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
                     self.handleSpectatorSwitch(-1)
                 elif event.key == pygame.K_d:
                     self.handleSpectatorSwitch(1)
                 elif event.key == pygame.K_g:
                     if self.cameraMode == 'god':
                         self.cameraMode = 'follow'
                     else:
                         self.cameraMode = 'god'
             
             # Screenshot (P)
             if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                 if not os.path.exists(os.path.join("docs", "screenshots")):
                     os.makedirs(os.path.join("docs", "screenshots"))
                 timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                 filename = os.path.join("docs", "screenshots", f"screenshot_{timestamp}.png")
                 pygame.image.save(self.screen, filename)
                 print(f"Screenshot saved: {filename}")
        
        # Handle wraparound for spectator index safely later in update
        if self.state == 'game_over':
            if keys[pygame.K_r]:
                self.restartGame()

    def handleSpectatorSwitch(self, direction):
        """
        Switch spectator target to previous or next snake in the list.
        direction: -1 for previous, 1 for next
        """
        if not self.snakes:
            return

        current_index = 0
        if self.spectatorSnake in self.snakes:
            current_index = self.snakes.index(self.spectatorSnake)
        
        # Calculate new index with wrap-around
        new_index = (current_index + direction) % len(self.snakes)
        self.spectatorSnake = self.snakes[new_index]
        self.cameraMode = 'follow'

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

        # Update Spatial Grid (Clear and Rebuild)
        self.spatialGrid.clear()
        for snake in self.snakes:
            self.spatialGrid.insert(snake)

        for snake in self.snakes:
            if isinstance(snake, playerSnake):
                snake.updateDirectionByMouse()
            elif isinstance(snake, ComputerSnake):
                # RL: Observe State
                snake.stateOld = getState(snake, self.snakes, self.food, MAP_WIDTH, MAP_HEIGHT, self.spatialGrid)
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
                # Adjusted Zoom: Base 600 + 1.5x length (prevents excessive zoom out at high scores)
                targetVirtualWidth = max(600 + snakeLengthWorld * 1.5, 200)
                targetZoom = SCREEN_WIDTH / targetVirtualWidth
                self.zoom += (targetZoom - self.zoom) * 0.05
                self.cameraX = player.head.centerx - (SCREEN_WIDTH / self.zoom) / 2
                self.cameraY = player.head.centery - (SCREEN_HEIGHT / self.zoom) / 2
        
        elif self.mode == 'learn':
            if len(self.snakes) > 0:
                 if self.cameraMode == 'god':
                     # Desired: See a good chunk of map but not all (too laggy)
                     # Use godViewZoom setting
                     targetZoom = self.godViewZoom
                     self.zoom += (targetZoom - self.zoom) * 0.05
                     # Center of map
                     self.cameraX = MAP_WIDTH/2 - (SCREEN_WIDTH / self.zoom) / 2
                     self.cameraY = MAP_HEIGHT/2 - (SCREEN_HEIGHT / self.zoom) / 2
                 
                 else: # Follow Mode
                     # Ensure we have a valid spectator target
                     if self.spectatorSnake not in self.snakes:
                         self.spectatorSnake = self.snakes[0]
                     
                     targetSnake = self.spectatorSnake
                     
                     # Simple fixed zoom for spectator for clarity
                     targetZoom = 0.8
                     self.zoom += (targetZoom - self.zoom) * 0.05
                     
                     self.cameraX = targetSnake.head.centerx - (SCREEN_WIDTH / self.zoom) / 2
                     self.cameraY = targetSnake.head.centery - (SCREEN_HEIGHT / self.zoom) / 2
            else:
                self.spectatorSnake = None

        self.checkDeaths()

        # RL: Learning Step (Only in learn mode)
        if self.mode == 'learn':
            for snake in self.snakes:
                if isinstance(snake, ComputerSnake) and hasattr(snake, 'stateOld'):
                    # Reward Logic
                    reward = config.REWARD_SURVIVAL 
                    if snake.score > snake.scoreOld:
                        reward = config.REWARD_EAT_FOOD
                    elif snake.score < snake.scoreOld:
                        reward += config.REWARD_BOOST_PENALTY
                    
                    if snake.hasKilled:
                        reward += config.REWARD_KILL
                        snake.hasKilled = False

                    # Wall Penalty Check
                    # Since move() clamps position, check if at boundary
                    head = snake.head
                    r = snake.radius
                    if head.centerx <= r or head.centerx >= MAP_WIDTH - r or \
                       head.centery <= r or head.centery >= MAP_HEIGHT - r:
                        reward += config.REWARD_WALL # Apply heavy penalty for hugging wall

                    snake.stateNew = getState(snake, self.snakes, self.food, MAP_WIDTH, MAP_HEIGHT, self.spatialGrid)
                    self.agent.learn(snake.stateOld, snake.action, reward, snake.stateNew)

    def checkCollision(self, snake):
        for i in range(len(self.food) - 1, -1, -1):
            food = self.food[i]
            
            # 計算蛇頭跟食物的距離
            dx = snake.head.centerx - food.x
            # 計算蛇頭跟食物的距離 (Squared Distance Optimization)
            dx = snake.head.centerx - food.x
            dy = snake.head.centery - food.y
            dist_sq = dx ** 2 + dy ** 2
            
            # 判斷標準：距離 < (蛇頭半徑 + 食物半徑)
            # 使用動態半徑 snake.radius
            radii_sum = snake.radius + food.radius
            
            if dist_sq < radii_sum ** 2:
                # Play Sound (Only for Player or Spectated Snake)
                should_play = False
                if self.mode == 'play' and isinstance(snake, playerSnake):
                    should_play = True
                elif self.mode == 'learn' and snake == self.spectatorSnake:
                    should_play = True
                
                if should_play and self.eat_sound:
                    self.eat_sound.play()
                
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
                    
                    if self.assets['grid']:
                         # Scale grid tile to match zoom
                         scaled_grid = pygame.transform.scale(self.assets['grid'], (int(gridSizeScreen)+1, int(gridSizeScreen)+1))
                         surface.blit(scaled_grid, (tileScreenX, tileScreenY))
                    else:
                        # Fallback to lines
                        if (row + col) % 2 == 0:
                            color = BLACK
                        else:
                            color = GRAY
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
                    if self.assets['skins']:
                        skin_idx = random.randint(0, 2)
                        h, b = self.assets['skins'][skin_idx]
                        newSnake.set_skin(h, b)
                    self.snakes.append(newSnake)
                # 如果是玩家死掉，這裡暫時不重生 (或者可以重生，看需求)
                elif isinstance(snake, playerSnake):
                    self.state = 'game_over'
                    # 玩家死掉不自動重生，等待玩家按 R 重玩

    def getKiller(self, snake):
        # 檢查 snake 是否撞到 OTHER snakes 的 body
        # 回傳造成撞擊的蛇 (killer)，如果沒撞到或是撞牆則回傳 True (代表死但無兇手) 或 None (活著)
        
        # USE SPATIAL GRID FOR QUERY
        headRadius = snake.radius
        headRect = snake.head
        
        # Query potential colliders from grid
        # Search radius 1 cell is likely enough if cell size is reasonable (e.g. 300)
        candidates = self.spatialGrid.get_potential_colliders(headRect, search_radius_cells=1)
        
        check_radius_sq_cache = {} # Cache radius calculations to avoid recalculating for same snake

        for otherSnake, bodyPart in candidates:
            if otherSnake == snake:
                continue
            
            # Get cached radius sum
            if otherSnake not in check_radius_sq_cache:
                r_sum = snake.radius + otherSnake.radius
                check_radius_sq_cache[otherSnake] = r_sum * r_sum
            
            limit_sq = check_radius_sq_cache[otherSnake]

            # Fast Euclidean check
            dx = headRect.centerx - bodyPart.centerx
            dy = headRect.centery - bodyPart.centery
            # Quick AABB check first? No, pure math might be faster in python than function calls
            # If dx > r_sum continue... optimized check:
            # if abs(dx) > r_sum or abs(dy) > r_sum: continue
            
            dist_sq = dx*dx + dy*dy
            if dist_sq < limit_sq:
                return otherSnake

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
                food = MediumFood(rect.centerx, rect.centery)
            else:
                food = LargeFood(rect.centerx, rect.centery)
            
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
        
        # 4. 畫食物 (Visual Culling)
        # Calculate visible world bounds
        visible_pad = 50 # padding to avoid popping
        view_min_x = self.cameraX - visible_pad
        view_min_y = self.cameraY - visible_pad
        view_max_x = self.cameraX + (SCREEN_WIDTH / self.zoom) + visible_pad
        view_max_y = self.cameraY + (SCREEN_HEIGHT / self.zoom) + visible_pad

        for food in self.food:
            if view_min_x < food.x < view_max_x and view_min_y < food.y < view_max_y:
                food.draw(self.screen, self.cameraX, self.cameraY, self.zoom)
            
        # 5. 畫蛇 (Visual Culling)
        for snake in self.snakes:
            # Simple bounding box check using head and estimated length
            # Note: Snake body can trail behind, so we need a generous margin or check body parts
            # For performance, checking head + max_len radius is faster than iterating body parts
            # Safe approximation: snake.head.x +/- (snake.length * snake.spacing)
            
            # Simple check: Is head on screen? (Most common case)
            # OR Is any part on screen? (Accurate but slow)
            # Compromise: Check if head is within reasonable distance of camera center
            # Max possible dimension of a snake is roughly length * spacing
            snake_bound = snake.length * snake.spacing
            
            if (view_min_x - snake_bound < snake.head.centerx < view_max_x + snake_bound and
                view_min_y - snake_bound < snake.head.centery < view_max_y + snake_bound):
                snake.draw(self.screen, self.cameraX, self.cameraY, self.zoom)
        
        # 6. UI Dashboard (Top-Left)
        player = self.snakes[0] # Usually player or spectator target
        if player:
            # Dashboard Config
            padding = 10
            panel_width = 220
            panel_height = 90
            panel_alpha = 180
            
            # Draw Panel Background
            panel_surf = pygame.Surface((panel_width, panel_height))
            panel_surf.fill((0, 0, 0))
            panel_surf.set_alpha(panel_alpha)
            self.screen.blit(panel_surf, (10, 10))
            
            # Draw Borders
            pygame.draw.rect(self.screen, (100, 200, 255), (10, 10, panel_width, panel_height + 100), 2) # Taller panel

            # Text Info
            # 1. SCORE
            score_text = self.largeFont.render(f"Score: {int(player.score)}", True, (255, 215, 0))
            score_text = pygame.transform.scale(score_text, (int(score_text.get_width() * 0.6), int(score_text.get_height() * 0.6)))
            self.screen.blit(score_text, (25, 20))

            # 2. Stats
            stats_color = (200, 200, 200)
            fps_val = int(self.clock.get_fps()) if self.clock else "N/A"
            line2 = f"Zoom: {self.zoom:.2f} | FPS: {fps_val}"
            surf2 = self.font.render(line2, True, stats_color)
            self.screen.blit(surf2, (25, 60))
            
            # 3. LEADERBOARD (Top 5)
            # Sort snakes by score
            sorted_snakes = sorted(self.snakes, key=lambda s: s.score, reverse=True)[:5]
            
            self.screen.blit(self.font.render("--- Leaderboard ---", True, WHITE), (25, 85))
            
            y_offset = 105
            for idx, s in enumerate(sorted_snakes):
                color = s.color
                name = "Player" if isinstance(s, playerSnake) else f"Bot {id(s) % 1000}"
                text = f"{idx+1}. {name}: {int(s.score)}"
                
                # Highlight if it's the current player/spectator
                if s == player:
                    color = (255, 215, 0) # Gold
                    text = f"> {text}"
                    
                surf = self.font.render(text, True, color)
                self.screen.blit(surf, (25, y_offset))
                y_offset += 15

            # 4. Draw Minimap
            self.drawMinimap()

        if self.state == 'game_over':
            self.drawGameOver()

    def drawGameOver(self):
        # 半透明黑色遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over 文字
        titleText = self.largeFont.render("GAME OVER", True, (255, 50, 50))
        titleRect = titleText.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        self.screen.blit(titleText, titleRect)
        
        # Restart 提示
        hintText = self.font.render("Press R to Restart", True, WHITE)
        hintRect = hintText.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20))
        self.screen.blit(hintText, hintRect)

    def drawMinimap(self):
        # Configuration
        map_size = 200 # Size of the minimap square
        margin = 20
        # Position: Bottom Right
        mm_x = SCREEN_WIDTH - map_size - margin
        mm_y = SCREEN_HEIGHT - map_size - margin
        
        # Scale factor
        scale_x = map_size / MAP_WIDTH
        scale_y = map_size / MAP_HEIGHT
        
        # 1. Background
        mm_surf = pygame.Surface((map_size, map_size))
        mm_surf.fill((20, 20, 30))
        mm_surf.set_alpha(200) # Semi-transparent
        
        # 2. Border
        pygame.draw.rect(mm_surf, (100, 200, 255), (0, 0, map_size, map_size), 2)
        
        # 3. Draw Food (Simple dots)
        for f in self.food:
            fx = int(f.x * scale_x)
            fy = int(f.y * scale_y)
            # Clip to minimap bounds
            fx = max(0, min(map_size-1, fx))
            fy = max(0, min(map_size-1, fy))
            
            # Simple color based on type
            color = f.color
            pygame.draw.circle(mm_surf, color, (fx, fy), 2)
            
        # 4. Draw Snakes
        for s in self.snakes:
            # Draw Head
            hx = int(s.x * scale_x)
            hy = int(s.y * scale_y)
            hx = max(0, min(map_size-1, hx))
            hy = max(0, min(map_size-1, hy))
            
            color = s.color
            # Highlight Player White/Gold
            if s == self.snakes[0]: # Assuming index 0 is player/target
                color = (255, 255, 255)
                radius = 4
            else:
                radius = 3
                
            pygame.draw.circle(mm_surf, color, (hx, hy), radius)
            
            # Draw Body (Simplified as dots or small lines)
            # Optimization: Only draw every Nth body part to save perf
            step = max(1, len(s.body) // 10) 
            for part in s.body[::step]:
                 bx = int(part.centerx * scale_x)
                 by = int(part.centery * scale_y)
                 pygame.draw.circle(mm_surf, s.color, (bx, by), 1)

        # 5. Draw View Rectangle (Camera view)
        view_w = SCREEN_WIDTH / self.zoom * scale_x
        view_h = SCREEN_HEIGHT / self.zoom * scale_y
        view_x = self.cameraX * scale_x
        view_y = self.cameraY * scale_y
        
        pygame.draw.rect(mm_surf, (255, 255, 255), (view_x, view_y, view_w, view_h), 1)

        # Blit to screen
        self.screen.blit(mm_surf, (mm_x, mm_y))
