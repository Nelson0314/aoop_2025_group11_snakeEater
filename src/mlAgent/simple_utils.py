import math
import pygame

def getSimpleState(snake, snakes, food_list, map_width, map_height):
    """
    Simplified State Vector (4 bits):
    1. Danger Ahead (1 bit)
    2. Food Left (1 bit)
    3. Food Right (1 bit)
    4. Food Front (1 bit)
    """
    head = snake.head
    
    # 1. Danger Ahead
    # Check a point slightly ahead of the snake
    danger_dist = 120 # Lookahead distance (Increased from 50)
    check_x = head.centerx + snake.direction.x * danger_dist
    check_y = head.centery + snake.direction.y * danger_dist
    
    danger_front = 0
    
    # Wall Danger
    if check_x < 0 or check_x > map_width or check_y < 0 or check_y > map_height:
        danger_front = 1
    
    # Body Danger (Self or Others) - Simple check
    # Note: For simplicity, we might skip optimizing this with SpatialGrid unless needed
    # But reusing existing collision logic is better.
    # Let's use a simplified distance check against all snakes
    if danger_front == 0:
         for s in snakes:
             for part in s.body:
                 if part == head or part == s.body[1]: continue # Skip own head/neck
                 dist = math.hypot(check_x - part.centerx, check_y - part.centery)
                 if dist < s.radius + 20: # Collision radius
                     danger_front = 1
                     break
             if danger_front: break

    # 2. Food Direction (Relative)
    # Find closest food
    closest_food = None
    min_dist = float('inf')
    
    for f in food_list:
        dist = math.hypot(f.x - head.centerx, f.y - head.centery)
        if dist < min_dist:
            min_dist = dist
            closest_food = f
            
    food_left = 0
    food_right = 0
    food_front = 0
    
    if closest_food:
        # Calculate angle to food
        dx = closest_food.x - head.centerx
        dy = closest_food.y - head.centery
        
        # Snake's current angle (0-360)
        # Convert vector to angle
        snake_angle = snake.angle % 360
        
        # Absolute angle to food
        food_angle = math.degrees(math.atan2(dy, dx)) % 360
        
        # Relative angle (Food - Snake)
        diff = (food_angle - snake_angle + 360) % 360
        
        # Front: 315 to 45
        if diff > 330 or diff < 30:
            food_front = 1
        # Right: 30 to 150
        elif 30 <= diff < 150:
            food_right = 1
        # Left: 210 to 330
        elif 210 <= diff < 330:
            food_left = 1
         # Behind is ignored (or covered implicitly by 0,0,0)

    return (danger_front, food_left, food_right, food_front)
