import pygame
from game import GAME
from settings import SCREEN_WIDTH
from snake import playerSnake

# Mock pygame display (needed for GAME init)
pygame.init()
pygame.display.set_mode((100, 100)) 

game = GAME(None)
player = playerSnake(0, 0, (255, 255, 255))
game.snakes = [player]

# Test Case 1: Initial Length
player.length = 10
# Spacing is 15. World Length = 150.
# Target Width = 150 * 0.9 = 135.
# Target Zoom = SCREEN_WIDTH / 135.
# Let's assume SCREEN_WIDTH is defined in settings. We need to check settings or print it.
print(f"SCREEN_WIDTH: {SCREEN_WIDTH}")

game.update() # This will run the zoom logic (and other things, might error if dependencies missing, but let's try)
# Actually game.update() calls snake.move() etc. better to just run the zoom logic snippet or mock carefully.
# But let's try running update() and see if it crashes. If it crashes on move(), I'll just copy-paste the logic or make a minimal test.
# player.updateDirectionByMouse() might fail if no display logic.

# Let's isolate the zoom logic test to avoid side effects
print("Testing Zoom Calculation Logic...")
snake_length_world = player.length * player.spacing
target_virtual_width = snake_length_world * 0.9
if target_virtual_width < 100: target_virtual_width = 100
expected_zoom = SCREEN_WIDTH / target_virtual_width
print(f"Length: {player.length}, WorldLen: {snake_length_world}, TargetWidth: {target_virtual_width}, ExpectedZoom: {expected_zoom}")

# Run actual update logic manually to avoid pygame event issues
game.zoom = 0.5 # Start different
# Apply logic manually to verify formula
# ... code from game.py ...
# Actually, I should just run game.update() but wrap it to ignore errors or mock inputs.
# Or better, just write a fresh script that imports nothing but tests the math.

# Let's try to run game.update() but patching internal methods that might fail
game.checkCollision = lambda s: None
game.checkDeaths = lambda: None
player.updateDirectionByMouse = lambda: None
player.move = lambda: None

game.zoom = 0.5
for i in range(100): # Run multiple times for smoothing to settle
    game.update()

print(f"Actual Zoom after 100 updates: {game.zoom}")

# Test Case 2: Longer Snake
player.length = 100
snake_length_world = player.length * player.spacing # 1500
target_virtual_width = snake_length_world * 0.9 # 1350
expected_zoom = SCREEN_WIDTH / target_virtual_width

# Reset zoom to close
game.zoom = expected_zoom + 0.1 
for i in range(100):
   game.update()

print(f"Length: {player.length}, WorldLen: {snake_length_world}, TargetWidth: {target_virtual_width}, ExpectedZoom: {expected_zoom}")
print(f"Actual Zoom after 100 updates: {game.zoom}")
