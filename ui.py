import pygame
import sys
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

def show_start_screen(screen, title="SLITHER AI", subtitle="Press ENTER to Start"):
    """
    Displays a polished start screen and waits for the user to press ENTER.
    """
    clock = pygame.time.Clock()
    
    # Fonts
    try:
        title_font = pygame.font.Font(None, 100) # Default system font, large
        sub_font = pygame.font.Font(None, 50)
        info_font = pygame.font.Font(None, 30)
    except Exception:
        # Fallback if font init fails (rare)
        title_font = pygame.font.SysFont('Arial', 100)
        sub_font = pygame.font.SysFont('Arial', 50)
        info_font = pygame.font.SysFont('Arial', 30)

    # Gradient background effect (simplified as vertical lines or just a nice color)
    # Let's keep it simple but clean: Dark background with some particles or just pulsing text
    
    waiting = True
    alpha = 0
    alpha_dir = 5

    while waiting:
        screen.fill((20, 20, 30)) # Dark Blue-ish Gray

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Visuals
        # 1. Title
        title_surf = title_font.render(title, True, (0, 255, 100)) # Greenish title
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
        
        # Shadow for title
        shadow_surf = title_font.render(title, True, (0, 100, 50))
        shadow_rect = shadow_surf.get_rect(center=(SCREEN_WIDTH/2 + 4, SCREEN_HEIGHT/3 + 4))
        screen.blit(shadow_surf, shadow_rect)
        screen.blit(title_surf, title_rect)

        # 2. Blinking Subtitle
        alpha += alpha_dir
        if alpha >= 255 or alpha <= 50:
            alpha_dir *= -1
        
        sub_surf = sub_font.render(subtitle, True, WHITE)
        sub_surf.set_alpha(alpha)
        sub_rect = sub_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(sub_surf, sub_rect)

        # 3. Footer Info
        footer_text = "Created by Group 11"
        footer_surf = info_font.render(footer_text, True, (150, 150, 150))
        footer_rect = footer_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 50))
        screen.blit(footer_surf, footer_rect)

        pygame.display.flip()
        clock.tick(60)
