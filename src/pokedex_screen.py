"""
pokedex_screen.py
Handles the Pokédex interface, displaying a list of all encountered 
and captured Pokémon with their discovery status.
"""

import pygame
import json
from src.constant import *

class PokedexScreen:
    """
    Manages the Pokédex view, including loading entry data from JSON 
    and rendering a grid of discovered Pokémon.
    """
    def __init__(self, screen):
        """Initializes the Pokédex with background assets and data list."""
        self.screen=screen
        
        # Load and scale the Pokedex background
        original_bg=pygame.image.load("assets/images/pokedex.jpg").convert()
        self.background=pygame.transform.smoothscale(original_bg, (1280, 720))
        
        self.font=FONT2
        self.pokemon_list=[]
        self.load_pokedex()

    def load_pokedex(self):
        """
        Loads the list of encountered Pokémon from the local pokedex.json file.
        Fails gracefully if the file is missing or corrupted.
        """
        try:
            with open("pokedex.json", "r") as f:
                self.pokemon_list=json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.pokemon_list=[]
            
    def event_gestion(self, event):
        """Processes keyboard input for Pokédex navigation."""
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                return "BACK_TO_MENU"
        return None
    
    def draw(self, screen):
        """
        Renders the grid of Pokémon entries.
        Pokémon are displayed as silhouettes if seen but not caught.
        """
        # Background
        screen.blit(self.background, (0, 0))
        
        # Empty State Check
        if not self.pokemon_list:
            text=self.font.render("No Pokémon seen yet!", True, (255, 255, 255))
            screen.blit(text, (500, 300))
        else:         
            # Grid Layout Configuration
            margin_x=100
            margin_y=120
            column_gap=350 
            row_gap=80   
            items_per_column=7 

            # Iterate through the list to generate the grid
            for index, poke in enumerate(self.pokemon_list):
                col=index // items_per_column
                row=index % items_per_column
                
                x=margin_x + (col * column_gap)
                y=margin_y + (row * row_gap)
           
                # Prevent drawing off-screen if list is too long
                if x > 1100: continue 
            
                # Sprite Rendering with Discovery Logic
                try:
                    img=pygame.image.load(poke['sprite']).convert_alpha()
                    img=pygame.transform.scale(img, (60, 60))
                    
                    # If not captured, apply a dark tint (silhouette effect)
                    if not poke.get('captured', False):
                        img.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_MULT)
                    
                    screen.blit(img, (x, y - 10))
                except Exception:
                    # Skip rendering if the sprite file is missing
                    pass 

                # Use green for captured, gray for only seen
                color=(0, 255, 0) if poke.get('captured', False) else (150, 150, 150)
                status="CAPTURED" if poke.get('captured', False) else "SEEN"
                
                name_txt=self.font.render(f"{poke['name']} - {status}", True, color)
                screen.blit(name_txt, (x + 70, y))

        # Navigation Hint
        back_hint=self.font.render("ESC to Return", True, (BLUE))
        screen.blit(back_hint, (20, 680))