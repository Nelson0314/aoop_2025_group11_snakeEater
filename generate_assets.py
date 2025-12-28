import pygame
import os

def create_circle_surface(radius, color, border_color=None, border_width=0):
    size = radius * 2
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surface, color, (radius, radius), radius)
    if border_color and border_width > 0:
        pygame.draw.circle(surface, border_color, (radius, radius), radius, border_width)
    return surface

def create_head(radius, color, eyes_color=(255, 255, 255)):
    surface = create_circle_surface(radius, color)
    # Eyes
    eye_radius = radius // 4
    pygame.draw.circle(surface, eyes_color, (radius + radius//2, radius - radius//3), eye_radius)
    pygame.draw.circle(surface, eyes_color, (radius + radius//2, radius + radius//3), eye_radius)
    # Pupils
    pygame.draw.circle(surface, (0,0,0), (radius + radius//2 + 2, radius - radius//3), eye_radius//2)
    pygame.draw.circle(surface, (0,0,0), (radius + radius//2 + 2, radius + radius//3), eye_radius//2)
    return surface

def create_grid_texture(size, color, line_color):
    surface = pygame.Surface((size, size))
    surface.fill(color)
    pygame.draw.rect(surface, line_color, (0, 0, size, size), 1)
    return surface

def main():
    if not os.path.exists("assets"):
        os.makedirs("assets")

    pygame.init()
    
    # 1. Green Skin (Cartoon)
    color = (50, 200, 50)
    head = create_head(32, color)
    body = create_circle_surface(32, color, (30, 150, 30), 2)
    pygame.image.save(head, "assets/skin_green_head.png")
    pygame.image.save(body, "assets/skin_green_body.png")

    # 2. Blue Skin (Neon)
    color = (50, 50, 255)
    head = create_head(32, color, (0, 255, 255)) # Cyan eyes
    body = create_circle_surface(32, color, (0, 255, 255), 2)
    pygame.image.save(head, "assets/skin_blue_head.png")
    pygame.image.save(body, "assets/skin_blue_body.png")

    # 3. Red Skin (Aggressive)
    color = (220, 50, 50)
    head = create_head(32, color, (255, 255, 0)) # Yellow eyes
    body = create_circle_surface(32, color, (100, 0, 0), 2)
    pygame.image.save(head, "assets/skin_red_head.png")
    pygame.image.save(body, "assets/skin_red_body.png")

    # 4. Grid
    grid = create_grid_texture(100, (20, 20, 20), (50, 50, 50))
    pygame.image.save(grid, "assets/grid_bg.png")

    print("Assets generated in /assets")
    pygame.quit()

if __name__ == "__main__":
    main()
