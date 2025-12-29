import pygame
import sys
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

def draw_text_centered(screen, font, text, y, color):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(SCREEN_WIDTH // 2, y))
    screen.blit(surf, rect)

def show_menu(screen):
    """
    Displays a navigable menu and returns the selected game mode string.
    Returns: 'play', 'learn', 'simple_learn', 'demo' or exits.
    """
    clock = pygame.time.Clock()
    
    # Fonts
    try:
        title_font = pygame.font.Font(None, 100)
        item_font = pygame.font.Font(None, 60)
        footer_font = pygame.font.Font(None, 30)
    except Exception:
        title_font = pygame.font.SysFont('Arial', 100)
        item_font = pygame.font.SysFont('Arial', 60)
        footer_font = pygame.font.SysFont('Arial', 30)

    # Menu Structure
    # Format: (Display Text, Return Value or Submenu List)
    TRAIN_MENU = [
        ("Train Complex Model (12-State)", "learn"),
        ("Train Simple Model (4-State)", "simple_learn"),
        ("Back", "BACK")
    ]
    
    MAIN_MENU = [
        ("Start Game", "play"),
        ("Training Models", TRAIN_MENU),
        ("Strategy Demo", "demo"),
        ("Quit", "QUIT")
    ]

    current_menu = MAIN_MENU
    selected_index = 0
    menu_stack = [] # To handle back navigation

    running = True
    while running:
        screen.fill((20, 20, 30))

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(current_menu)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(current_menu)
                elif event.key == pygame.K_RETURN:
                    # Select Item
                    label, action = current_menu[selected_index]
                    
                    if isinstance(action, list): # Submenu
                        menu_stack.append((current_menu, selected_index))
                        current_menu = action
                        selected_index = 0
                    elif action == "BACK":
                        if menu_stack:
                            current_menu, selected_index = menu_stack.pop()
                    elif action == "QUIT":
                        pygame.quit()
                        sys.exit()
                    else:
                        # Leaf node (game mode)
                        return action
                
                elif event.key == pygame.K_ESCAPE:
                    if menu_stack:
                        current_menu, selected_index = menu_stack.pop()
                    else:
                        pygame.quit()
                        sys.exit()

        # Rendering
        # Title
        title_text = "SLITHER AI" if current_menu == MAIN_MENU else "TRAINING MODE"
        draw_text_centered(screen, title_font, title_text, SCREEN_HEIGHT // 4, (0, 255, 100))
        
        # Menu Items
        start_y = SCREEN_HEIGHT // 2
        spacing = 70
        
        for i, (label, action) in enumerate(current_menu):
            color = (255, 255, 100) if i == selected_index else (150, 150, 150)
            
            # Add ">" indicator for selected
            display_text = f"> {label} <" if i == selected_index else label
            
            draw_text_centered(screen, item_font, display_text, start_y + i * spacing, color)

        # Footer
        draw_text_centered(screen, footer_font, "Use Arrow Keys to Navigate, Enter to Select", SCREEN_HEIGHT - 50, (100, 100, 100))

        pygame.display.flip()
        clock.tick(60)
