import pygame
from fight import Fight
from constant import *

class FightScreen:
    def __init__(self, screen):
        self.screen = screen

        original_bg = pygame.image.load("assets/images/fight_background.jpg").convert()
        self.background = pygame.transform.smoothscale(original_bg, (1280, 720))
    
        button_width = 250
        button_height = 60
        gap = 40
        start_x = (1280 - (button_width * 3 + gap * 2)) // 2
        
        self.rect_attack = pygame.Rect(start_x, 600, button_width, button_height)
        self.rect_potion = pygame.Rect(start_x + button_width + gap, 600, button_width, button_height)
        self.rect_escape = pygame.Rect(start_x + (button_width + gap) * 2, 600, button_width, button_height)
        
        self.font_bold = FONT1
        self.font_simple = FONT2
        self.player_pokemon = None
        self.opponent = None
        self.message = "Choose an action!"
        
    def event_gestion(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_m = pygame.mouse.get_pos()
            if self.rect_attack.collidepoint(pos_m):
                return "ATTACK"
            elif self.rect_potion.collidepoint(pos_m):
                return "POTION"
            elif self.rect_escape.collidepoint(pos_m):
                return "ESCAPE"
        return None

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
    
        if self.player_pokemon:
    
            sprite_player = pygame.transform.smoothscale(self.player_pokemon.sprite, (250, 250))
            screen.blit(sprite_player, (150, 250))
      
            text_name = self.font_simple.render(f"{self.player_pokemon.name} Lv.{self.player_pokemon.level}", True, (255, 255, 255))
            screen.blit(text_name, (150, 200))
            
            hp_text = self.font_simple.render(f"HP: {self.player_pokemon.hp}/{self.player_pokemon.hp_max}", True, (0, 255, 0))
            screen.blit(hp_text, (150, 510))
           
            xp_text = pygame.font.SysFont("Arial", 20).render(f"XP: {self.player_pokemon.xp}/100", True, (255, 255, 100))
            screen.blit(xp_text, (150, 540))
   
        if self.opponent:
            sprite_opponent = pygame.transform.smoothscale(self.opponent.sprite, (250, 250))
            screen.blit(sprite_opponent, (880, 250))
            
            text_name = self.font_simple.render(f"{self.opponent.name} Lv.{self.opponent.level}", True, (255, 255, 255))
            screen.blit(text_name, (880, 200))
            
            hp_text = self.font_simple.render(f"HP: {self.opponent.hp}/{self.opponent.hp_max}", True, (255, 0, 0))
            screen.blit(hp_text, (880, 510))
    
        message_box = pygame.Rect(240, 50, 800, 120)
        pygame.draw.rect(screen, (0, 0, 0), message_box)
        pygame.draw.rect(screen, (255, 255, 255), message_box, 3)
    
        lines = self.message.split('\n') 
        y_offset = 70
        for line in lines[:3]: 
            msg_text = self.font_simple.render(line, True, (255, 255, 255))
            screen.blit(msg_text, (260, y_offset))
            y_offset += 35  

        pygame.draw.rect(screen, (100, 100, 200), self.rect_attack)
        pygame.draw.rect(screen, (100, 200, 100), self.rect_potion)
        pygame.draw.rect(screen, (200, 100, 100), self.rect_escape)
    
        screen.blit(self.font_simple.render("FIGHT", True, (255, 255, 255)), (self.rect_attack.x + 80, self.rect_attack.y + 15))
        screen.blit(self.font_simple.render("POTION", True, (255, 255, 255)), (self.rect_potion.x + 75, self.rect_potion.y + 15))
        screen.blit(self.font_simple.render("ESCAPE", True, (255, 255, 255)), (self.rect_escape.x + 75, self.rect_escape.y + 15))