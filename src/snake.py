import pygame
import math
import random
from .settings import MAP_HEIGHT, MAP_WIDTH, TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, BOOST_SPEED, BOOST_COST, MIN_SCORE_TO_BOOST
class Snake():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.head = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.score = 0.0 # Float for boost decay
        self.direction = pygame.Vector2(1, 0)
        self.base_speed = 7
        self.speed = self.base_speed
        self.isBoosting = False
        
        self.body = []
        self.trace = [] # History of head positions [(x, y), ...]

        # Initialize body and trace
        # Create a straight line trace backwards
        current_spacing = self.spacing
        for i in range(1000): # Pre-allocate enough trace
             tx = x - i 
             ty = y
             self.trace.append((tx, ty))
        
        # Initialize body parts along trace
        for i in range(self.length):
             target_idx = int(i * current_spacing)
             if target_idx < len(self.trace):
                 pos = self.trace[target_idx]
                 self.body.append(pygame.Rect(int(pos[0]), int(pos[1]), TILE_SIZE, TILE_SIZE))
             else:
                 self.body.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

    @property
    def length(self):
        # Restore: Length = 10 + sqrt(score)
        return 10 + int(math.sqrt(self.score))

    @property
    def radius(self):
        # Restore: Radius scales with length (formerly length * 1.5)
        # Note: length is now smaller (sqrt-based), so 1.5 might be appropriate
        return int(self.length * 1.5)

    @property
    def spacing(self):
        # Dynamic spacing to keep body connected as radius grows
        return max(5, int(self.radius * 0.8))
        
    def set_skin(self, head_img, body_img):
        self.head_img = head_img
        self.body_img = body_img

    def draw(self, screen, cameraX, cameraY, zoom):
        radius = int(self.radius * zoom)
        if radius < 1: radius = 1
        
        # Draw Body
        for i, part in enumerate(self.body):
            # Skip head (index 0)
            if i == 0: continue
            
            screenX = (part.centerx - cameraX) * zoom
            screenY = (part.centery - cameraY) * zoom
            screenCenterX = int(screenX)
            screenCenterY = int(screenY)
            
            if hasattr(self, 'body_img') and self.body_img:
                scaled_size = int(radius * 2) # Diameter
                scaled_img = pygame.transform.scale(self.body_img, (scaled_size, scaled_size))
                rect = scaled_img.get_rect(center=(screenCenterX, screenCenterY))
                screen.blit(scaled_img, rect)
            else:
                 pygame.draw.circle(screen, self.color, (screenCenterX, screenCenterY), radius)

        # Draw Head
        head = self.body[0]
        screenX = (head.centerx - cameraX) * zoom
        screenY = (head.centery - cameraY) * zoom
        screenCenterX = int(screenX)
        screenCenterY = int(screenY)
        
        if hasattr(self, 'head_img') and self.head_img:
             # Rotation
             angle = math.degrees(math.atan2(-self.direction.y, self.direction.x)) - 90
             scaled_size = int(radius * 2) # Use same size as body (Radius * 2)
             scaled_head = pygame.transform.scale(self.head_img, (scaled_size, scaled_size))
             rotated_head = pygame.transform.rotate(scaled_head, angle)
             rect = rotated_head.get_rect(center=(screenCenterX, screenCenterY))
             screen.blit(rotated_head, rect)
        else:
             pygame.draw.circle(screen, self.color, (screenCenterX, screenCenterY), radius, 0)

    def grow(self, amount):
        self.score += amount

    def move(self):
        # 1. Boost Logic
        if self.isBoosting and self.score > MIN_SCORE_TO_BOOST:
            self.speed = BOOST_SPEED
            self.score -= BOOST_COST # Deduct score directly
        else:
             self.speed = self.base_speed
             if self.score <= MIN_SCORE_TO_BOOST:
                 self.isBoosting = False

        # 2. Update Head Position
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed
        
        # Boundary Clamp
        r = self.radius
        if self.x < r: self.x = r
        if self.x > MAP_WIDTH - r: self.x = MAP_WIDTH - r
        if self.y < r: self.y = r
        if self.y > MAP_HEIGHT - r: self.y = MAP_HEIGHT - r
        
        # 3. Update Trace
        # Insert current position at start
        self.trace.insert(0, (self.x, self.y))
        
        # 4. Update Body Parts along Trace
        # Head (Body[0]) is always at trace[0]
        self.head.centerx = int(self.x)
        self.head.centery = int(self.y)
        
        if not self.body:
             self.body.append(self.head.copy())
        self.body[0] = self.head.copy()
        
        current_spacing = self.spacing
        current_trace_idx = 0
        accumulated_dist = 0
        
        # Update existing body parts
        # Algorithm: Walk down the trace until accumulated distance > required distance for next part
        
        for i in range(1, len(self.body)):
            # We want body[i] to be at distance i * spacing from head
            # Or simpler: body[i] is spacing away from body[i-1]
            
            # Find point on trace that is 'current_spacing' away from body[i-1] (or previous point found)
            # Since trace is discrete, we just find the first point > spacing distance
            
            start_pos = (self.body[i-1].centerx, self.body[i-1].centery)
            
            # Optimization: Start searching from current_trace_idx
            found = False
            for j in range(current_trace_idx, len(self.trace)):
                p = self.trace[j]
                dx = start_pos[0] - p[0]
                dy = start_pos[1] - p[1]
                dist_sq = dx*dx + dy*dy
                
                # Check squared distance to avoid sqrt spam
                if dist_sq >= current_spacing * current_spacing:
                    # Found the point
                    self.body[i].centerx = int(p[0])
                    self.body[i].centery = int(p[1])
                    current_trace_idx = j # Next part starts searching from here
                    found = True
                    break
            
            if not found:
                 # Ran out of trace (should not happen if trace is long enough)
                 # Just stack at end of trace
                 if self.trace:
                     last = self.trace[-1]
                     self.body[i].centerx = int(last[0])
                     self.body[i].centery = int(last[1])

        # 5. Manage Trace Length
        # Keep enough trace for all body parts
        # Max index needed was 'current_trace_idx' for the last body part
        # Add some buffer
        if len(self.trace) > current_trace_idx + 100:
            self.trace = self.trace[:current_trace_idx + 100]

        # 6. Length Control
        while len(self.body) < self.length:
            self.body.append(self.body[-1].copy())
        while len(self.body) > self.length:
            self.body.pop()


