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
        self.score = 0
        self.direction = pygame.Vector2(1, 0)
        self.base_speed = 7
        self.speed = self.base_speed
        self.isBoosting = False
        
        self.body = []
        # Initialize body parts
        for i in range(10): 
             self.body.append(pygame.Rect(x - i * 5, y, TILE_SIZE, TILE_SIZE))
        
        self.length = 10
        self.exact_length = float(self.length) # Float for smooth decay

    @property
    def radius(self):
        # Dynamic radius based on length
        return int(TILE_SIZE/2 + self.length * 0.02) 

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
        diameter = radius * 2

        # Draw Body
        if hasattr(self, 'body_img') and self.body_img:
            # Scale body image
            scaled_body = pygame.transform.scale(self.body_img, (diameter, diameter))
            for tile in self.body:
                screenCenterX = (tile.centerx - cameraX) * zoom
                screenCenterY = (tile.centery - cameraY) * zoom
                # Blit centered
                screen.blit(scaled_body, (screenCenterX - radius, screenCenterY - radius))
        else:
            # Fallback
            for tile in self.body:
                screenCenterX = (tile.centerx - cameraX) * zoom
                screenCenterY = (tile.centery - cameraY) * zoom
                pygame.draw.circle(screen, self.color, (screenCenterX, screenCenterY), radius, 0)
        
        # Draw Head
        screenCenterX = (self.head.centerx - cameraX) * zoom
        screenCenterY = (self.head.centery - cameraY) * zoom
        
        if hasattr(self, 'head_img') and self.head_img:
            # Rotate and scale head
            angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
            scaled_head = pygame.transform.scale(self.head_img, (diameter, diameter))
            rotated_head = pygame.transform.rotate(scaled_head, angle)
            rect = rotated_head.get_rect(center=(screenCenterX, screenCenterY))
            screen.blit(rotated_head, rect)
        else:
             pygame.draw.circle(screen, self.color, (screenCenterX, screenCenterY), radius, 0)

    def grow(self, amount):
        self.length += amount
        self.exact_length += amount # Keep sync
        self.score += amount

    def move(self):
        head = self.body[0]
        
        newX = head.centerx + self.direction.x * self.speed
        newY = head.centery + self.direction.y * self.speed
        
        # 使用動態半徑進行邊界檢查
        radius = self.radius 
        
        if newX - radius < 0: 
            newX = radius
        elif newX + radius > MAP_WIDTH: 
            newX = MAP_WIDTH - radius
        if newY - radius < 0: 
            newY = radius
        elif newY + radius > MAP_HEIGHT: 
            newY = MAP_HEIGHT - radius
        head.center = (newX, newY)

        while len(self.body) < self.length:
            self.body.append(pygame.Rect(head.x, head.y, TILE_SIZE, TILE_SIZE))

        for i in range(1, len(self.body)):
            leader = self.body[i-1]
            follower = self.body[i]

            dx = leader.centerx - follower.centerx
            dy = leader.centery - follower.centery
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 0:
                scale = self.spacing / dist
                targetX = leader.centerx - dx * scale
                targetY = leader.centery - dy * scale
                follower.centerx = targetX
                follower.centery = targetY

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