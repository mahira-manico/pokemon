"""
selection_screen.py
Handles the Pokémon selection interface where players choose their 
combatant from captured or custom Pokémon.
"""

import json
import pygame
from src.constant import *

class SelectionScreen:
    """
    Renders a grid of available Pokémon and displays detailed stats 
    for the currently selected one.
    """
    def __init__(self, screen, file_to_load):
        """Initializes the selection screen and loads the player's collection."""
        self.screen=screen
        self.data_file=file_to_load
        self.font_bold=FONT1
        self.font_normal=FONT2
        
        # State variables for selection
        self.pokemon_choosen=None
        self.pokemon_choosen_id=None
        self.buttons_pokemon=[]
        self.all_pokemon={}
        
        self.load_pokemon()

    def load_pokemon(self):
        """
        Parses the save file and Pokédex to determine which Pokémon 
        should be displayed (starters, captured, or custom).
        """
        # Load main character data
        with open(self.data_file, "r") as file:
            self.all_pokemon=json.load(file)

        # Cross-reference with Pokédex for capture status
        captured_names=[]
        try:
            with open("pokedex.json", "r") as f:
                pokedex_data=json.load(f)
                captured_names=[p['name'] for p in pokedex_data if p.get('captured')]
        except (FileNotFoundError, json.JSONDecodeError):
             captured_names=[]

        self.buttons_pokemon=[]
        index_display=0
        
        # Grid Generation Logic
        
        for pokemon_id, pokemon in self.all_pokemon.items():
            # Display logic: starter, captured in pokedex, or custom added if > ID 36)
            is_starter=(pokemon_id=="1")
            is_captured=(pokemon["name"] in captured_names)
            is_custom=(int(pokemon_id) > 36)

            if is_starter or is_captured or is_custom:
                column=6
                margin_x, margin_y=50, 100
                space_between=100
                
                # Math to calculate X and Y position based on index
                x=margin_x + (index_display % column * space_between)
                y=margin_y + (index_display // column * space_between)
                
                image=pygame.image.load(pokemon["sprite"])
                image=pygame.transform.scale(image, (64, 64))
                rect=pygame.Rect(x, y, 64, 64)
                
                self.buttons_pokemon.append({
                    "rect":rect,
                    "image":image,
                    "id":pokemon_id,
                    "data":pokemon
                })
                index_display += 1
     
    def event_gestion(self, event):
        """Processes clicks on Pokémon icons and navigation buttons."""
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                return "BACK_TO_MENU"
   
        if event.type==pygame.MOUSEBUTTONDOWN:
            mouse_position=pygame.mouse.get_pos()
       
            # Check if a Pokémon icon was clicked
            for buttons in self.buttons_pokemon:
                if buttons["rect"].collidepoint(mouse_position):
                    self.pokemon_choosen=buttons["data"]
                    self.pokemon_choosen_id=buttons["id"]
            
            # Check for the "FIGHT" button only if a Pokémon is selected
            if self.pokemon_choosen_id:
                go_button_rect=pygame.Rect(950, 550, 180, 60)
                if go_button_rect.collidepoint(mouse_position):
                    return "GO_FIGHT"
                
            # Back button logic
            if hasattr(self, 'back_button_rect') and self.back_button_rect.collidepoint(mouse_position):
                return "BACK_TO_MENU"
                
        return None
    
    def draw(self, screen):
        """Renders the selection grid, info box, and interactive buttons."""
        screen.fill((20, 20, 40))  
   
        title=self.font_bold.render("Choose your Pokemon!", True, (255, 255, 255))
        screen.blit(title, (440, 20))

        # Render Back Button
        self.back_button_rect=pygame.Rect(50, 620, 150, 50)
        pygame.draw.rect(screen, (100, 100, 100), self.back_button_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.back_button_rect, 2, border_radius=10)
    
        back_text=self.font_normal.render("BACK", True, (255, 255, 255))
        text_rect=back_text.get_rect(center=self.back_button_rect.center)
        screen.blit(back_text, text_rect)
    
        # Draw Pokémon Icons
        for button in self.buttons_pokemon:
            screen.blit(button["image"], button["rect"])
            # Highlight the selected Pokémon
            if self.pokemon_choosen_id==button["id"]:
                pygame.draw.rect(screen, (GOLD), button["rect"], 3)  

        # Draw Stats Info Box
        if self.pokemon_choosen:
            info_box=pygame.Rect(850, 150, 380, 250)
            pygame.draw.rect(screen, (0, 0, 0), info_box)
            pygame.draw.rect(screen, (255, 215, 0), info_box, 3) # Golden border
    
            # Render stats with different colors for readability
            name=self.font_normal.render(f"Name: {self.pokemon_choosen['name']}", True, (255, 255, 255))
            type_text=self.font_normal.render(f"Type: {'/'.join(self.pokemon_choosen['type'])}", True, (255, 255, 255))
            hp_text=self.font_normal.render(f"HP: {self.pokemon_choosen['hp']}", True, (0, 255, 0))
            atk_text=self.font_normal.render(f"ATK: {self.pokemon_choosen['attack']}", True, (255, 100, 100))
            def_text=self.font_normal.render(f"DEF: {self.pokemon_choosen['defense']}", True, (100, 100, 255))
 
            screen.blit(name, (870, 170))
            screen.blit(type_text, (870, 210))
            screen.blit(hp_text, (870, 250))
            screen.blit(atk_text, (870, 290))
            screen.blit(def_text, (870, 330))
    
        # Render Fight Button if selection is made
        if self.pokemon_choosen_id:
            go_button=pygame.Rect(950, 550, 180, 60)
            pygame.draw.rect(screen, (0, 200, 0), go_button)
            text_go=self.font_normal.render("FIGHT!", True, (255, 255, 255))
            screen.blit(text_go, (go_button.x + 50, go_button.y + 15))
            
        help_txt=self.font_normal.render("ESC to Return", True, (150, 150, 150))
        screen.blit(help_txt, (1100, 680))
  
    def refresh(self):   
        """Reloads the Pokémon list (used after adding a new custom Pokémon)."""
        self.buttons_pokemon=[]
        self.load_pokemon()