class playerSnake(Snake):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

    def updateDirectionByMouse(self):
        mx, my = pygame.mouse.get_pos()
        dx = mx - SCREEN_WIDTH / 2
        dy = my - SCREEN_HEIGHT / 2
        
        # Create vector
        vec = pygame.Vector2(dx, dy)
        if vec.length() > 0:
            vec = vec.normalize()
            self.direction = vec
        
        # Check Boost (Left Click)
        if pygame.mouse.get_pressed()[0]:
            self.isBoosting = True
        else:
            self.isBoosting = False

from .mlAgent import config

class ComputerSnake(Snake):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.angle = random.uniform(0, 360)
        self.turn_speed = 15 # Degrees per frame
        
        # State tracking for RL
        self.stateOld = None
        self.action = 0
        self.hasKilled = False

    def performAction(self, action):
        """
        Action Space:
        0: Straight
        1: Left
        2: Right
        3: Boost + Straight
        4: Boost + Left
        5: Boost + Right
        """
        # Determine Boost
        if action >= 3:
            self.isBoosting = True
            move_action = action - 3
        else:
            self.isBoosting = False
            move_action = action

        # 0: Keep current direction
        if move_action == 0:
            pass 
        # 1: Turn Left
        elif move_action == 1:
            self.angle -= self.turn_speed
        # 2: Turn Right
        elif move_action == 2:
            self.angle += self.turn_speed
            
        # Update vector from angle
        rad = math.radians(self.angle)
        self.direction = pygame.Vector2(math.cos(rad), math.sin(rad))

    def updateDirection(self):
        # With Q-learning, direction is updated via performAction called from game loop
        # So this default behavior is just ensuring the vector matches the angle if called
        rad = math.radians(self.angle)
        self.direction = pygame.Vector2(math.cos(rad), math.sin(rad))