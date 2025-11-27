MAP_WIDTH = 10000
MAP_HEIGHT = 10000
TILE_SIZE = 20
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GRID_SIZE = 300
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
# 1. 數量限制 (地圖上同時存在的數量)
FOOD_COUNTS = {
    'small': 200,   # 小食物由 200 個
    'medium': 50,   # 中食物由 50 個
    'large': 10     # 大食物由 10 個
}

# 2. 增加長度 (吃到後蛇變長幾格)
FOOD_GROWTH = {
    'small': 1,
    'medium': 2,
    'large': 3
}

# 3. 視覺半徑 (畫在螢幕上的大小)
FOOD_RADIUS = {
    'small': 5,
    'medium': 8,
    'large': 12
}

# 4. 顏色 (RGB)
FOOD_COLORS = {
    'small': (50, 50, 255),    # 藍色
    'medium': (255, 50, 255),  # 紫色
    'large': (255, 215, 0)     # 金色
}