import pygame
from constant import *

class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_bold = FONT1
        self.font_normal = FONT2
        
        self.overlay = pygame.Surface((1280, 720))
        self.overlay.set_alpha(190) 
        self.overlay.fill((20, 20, 35))

    def draw(self, message):

        self.screen.blit(self.overlay, (0, 0))
        
        is_victory = "won" in message.lower()
        title_color = (255, 215, 0) if is_victory else (255, 70, 70)
   
        lines = message.split('\n')
        y = 300
        for line in lines:
            text_surf = self.font_normal.render(line, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(640, y))
            self.screen.blit(text_surf, text_rect)
            y += 55
            

        bar_rect = pygame.Rect(0, 620, 1280, 100)
        pygame.draw.rect(self.screen, (40, 40, 60), bar_rect)
        pygame.draw.line(self.screen, title_color, (0, 620), (1280, 620), 3) 
        
        hint = self.font_normal.render("[R] Replay  -   [SPACE] Main Menu", True, (220, 220, 220))
        hint_rect = hint.get_rect(center=(640, 670))
        self.screen.blit(hint, hint_rect)