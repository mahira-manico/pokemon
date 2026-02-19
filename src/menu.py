import pygame
from constant import *

class Menu_screen:
   def __init__(self,screen):
      self.font=pygame.font.SysFont("Arial",40)
      self.state="MENU"
      self.rect_play=pygame.Rect(100,200,200,50)
      self.rect_pokedex=pygame.Rect(100,300,200,50)
      self.rect_add_pokemon=pygame.Rect(100,400,200,50)

   def main_menu(self):
     running=True

     while running:
      
      for event in pygame.event.get():

        if event.type==pygame.QUIT:
           self.running=False
        elif event.type==pygame.MOUSEBUTTONDOWN:
           pos_mouse=pygame.mouse.get_pos()
           if self.rect_play.collidepoint(pos_mouse):
              self.state="GAME"
              self.running=False
           
           elif self.rect_pokedex.collidepoint(pos_mouse):
              self.state="POKEDEX"
              self.running=False
           
           elif self.rect_add_pokemon.collidepoint(pos_mouse):
              self.state="LIST"
              self.running=False

     return self.state
   pygame.time.Clock().tick(60)


           
       
          
    