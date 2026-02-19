import pygame
from constant import *

class Menu_screen:
   def __init__(self,screen):
      self.font=pygame.font.SysFont("Arial",40)
      self.state="MENU"
      self.rect_play=pygame.Rect(100,200,200,50)
      self.rect_pokedex=pygame.Rect(100,300,200,50)
      self.rect_add_pokemon=pygame.Rect(100,400,200,50)

   def event_gestion(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN:
           pos_mouse=pygame.mouse.get_pos()
           if self.rect_play.collidepoint(pos_mouse):
              self.state="GAME"
           
           elif self.rect_pokedex.collidepoint(pos_mouse):
              self.state="POKEDEX"
           
           elif self.rect_add_pokemon.collidepoint(pos_mouse):
              self.state="LIST"

   def draw(self, screen):
      pass



           
       
          
    