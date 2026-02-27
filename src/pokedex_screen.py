import pygame
import json
from src.constant import *

class PokedexScreen:
    def __init__(self, screen):
        self.screen = screen
        original_bg=pygame.image.load("assets/images/pokedex.jpg").convert()
        self.background=pygame.transform.smoothscale(original_bg, (1280, 720))
        self.font = FONT2
        self.pokemon_list = []
        self.load_pokedex()

    
    def load_pokedex(self):
        try:
            with open("pokedex.json", "r") as f:
                self.pokemon_list = json.load(f)
        except FileNotFoundError:
            self.pokemon_list = []
            
    def event_gestion(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "BACK_TO_MENU"
        return None
    
    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        
        if not self.pokemon_list:
            text = self.font.render("No Pokémon seen yet!", True, (255, 255, 255))
            screen.blit(text, (500, 300))
        else:         
            margin_x = 100
            margin_y = 120
            column_gap = 350 
            row_gap = 80   
            items_per_column = 7 
            for index, poke in enumerate(self.pokemon_list):
             
                col = index // items_per_column
                row = index % items_per_column
                
                x = margin_x + (col * column_gap)
                y = margin_y + (row * row_gap)
           
                if x > 1100: continue 
            
                try:
                    img = pygame.image.load(poke['sprite']).convert_alpha()
                    img = pygame.transform.scale(img, (60, 60))
                    if not poke.get('captured', False):
                        img.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_MULT)
                    screen.blit(img, (x, y - 10))
                except:
                    pass 

                color = (0, 255, 0) if poke.get('captured', False) else (150, 150, 150)
                status = "CAPTURED" if poke.get('captured', False) else "SEEN"
                
                name_txt = self.font.render(f"{poke['name']} - {status}", True, color)
                screen.blit(name_txt, (x + 70, y))

        back_hint = self.font.render("ESC to Return", True, (BLUE))
        screen.blit(back_hint, (20, 680))