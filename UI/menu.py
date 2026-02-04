from typing import Tuple
import pygame
from Core import config

def hex_to_rgb(hexstr: str) -> Tuple[int, int, int]:
    s = hexstr.lstrip("#")
    if len(s) != 6:
        return (255, 255, 255)
    return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))

class MenuManager:
    def __init__(self):
        # Initialize fonts
        self.font_large = pygame.font.SysFont(None, 72)
        self.font_medium = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 24)
        
        # Colors
        self.colors = {
            'white': (255, 255, 255),
            'light_gray': (200, 200, 200),
            'red': hex_to_rgb("#FF3232"),
            'green': hex_to_rgb("#32FF32"),
            'blue': (100, 150, 255),
        }
    
    def draw_menu(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        
        title = self.font_large.render("BREAKOUT", True, self.colors['white'])
        start = self.font_medium.render("Press SPACE to Start", True, self.colors['light_gray'])
        quit_text = self.font_medium.render("Press ESC to Quit", True, self.colors['light_gray'])
        
        screen.blit(title, (config.SCREEN_WIDTH//2 - title.get_width()//2, 150))
        screen.blit(start, (config.SCREEN_WIDTH//2 - start.get_width()//2, 250))
        screen.blit(quit_text, (config.SCREEN_WIDTH//2 - quit_text.get_width()//2, 300))
    
    def draw_pause_screen(self, screen: pygame.Surface) -> None:
        # Draw semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # Draw pause text
        pause_text = self.font_large.render("PAUSED", True, self.colors['white'])
        continue_text = self.font_medium.render("Press P to Continue", True, self.colors['light_gray'])
        
        screen.blit(pause_text, (config.SCREEN_WIDTH//2 - pause_text.get_width()//2, 200))
        screen.blit(continue_text, (config.SCREEN_WIDTH//2 - continue_text.get_width()//2, 280))
    
    # Draw game over or level complete screen
    def draw_game_over(self, screen: pygame.Surface, lives: int, score: int) -> None:
        screen.fill((0, 0, 0))
        
        if lives <= 0:
            title = self.font_large.render("GAME OVER", True, self.colors['red'])
            restart_text = self.font_medium.render("Press R to Restart", True, self.colors['light_gray'])

        else:
            title = self.font_large.render("LEVEL COMPLETE!", True, self.colors['green'])
            restart_text = self.font_medium.render("Press Space to Continue", True, self.colors['light_gray'])
            

        score_text = self.font_medium.render(f"Final Score: {score}", True, self.colors['white'])
        quit_text = self.font_medium.render("Press ESC to Quit", True, self.colors['light_gray'])
        restart_text = self.font_medium.render("Press R to Restart", True, self.colors['light_gray'])

        screen.blit(title, (config.SCREEN_WIDTH//2 - title.get_width()//2, 150))
        screen.blit(score_text, (config.SCREEN_WIDTH//2 - score_text.get_width()//2, 250))
        screen.blit(restart_text, (config.SCREEN_WIDTH//2 - restart_text.get_width()//2, 300))
        screen.blit(quit_text, (config.SCREEN_WIDTH//2 - quit_text.get_width()//2, 350))
    
    # Draw the heads-up display (score and lives)
    def draw_hud(self, screen: pygame.Surface, score: int, lives: int) -> None:
        hud_text = self.font_small.render(f"Score: {score}  Lives: {lives}", True, self.colors['white'])
        screen.blit(hud_text, (8, 8))
    
    # Helper to draw centered text
    def draw_centered_text(self, screen: pygame.Surface, text: str, font_type: str = 'medium', 
                          y_offset: int = 0, color: str = 'white') -> None:
        font = getattr(self, f'font_{font_type}')
        rendered = font.render(text, True, self.colors[color])
        x = config.SCREEN_WIDTH // 2 - rendered.get_width() // 2
        screen.blit(rendered, (x, config.SCREEN_HEIGHT // 2 + y_offset))