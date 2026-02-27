"""
fight_screen.py
Handles the visual representation of Pokémon battles, including animations,
health bars, and battle backgrounds.
"""

import pygame
from src.constant import *
import random

class FightScreen:
    """
    Manages the battle UI, rendering sprites, animating health bars, 
    and handling screen shake effects.
    """
    def __init__(self, screen):
        """Initializes the battle screen with backgrounds and UI elements."""
        self.screen=screen
        
        # Load multiple backgrounds for variety
        self.bg_paths=[
            "assets/images/background_1.jpg",
            "assets/images/background_2.jpg",
            "assets/images/background_3.jpg",
            "assets/images/background_4.jpg",
            "assets/images/background_5.jpg",
            "assets/images/background_6.jpg",
            "assets/images/background_7.jpg",
            "assets/images/background_8.jpg"
        ]
   
        self.backgrounds=[]
        for path in self.bg_paths:
            img=pygame.image.load(path).convert()
            img=pygame.transform.smoothscale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.backgrounds.append(img)

        self.current_bg=self.backgrounds[0]
    
        # Button Layout Configuration
        button_width=250
        button_height=60
        gap=40
        start_x=(1280 - (button_width * 3 + gap * 2)) // 2
        
        self.rect_attack=pygame.Rect(start_x, 600, button_width, button_height)
        self.rect_potion=pygame.Rect(start_x + button_width + gap, 600, button_width, button_height)
        self.rect_escape=pygame.Rect(start_x + (button_width + gap) * 2, 600, button_width, button_height)
        
        # Animation & Visual Effects variables
        self.shake_intensity=0
        self.display_hp_player=0   # Used for smooth HP bar animation
        self.display_hp_opponent=0 # Used for smooth HP bar animation
        self.font_bold=FONT1
        self.font_simple=FONT2
        self.player_pokemon=None
        self.opponent=None
        self.message="Choose an action!"
        
    def event_gestion(self, event):
        """Checks for mouse clicks on battle action buttons."""
        if event.type==pygame.MOUSEBUTTONDOWN:
            pos_m=pygame.mouse.get_pos()
            if self.rect_attack.collidepoint(pos_m):
                return "ATTACK"
            elif self.rect_potion.collidepoint(pos_m):
                return "POTION"
            elif self.rect_escape.collidepoint(pos_m):
                return "ESCAPE"
        return None 

    def setup_new_fight(self):
        """Selects a random background for a fresh battle encounter."""
        self.current_bg=random.choice(self.backgrounds)

    def update(self):
        """Updates HP bar animations and reduces screen shake intensity over time."""
        speed=0.5
    
        # Smooth HP decrease animation for Player
        if self.player_pokemon:
            if self.display_hp_player > self.player_pokemon.hp:
                self.display_hp_player -= speed
            elif self.display_hp_player < self.player_pokemon.hp:
                self.display_hp_player=self.player_pokemon.hp 

        # Smooth HP decrease animation for Opponent
        if self.opponent:
            if self.display_hp_opponent > self.opponent.hp:
                self.display_hp_opponent -= speed
            elif self.display_hp_opponent < self.opponent.hp:
                self.display_hp_opponent=self.opponent.hp

        # Gradually stop the screen shaking
        if self.shake_intensity > 0:
            self.shake_intensity -= 1
    
    def draw(self, screen):
        """Renders all battle elements: background, sprites, UI, and messages."""
        # Calculate random offset if screen shake is active
        offset_x=random.randint(-self.shake_intensity, self.shake_intensity) if self.shake_intensity > 0 else 0
        offset_y=random.randint(-self.shake_intensity, self.shake_intensity) if self.shake_intensity > 0 else 0

        # Draw background with potential shake offset
        screen.blit(self.current_bg, (offset_x, offset_y))
    
        # Draw Player Section
        if self.player_pokemon:
            if self.display_hp_player==0: self.display_hp_player=self.player_pokemon.hp
            self.draw_hp_bar(150, 520, self.display_hp_player, self.player_pokemon.hp_max)
            
            sprite_player=pygame.transform.smoothscale(self.player_pokemon.sprite, (250, 250))
            screen.blit(sprite_player, (150 + offset_x, 250 + offset_y))
      
            text_name=self.font_simple.render(f"{self.player_pokemon.name} Lv.{self.player_pokemon.level}", True, (255, 255, 255))
            screen.blit(text_name, (150+ offset_x, 200+ offset_y))
           
            xp_text=self.font_simple.render(f"XP: {self.player_pokemon.xp}/100", True, (255, 255, 100))
            screen.blit(xp_text, (150+ offset_x, 550+ offset_y))
   
        # Draw Opponent Section
        if self.opponent:
            if self.display_hp_opponent==0: self.display_hp_opponent=self.opponent.hp
            self.draw_hp_bar(880, 520, self.display_hp_opponent, self.opponent.hp_max)
            
            sprite_opponent=pygame.transform.smoothscale(self.opponent.sprite, (250, 250))
            screen.blit(sprite_opponent, (880+ offset_x, 250+ offset_y))
            
            text_name=self.font_simple.render(f"{self.opponent.name} Lv.{self.opponent.level}", True, (255, 255, 255))
            screen.blit(text_name, (880+ offset_x, 200+ offset_y))
    
        # Render Dialogue/Message Box
        message_box=pygame.Rect(240, 50, 800, 120)
        pygame.draw.rect(screen, (0, 0, 0), message_box)
        pygame.draw.rect(screen, (255, 255, 255), message_box, 3)
    
        # Support for multi-line messages
        lines=self.message.split('\n') 
        y_offset=70
        for line in lines[:3]: 
            msg_text=self.font_simple.render(line, True, (255, 255, 255))
            screen.blit(msg_text, (260, y_offset))
            y_offset += 35  

        # Draw Action Buttons
        pygame.draw.rect(screen, (100, 100, 200), self.rect_attack)
        pygame.draw.rect(screen, (100, 200, 100), self.rect_potion)
        pygame.draw.rect(screen, (200, 100, 100), self.rect_escape)
    
        screen.blit(self.font_simple.render("FIGHT", True, (255, 255, 255)), (self.rect_attack.x + 80, self.rect_attack.y + 15))
        screen.blit(self.font_simple.render("POTION", True, (255, 255, 255)), (self.rect_potion.x + 75, self.rect_potion.y + 15))
        screen.blit(self.font_simple.render("ESCAPE", True, (255, 255, 255)), (self.rect_escape.x + 75, self.rect_escape.y + 15))
    
    def draw_hp_bar(self, x, y, current_hp, max_hp):
        """
        Draws a dynamic health bar. The ratio is clamped between 0 and 1
        to prevent the bar from extending beyond its border.
        """
        width=200
        height=15

        ratio=max(0, min(1, current_hp / max_hp))

        if ratio > 0.5: color=(0, 255, 0)     
        elif ratio > 0.2: color=(255, 165, 0)  
        else: color=(255, 0, 0)               
 
        # Inside
        pygame.draw.rect(self.screen, (50, 50, 50), (x, y, width, height))
 
        # Life jaudge
        pygame.draw.rect(self.screen, color, (x, y, int(width * ratio), height))
    
        # Border
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, width, height), 2)