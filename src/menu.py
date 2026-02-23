import pygame
from constant import *

class Menu_screen:
   def __init__(self, screen):

      original_bg = pygame.image.load("assets/images/pokemon_menu.jpg").convert()
      self.background = pygame.transform.smoothscale(original_bg, (1280, 720))
      
      self.font_title=pygame.font.Font("assets/fonts/solid_pokemon.ttf",90)
      self.font_normal = FONT2
     
      btn_w, btn_h = 300, 60
      center_x = (1280 - btn_w) // 2
      
      self.rect_play = pygame.Rect(center_x, 300, btn_w, btn_h)
      self.rect_pokedex = pygame.Rect(center_x, 400, btn_w, btn_h)
      self.rect_add_pokemon = pygame.Rect(center_x, 500, btn_w, btn_h)

   def event_gestion(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
           pos_mouse = pygame.mouse.get_pos()
           if self.rect_play.collidepoint(pos_mouse):
              return "GAME"
           elif self.rect_pokedex.collidepoint(pos_mouse):
              return "POKEDEX"
           elif self.rect_add_pokemon.collidepoint(pos_mouse):
              return "LIST"
        return None

   def draw(self, screen):

    screen.blit(self.background, (0, 0))

    text_title = self.font_title.render("POKÉMON ADVENTURE", True, (255, 215, 0)) 
    title_rect = text_title.get_rect(center=(640, 150))
    screen.blit(text_title, title_rect)

    buttons = [
        (self.rect_play, (100, 100, 200), "PLAY"),
        (self.rect_pokedex, (100, 200, 100), "POKEDEX"),
        (self.rect_add_pokemon, (200, 100, 100), "ADD POKEMON")
    ]

    for rect, color, label in buttons:
  
        pygame.draw.rect(screen, (30, 30, 30), (rect.x + 5, rect.y + 5, rect.w, rect.h)) 

        pygame.draw.rect(screen, color, rect)
       
        text_surf = self.font_normal.render(label, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

           
       
          
    