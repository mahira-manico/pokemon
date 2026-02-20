import pygame
from fight import Fight
from constant import *

class FightScreen:
    def __init__(self,screen):
        self.screen=screen
        self.rect_attack = pygame.Rect(80, 520, 180, 50)
        self.rect_potion = pygame.Rect(310, 520, 180, 50)
        self.rect_escape = pygame.Rect(540, 520, 180, 50)
        self.font_bold=FONT1
        self.font_simple=FONT2
        self.player_pokemon=None
        self.opponent=None
        self.message="Choose an action!"
        
        
    
    def event_gestion(self,event):
       if event.type==pygame.MOUSEBUTTONDOWN:
          pos_m=pygame.mouse.get_pos()

          if self.rect_attack.collidepoint(pos_m):
             return "ATTACK"
          
          elif self.rect_potion.collidepoint(pos_m):
             return "POTION"
          
          elif self.rect_escape.collidepoint(pos_m):
             return "ESCAPE"
          
          elif self.state == "GAME_OVER":
           self.screen.fill((0, 0, 0))
    
          lines = self.game_over_message.split('\n')
          y = 200
          for line in lines:
           text = FONT1.render(line, True, (255, 255, 255))
           self.screen.blit(text, (200, y))
           y += 50
    
   
          text_replay = FONT2.render("Press R to Replay or SPACE for Menu", True, (200, 200, 200))
          self.screen.blit(text_replay, (150, 450))
          
       return None

    def draw(self, screen):
     screen.fill((50, 20, 20))
    
     if self.player_pokemon:
        sprite_player = pygame.transform.scale(self.player_pokemon.sprite, (120, 120))
        screen.blit(sprite_player, (80, 250))
  
        text_name = self.font_simple.render(f"{self.player_pokemon.name} Lv.{self.player_pokemon.level}", True, (255, 255, 255))
        screen.blit(text_name, (80, 200))
        
        hp_text = self.font_simple.render(f"HP: {self.player_pokemon.hp}/{self.player_pokemon.hp_max}", True, (0, 255, 0))
        screen.blit(hp_text, (80, 380))
    
     if self.opponent:
        sprite_opponent = pygame.transform.scale(self.opponent.sprite, (120, 120))
        screen.blit(sprite_opponent, (580, 250))
        
        text_name = self.font_simple.render(f"{self.opponent.name} Lv.{self.opponent.level}", True, (255, 255, 255))
        screen.blit(text_name, (580, 200))
        
        hp_text = self.font_simple.render(f"HP: {self.opponent.hp}/{self.opponent.hp_max}", True, (255, 0, 0))
        screen.blit(hp_text, (580, 380))
    

     message_box = pygame.Rect(80, 430, 640, 80)
     pygame.draw.rect(screen, (0, 0, 0), message_box)
     pygame.draw.rect(screen, (255, 255, 255), message_box, 3)
    
     lines = self.message.split('\n') 
     y_offset = 440
     for line in lines[:3]: 
      if len(line) > 70:
        line = line[:70] + "..."
    
      msg_text = self.font_simple.render(line, True, (255, 255, 255))
      screen.blit(msg_text, (90, y_offset))
      y_offset += 25  

     pygame.draw.rect(screen, (100, 100, 200), self.rect_attack)
     pygame.draw.rect(screen, (100, 200, 100), self.rect_potion)
     pygame.draw.rect(screen, (200, 100, 100), self.rect_escape)
    
     text_attack = self.font_simple.render("FIGHT", True, (255, 255, 255))
     text_potion = self.font_simple.render("POTION", True, (255, 255, 255))
     text_escape = self.font_simple.render("ESCAPE", True, (255, 255, 255))
    
     screen.blit(text_attack, (self.rect_attack.x + 40, self.rect_attack.y + 10))
     screen.blit(text_potion, (self.rect_potion.x + 30, self.rect_potion.y + 10))
     screen.blit(text_escape, (self.rect_escape.x + 30, self.rect_escape.y + 10))