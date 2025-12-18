import math
import pygame
from settings import TILE_SIZE

def getState(snake, snakes, foods, mapWidth, mapHeight):
    """
    Extracts a discrete state from the game environment for the Q-learning agent.
    Returns a tuple representing the state.
    """
    head = snake.body[0]
    
    # 1. Look-ahead points for danger detection
    pointL = pygame.Vector2(head.centerx, head.centery) + snake.direction.rotate(-45) * TILE_SIZE * 5
    pointF = pygame.Vector2(head.centerx, head.centery) + snake.direction * TILE_SIZE * 5
    pointR = pygame.Vector2(head.centerx, head.centery) + snake.direction.rotate(45) * TILE_SIZE * 5

    def isCollision(pt):
        # Wall collision
        if pt.x < 0 or pt.x > mapWidth or pt.y < 0 or pt.y > mapHeight:
            return True
        # Snake collision (check all OTHER snakes)
        # Check against all bodies of all other snakes
        for other in snakes:
            if other == snake: continue
            for part in other.body:
                dist = math.sqrt((pt.x - part.centerx)**2 + (pt.y - part.centery)**2)
                if dist < snake.radius + other.radius: # Simple radius check
                    return True
        return False

    dangerL = isCollision(pointL)
    dangerF = isCollision(pointF)
    dangerR = isCollision(pointR)

    # 2. Food direction (Find closest food)
    closestFood = None
    minDist = float('inf')
    
    # Optimisation: Check a subset or just closest one
    # If too many foods, getting closest might be slow, but for 500 foods it's fine
    for food in foods:
        dist = math.hypot(food.x - head.centerx, food.y - head.centery)
        if dist < minDist:
            minDist = dist
            closestFood = food
            
    # Direction booleans
    dirL = snake.direction.x < 0
    dirR = snake.direction.x > 0
    dirU = snake.direction.y < 0
    dirD = snake.direction.y > 0

    # Food relative position
    foodL = False
    foodR = False
    foodU = False
    foodD = False
    
    if closestFood:
        foodL = closestFood.x < head.centerx
        foodR = closestFood.x > head.centerx
        foodU = closestFood.y < head.centery
        foodD = closestFood.y > head.centery

    # 3. Combat Awareness: Enemy Head Near Body Segment 3
    # Used for "Cut off" strategies
    enemyHeadNearBody3 = False
    if len(snake.body) >= 3:
        targetBodyPart = snake.body[2] # 3rd segment (index 2)
        detectionRadius = snake.radius * 4 # Detect within ~2 body widths
        
        for other in snakes:
            if other == snake: continue
            dist = math.hypot(other.head.centerx - targetBodyPart.centerx, other.head.centery - targetBodyPart.centery)
            if dist < detectionRadius:
                enemyHeadNearBody3 = True
                break

    # Convert booleans to 0 or 1 integers for the state tuple
    state = (
        # Danger
        int(dangerF),
        int(dangerR),
        int(dangerL),
        
        # Current Direction
        int(dirL),
        int(dirR), 
        int(dirU), 
        int(dirD),
        
        # Food Location 
        int(foodL), 
        int(foodR), 
        int(foodU), 
        int(foodD),

        # Combat (New)
        int(enemyHeadNearBody3)
    )
    
    return state