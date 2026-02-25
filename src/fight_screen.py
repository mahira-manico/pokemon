import pygame
from fight import Fight
from constant import *
import random

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
        
        self.shake_intensity = 0
        self.display_hp_player = 0
        self.display_hp_opponent = 0
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


    def update(self):
  
     speed = 0.5
    
     if self.player_pokemon:
        if self.display_hp_player > self.player_pokemon.hp:
            self.display_hp_player -= speed
        elif self.display_hp_player < self.player_pokemon.hp:
            self.display_hp_player = self.player_pokemon.hp 

     if self.opponent:
        if self.display_hp_opponent > self.opponent.hp:
            self.display_hp_opponent -= speed
        elif self.display_hp_opponent < self.opponent.hp:
            self.display_hp_opponent = self.opponent.hp

     if self.shake_intensity > 0:
        self.shake_intensity -= 1
    
    def draw(self, screen):
        offset_x = random.randint(-self.shake_intensity, self.shake_intensity) if self.shake_intensity > 0 else 0
        offset_y = random.randint(-self.shake_intensity, self.shake_intensity) if self.shake_intensity > 0 else 0

        screen.blit(self.background, (offset_x, offset_y))
    
        if self.player_pokemon:

            if self.display_hp_player == 0: self.display_hp_player = self.player_pokemon.hp
    
            self.draw_hp_bar(150, 520, self.display_hp_player, self.player_pokemon.hp_max)
            sprite_player = pygame.transform.smoothscale(self.player_pokemon.sprite, (250, 250))
            screen.blit(sprite_player, (150 + offset_x, 250 + offset_y))
      
            text_name = self.font_simple.render(f"{self.player_pokemon.name} Lv.{self.player_pokemon.level}", True, (255, 255, 255))
            screen.blit(text_name, (150+ offset_x, 200+ offset_y))
           
            xp_text = pygame.font.SysFont("Arial", 20).render(f"XP: {self.player_pokemon.xp}/100", True, (255, 255, 100))
            screen.blit(xp_text, (150+ offset_x, 550+ offset_y))
   
        if self.opponent:
            if self.display_hp_opponent == 0: self.display_hp_opponent = self.opponent.hp
    
            self.draw_hp_bar(880, 520, self.display_hp_opponent, self.opponent.hp_max)
            sprite_opponent = pygame.transform.smoothscale(self.opponent.sprite, (250, 250))
            screen.blit(sprite_opponent, (880+ offset_x, 250+ offset_y))
            
            text_name = self.font_simple.render(f"{self.opponent.name} Lv.{self.opponent.level}", True, (255, 255, 255))
            screen.blit(text_name, (880+ offset_x, 200+ offset_y))
    
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
    
    def draw_hp_bar(self, x, y, current_hp, max_hp):
     width = 200
     height = 15

     ratio = max(0, current_hp / max_hp)

     if ratio > 0.5: color = (0, 255, 0)     
     elif ratio > 0.2: color = (255, 165, 0)  
     else: color = (255, 0, 0)               
 
     pygame.draw.rect(self.screen, (50, 50, 50), (x, y, width, height))
 
     pygame.draw.rect(self.screen, color, (x, y, int(width * ratio), height))
    
     pygame.draw.rect(self.screen, (255, 255, 255), (x, y, width, height), 2)