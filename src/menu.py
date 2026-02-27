"""
menu_screen.py
Main hub of the game. Handles navigation to different game modes 
and data management (resetting progress).
"""

import pygame
from src.constant import *

class Menu_screen:
    """
    Manages the main menu interface, including buttons for navigation 
    and a confirmation system for data deletion.
    """
    def __init__(self, screen):
        """Initializes menu assets, button rectangles, and UI states."""
        self.screen=screen
  
        # UI State flags
        self.show_confirm=False 
        self.reset_msg_timer=0
        
        # UI Element positions
        self.reset_rect=pygame.Rect(1050, 650, 200, 50)
        self.yes_rect=pygame.Rect(450, 400, 150, 60)
        self.no_rect=pygame.Rect(680, 400, 150, 60)

        # Background loading and scaling
        original_bg=pygame.image.load("assets/images/pokemon_menu.jpg").convert()
        self.background=pygame.transform.smoothscale(original_bg, (1280, 720))
      
        # Fonts
        self.font_title=pygame.font.Font("assets/fonts/solid_pokemon.ttf", 90)
        self.font_normal=FONT2
     
        # Centering navigation buttons
        btn_w, btn_h=300, 60
        center_x=(1280 - btn_w) // 2
        self.rect_play=pygame.Rect(center_x, 300, btn_w, btn_h)
        self.rect_pokedex=pygame.Rect(center_x, 400, btn_w, btn_h)
        self.rect_add_pokemon=pygame.Rect(center_x, 500, btn_w, btn_h)

    def event_gestion(self, event):
        """
        Processes user input for menu navigation and data reset confirmation.
        
        Returns:
            str: The action keyword for the engine (GAME, POKEDEX, LIST, RESET_DATA).
        """
        # Close confirmation pop-up with ESC
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                if self.show_confirm:
                    self.show_confirm=False
                    return None
                
        if event.type==pygame.MOUSEBUTTONDOWN:
            pos_mouse=pygame.mouse.get_pos()

            # Logic while confirmation pop-up is active
            if self.show_confirm:
                if self.yes_rect.collidepoint(pos_mouse):
                    self.show_confirm=False
                    return "RESET_DATA"
                elif self.no_rect.collidepoint(pos_mouse):
                    self.show_confirm=False
                    return None
                return None
            
            # Reset button triggers confirmation
            if self.reset_rect.collidepoint(pos_mouse):
                self.show_confirm=True
                return None

            # Navigation buttons
            if self.rect_play.collidepoint(pos_mouse):
                return "GAME"
            elif self.rect_pokedex.collidepoint(pos_mouse):
                return "POKEDEX"
            elif self.rect_add_pokemon.collidepoint(pos_mouse):
                return "LIST"

        return None

    def trigger_reset_message(self):
        """Initializes the success notification timer (2 seconds at 60 FPS)."""
        self.reset_msg_timer=120

    def draw(self, screen):
        """Renders the menu background, title, buttons, and pop-ups."""
        # 1. Background and Title
        screen.blit(self.background, (0, 0))
        text_title=self.font_title.render("POKÉMON ADVENTURE", True, (255, 215, 0)) 
        title_rect=text_title.get_rect(center=(640, 150))
        screen.blit(text_title, title_rect)

        # Main Menu View
        if not self.show_confirm:
            buttons=[
                (self.rect_play, (100, 100, 200), "PLAY"),
                (self.rect_pokedex, (100, 200, 100), "POKEDEX"),
                (self.rect_add_pokemon, (200, 100, 100), "ADD POKEMON")
            ]

            for rect, color, label in buttons:
                # Button Shadow
                pygame.draw.rect(screen, (30, 30, 30), (rect.x + 5, rect.y + 5, rect.w, rect.h)) 
                # Button Face
                pygame.draw.rect(screen, color, rect)
                # Button Text
                text_surf=self.font_normal.render(label, True, (255, 255, 255))
                text_rect=text_surf.get_rect(center=rect.center)
                screen.blit(text_surf, text_rect)
       
            # Reset Data Button
            pygame.draw.rect(screen, (150, 0, 0), self.reset_rect, border_radius=5)
            reset_txt=self.font_normal.render("Reset Data", True, (255, 255, 255))
            reset_rect_center=reset_txt.get_rect(center=self.reset_rect.center)
            screen.blit(reset_txt, reset_rect_center)
         
            # Success Notification Logic
            if self.reset_msg_timer > 0:
                notif_rect=pygame.Rect(490, 20, 300, 40)
                pygame.draw.rect(screen, (40, 180, 40), notif_rect, border_radius=10)
                txt=self.font_normal.render("DATA RESET SUCCESS!", True, (255, 255, 255))
                txt_rect=txt.get_rect(center=notif_rect.center)
                screen.blit(txt, txt_rect)
                self.reset_msg_timer -= 1
        
        # Confirmation Pop-up View
        else:
            # Darken background
            overlay=pygame.Surface((1280, 720), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) 
            screen.blit(overlay, (0, 0))

            # Confirmation Box
            confirm_box=pygame.Rect(390, 250, 500, 250)
            pygame.draw.rect(screen, (40, 40, 60), confirm_box, border_radius=15)
            pygame.draw.rect(screen, (255, 255, 255), confirm_box, 3, border_radius=15)

            msg=self.font_normal.render("ARE YOU SURE?", True, (255, 255, 255))
            msg_rect=msg.get_rect(center=(640, 320))
            screen.blit(msg, msg_rect)

            # YES/NO Buttons
            pygame.draw.rect(screen, (40, 180, 40), self.yes_rect, border_radius=8)
            txt_yes=self.font_normal.render("YES", True, (255, 255, 255))
            screen.blit(txt_yes, txt_yes.get_rect(center=self.yes_rect.center))

            pygame.draw.rect(screen, (180, 40, 40), self.no_rect, border_radius=8)
            txt_no=self.font_normal.render("NO", True, (255, 255, 255))
            screen.blit(txt_no, txt_no.get_rect(center=self.no_rect.center))