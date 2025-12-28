import pygame
import pygame.gfxdraw # Import gfxdraw
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
        # Length = 10 + sqrt(score)
        return 10 + int(math.sqrt(self.score))

    @property
    def radius(self):
        # Radius scales with length
        return int(self.length * 1.5)

    @property
    def spacing(self):
        # Dynamic spacing to keep body connected as radius grows
        return max(5, int(self.radius * 1.2))
        
    def set_skin(self, head_img, body_img):
        self.head_img = head_img
        self.body_img = body_img

    def draw(self, screen, cameraX, cameraY, zoom):
        radius = int(self.radius * zoom)
        if radius < 1: radius = 1
        
        # Draw Body (Reverse order so tail is below neck)
        for i in range(len(self.body) - 1, 0, -1):
            part = self.body[i]
            
            screenX = (part.centerx - cameraX) * zoom
            screenY = (part.centery - cameraY) * zoom
            screenCenterX = int(screenX)
            screenCenterY = int(screenY)
            
            if hasattr(self, 'body_img') and self.body_img:
                scaled_size = int(radius * 2) 
                scaled_img = pygame.transform.scale(self.body_img, (scaled_size, scaled_size))
                rect = scaled_img.get_rect(center=(screenCenterX, screenCenterY))
                screen.blit(scaled_img, rect)
            else:
                 # Use gfxdraw for smooth edges (No outline)
                 pygame.gfxdraw.filled_circle(screen, screenCenterX, screenCenterY, radius, self.color)
                 pygame.gfxdraw.aacircle(screen, screenCenterX, screenCenterY, radius, self.color)

        # Draw Head
        head = self.body[0]
        screenX = (head.centerx - cameraX) * zoom
        screenY = (head.centery - cameraY) * zoom
        screenCenterX = int(screenX)
        screenCenterY = int(screenY)
        
        if hasattr(self, 'head_img') and self.head_img:
             angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
             scaled_size = int(radius * 2)
             scaled_head = pygame.transform.scale(self.head_img, (scaled_size, scaled_size))
             rotated_head = pygame.transform.rotate(scaled_head, angle)
             rect = rotated_head.get_rect(center=(screenCenterX, screenCenterY))
             screen.blit(rotated_head, rect)
        else:
             pygame.gfxdraw.filled_circle(screen, screenCenterX, screenCenterY, radius, self.color)
             pygame.gfxdraw.aacircle(screen, screenCenterX, screenCenterY, radius, self.color)

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
        # Ensure body list is initialized
        if not self.body:
             self.body.append(self.head.copy())
        
        # Sync Head (body[0])
        self.body[0] = self.head.copy()
            
        current_spacing = self.spacing
        current_trace_idx = 0
        acc_trace_dist = 0 # Cumulative distance along trace
        
        # We need to place body[i] at distance i * spacing from the head
        # We assume trace is continuous from head (index 0) backwards
        
        for i in range(1, len(self.body)):
            target_dist = i * current_spacing
            
            # Find the segment in trace that contains 'target_dist'
            while current_trace_idx < len(self.trace) - 1:
                p1 = self.trace[current_trace_idx]
                p2 = self.trace[current_trace_idx + 1]
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                seg_len = math.sqrt(dx**2 + dy**2)
                
                if acc_trace_dist + seg_len >= target_dist:
                    # Target is in this segment
                    remain_dist = target_dist - acc_trace_dist
                    ratio = remain_dist / seg_len if seg_len > 0 else 0
                    
                    # Interpolate
                    newX = p1[0] + dx * ratio
                    newY = p1[1] + dy * ratio
                    
                    self.body[i].centerx = int(newX)
                    self.body[i].centery = int(newY)
                    break # Done for this body part, stay at this trace segment for next body part?
                          # No, next body part needs target_dist + spacing. 
                          # We can continue from current trace segment state, but simpler to just loop or use local variables?
                          # To optimize: don't reset 'acc_trace_dist' or 'current_trace_idx' completely, 
                          # but 'target_dist' is increasing. 
                          # Correct logic: We stay inside this 'while' loop across 'for' iterations? No.
                          # Standard way: Just continue loop.
                    
                else:
                    # Move to next segment
                    acc_trace_dist += seg_len
                    current_trace_idx += 1
            
            # If ran out of trace
            if current_trace_idx >= len(self.trace) - 1:
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