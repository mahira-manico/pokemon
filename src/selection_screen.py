import json
import pygame

class SelectionScreen:
    def __init__(self,screen):
        self.screen=screen
        self.pokemon_choosen=None
        self.pokemon_choosen_id=None
        self.buttons_pokemon=[]
        self.load_pokemon()
        self.all_pokemon={}

    def load_pokemon(self):
        with open("data/pokemon.json", "r") as file:
            self.all_pokemon=json.load(file)
        for index, (pokemon_id,pokemon) in enumerate(self.all_pokemon.items()):
            column=6
            margin_x=50
            margin_y=100
            space_between=80
            actual_column=index%column
            actual_lign=index//column
            x=margin_x+(actual_column*space_between)
            y=margin_y+(actual_lign*space_between)
            rect=pygame.Rect(x,y,64,64)
            image_path=pokemon["sprite"]
            image=pygame.image.load(image_path)
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
    
    def draw(self,screen):
        pass

