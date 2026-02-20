import json
import pygame
from constant import *

class SelectionScreen:
    def __init__(self,screen):
        self.screen=screen
        self.font_bold=FONT1
        self.font_normal=FONT2
        self.pokemon_choosen=None
        self.pokemon_choosen_id=None
        self.buttons_pokemon=[]
        self.all_pokemon={}
        self.load_pokemon()

    def load_pokemon(self):
        with open("data/pokemon.json", "r") as file:
            self.all_pokemon=json.load(file)
        for index, (pokemon_id,pokemon) in enumerate(self.all_pokemon.items()):
            column=6
            margin_x=50
            margin_y=100
            space_between=100
            actual_column=index%column
            actual_lign=index//column
            x=margin_x+(actual_column*space_between)
            y=margin_y+(actual_lign*space_between)
            rect=pygame.Rect(x,y,64,64)
            image_path=pokemon["sprite"]
            image=pygame.image.load(image_path)
            image = pygame.transform.scale(image, (64, 64))
            rect = pygame.Rect(x, y, 64, 64)
            self.buttons_pokemon.append({
                "rect":rect,
                "image":image,
                "id":pokemon_id,
                "data":pokemon
            })
     
    def event_gestion(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            mouse_position=pygame.mouse.get_pos()
            for buttons in self.buttons_pokemon:
                if buttons["rect"].collidepoint(mouse_position):
                    self.pokemon_choosen=buttons["data"]
                    self.pokemon_choosen_id=buttons["id"]
            if self.pokemon_choosen_id:
                go_button = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 80, 120, 50)
                if go_button.collidepoint(mouse_position):
                  return "GO_FIGHT"
        return None
    
    def draw(self,screen):
     screen.fill((20, 20, 40))  
   
   
     title = self.font_bold.render("Choose your Pokemon!", True, (255, 255, 255))
     screen.blit(title, (200, 20))
    
     for button in self.buttons_pokemon:
        screen.blit(button["image"], button["rect"])
        
        if self.pokemon_choosen_id == button["id"]:
            pygame.draw.rect(screen, (GOLD), button["rect"], 3)  
    
     if self.pokemon_choosen_id:
        go_button = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 80, 120, 50)
        pygame.draw.rect(screen, (0, 200, 0), go_button)
        text_go = self.font_normal.render("GO!", True, (255, 255, 255))
        screen.blit(text_go, (go_button.x + 35, go_button.y + 10))


