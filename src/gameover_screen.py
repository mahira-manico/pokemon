"""
gameover_screen.py
Handles the end-of-battle overlay, displaying results, XP gains, 
and providing options to restart or return to the menu.
"""

import pygame
from src.constant import *

class GameOverScreen:
    """
    Renders a semi-transparent summary screen over the battle view
    to show victory or defeat messages.
    """
    def __init__(self, screen):
        """Initializes the overlay surface and font styles."""
        self.screen=screen
        self.font_bold=FONT1
        self.font_normal=FONT2
        
        # Create a semi-transparent dark overlay
        self.overlay=pygame.Surface((1280, 720))
        self.overlay.set_alpha(190) # Adjust transparency (0-255)
        self.overlay.fill((20, 20, 35))

    def draw(self, message):
        """
        Draws the game over message, dynamically changing colors 
        based on the outcome (Victory vs Defeat).
        """
        # Apply the dark background overlay
        self.screen.blit(self.overlay, (0, 0))
        
        # Determine theme color based on the content of the message
        is_victory="won" in message.lower()
        title_color=(255, 215, 0) if is_victory else (255, 70, 70)
   
        # Split message into lines to handle multi-line summaries (XP, Evolution, etc.)
        lines=message.split('\n')
        y=200
        for line in lines:
            text_surf=self.font_normal.render(line, True, (255, 255, 255))
            text_rect=text_surf.get_rect(center=(640, y))
            self.screen.blit(text_surf, text_rect)
            y += 35
            
        # Draw bottom navigation bar
        bar_rect=pygame.Rect(0, 620, 1280, 100)
        pygame.draw.rect(self.screen, (40, 40, 60), bar_rect)
        # Accent line using the outcome theme color
        pygame.draw.line(self.screen, title_color, (0, 620), (1280, 620), 3) 
        
        # Render interaction hints
        hint=self.font_normal.render("[R] Replay  -  [SPACE] Main Menu", True, (220, 220, 220))
        hint_rect=hint.get_rect(center=(640, 670))
        self.screen.blit(hint, hint_rect)