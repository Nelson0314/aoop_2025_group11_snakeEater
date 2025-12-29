MAP_WIDTH = 7000
MAP_HEIGHT = 7000
TILE_SIZE = 20
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GRID_SIZE = 300
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
# 1. 數量限制 (地圖上同時存在的數量)
FOOD_COUNTS = {
    'small': 450,   # Reduced from 700
    'medium': 100,  # Reduced from 250
    'large': 30     # Reduced from 100
}

# 2. 增加長度 (吃到後蛇變長幾格)
FOOD_GROWTH = {
    'small': 1,
    'medium': 2,
    'large': 3
}

# 3. 加速設定 (Boost Settings)
BOOST_SPEED = 6          # Base speed 3.5 vs Boost speed 6 (Halved for 60fps)
BOOST_COST = 0.05        # Score deduction per frame (Halved for 60fps)
MIN_SCORE_TO_BOOST = 10  # Minimum length/score to enable boost

# 3. 視覺半徑 (畫在螢幕上的大小)
FOOD_RADIUS = {
    'small': 11,
    'medium': 17,
    'large': 23
}

# 4. 顏色 (RGB)
FOOD_COLORS = {
    'small': (50, 50, 255),    # 藍色
    'medium': (255, 50, 255),  # 紫色
    'large': (255, 215, 0)     # 金色
}