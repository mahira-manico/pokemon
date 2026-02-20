import pygame
from constant import *

class Menu_screen:
   def __init__(self,screen):
      self.background=pygame.image.load("assets/images/pokemon_menu.jpg").convert()
      self.font_bold=FONT1
      self.font_normal=FONT2
      self.state="MENU"
      self.rect_play=pygame.Rect(100,200,200,50)
      self.rect_pokedex=pygame.Rect(100,300,200,50)
      self.rect_add_pokemon=pygame.Rect(100,400,200,50)

   def event_gestion(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN:
           pos_mouse=pygame.mouse.get_pos()
           if self.rect_play.collidepoint(pos_mouse):
              return "GAME"
           
           elif self.rect_pokedex.collidepoint(pos_mouse):
              return "POKEDEX"
           
           elif self.rect_add_pokemon.collidepoint(pos_mouse):
              return "LIST"
        return None

   def draw(self, screen):
    screen.blit(self.background,(0,0))


    pygame.draw.rect(screen, (100, 100, 200), self.rect_play)
    pygame.draw.rect(screen, (100, 200, 100), self.rect_pokedex)
    pygame.draw.rect(screen, (200, 100, 100), self.rect_add_pokemon)
    
    text_title=self.font_bold.render("POKÉMON!",True,(RED))
    text_play = self.font_normal.render("PLAY", True, (255, 255, 255))
    text_pokedex = self.font_normal.render("POKEDEX", True, (255, 255, 255))
    text_add = self.font_normal.render("ADD", True, (255, 255, 255))
    
    screen.blit(text_title, (200,300))
    screen.blit(text_play, (self.rect_play.x + 50, self.rect_play.y + 10))
    screen.blit(text_pokedex, (self.rect_pokedex.x + 20, self.rect_pokedex.y + 10))
    screen.blit(text_add, (self.rect_add_pokemon.x + 70, self.rect_add_pokemon.y + 10))



           
       
          
    