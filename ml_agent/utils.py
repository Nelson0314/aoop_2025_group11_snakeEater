import math
import pygame
from settings import TILE_SIZE

def get_state(snake, snakes, foods, map_width, map_height):
    """
    Extracts a discrete state from the game environment for the Q-learning agent.
    Returns a tuple representing the state.
    """
    head = snake.body[0]
    
    # 1. Look-ahead points for danger detection
    point_l = pygame.Vector2(head.centerx, head.centery) + snake.direction.rotate(-45) * TILE_SIZE * 3
    point_f = pygame.Vector2(head.centerx, head.centery) + snake.direction * TILE_SIZE * 3
    point_r = pygame.Vector2(head.centerx, head.centery) + snake.direction.rotate(45) * TILE_SIZE * 3

    def is_collision(pt):
        # Wall collision
        if pt.x < 0 or pt.x > map_width or pt.y < 0 or pt.y > map_height:
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

    danger_l = is_collision(point_l)
    danger_f = is_collision(point_f)
    danger_r = is_collision(point_r)

    # 2. Food direction (Find closest food)
    closest_food = None
    min_dist = float('inf')
    
    # Optimisation: Check a subset or just closest one
    # If too many foods, getting closest might be slow, but for 500 foods it's fine
    for food in foods:
        dist = math.hypot(food.x - head.centerx, food.y - head.centery)
        if dist < min_dist:
            min_dist = dist
            closest_food = food
            
    # Direction booleans
    dir_l = snake.direction.x < 0
    dir_r = snake.direction.x > 0
    dir_u = snake.direction.y < 0
    dir_d = snake.direction.y > 0

    # Food relative position
    food_l = False
    food_r = False
    food_u = False
    food_d = False
    
    if closest_food:
        food_l = closest_food.x < head.centerx
        food_r = closest_food.x > head.centerx
        food_u = closest_food.y < head.centery
        food_d = closest_food.y > head.centery

    # Convert booleans to 0 or 1 integers for the state tuple
    state = (
        # Danger
        int(danger_f),
        int(danger_r),
        int(danger_l),
        
        # Current Direction
        int(dir_l),
        int(dir_r), 
        int(dir_u), 
        int(dir_d),
        
        # Food Location 
        int(food_l), 
        int(food_r), 
        int(food_u), 
        int(food_d)
    )
    
    return state
