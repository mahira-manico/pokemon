import pygame
from src.constant import *
from src.pokemon import Pokemon
from src.sound_management import SoundManager

class AddPokemonScreen:
    def __init__(self, screen,save_path):
        self.screen = screen

        original_bg = pygame.image.load("assets/images/add_pokemon.jpg").convert()
        self.background = pygame.transform.smoothscale(original_bg, (1280, 720))
        self.sound=SoundManager()
        self.save_path = save_path
        
        self.font_simple = FONT2
        self.font_bold = FONT1

        self.available_types = [
          "Normal", "Fire", "Water", "Grass", "Electric", "Ice", 
          "Fighting", "Poison", "Ground", "Flying", "Psychic", 
          "Bug", "Rock", "Ghost", "Dragon", "Steel", "Fairy"
        ]

        self.selected_type_index1 = 0 
        self.selected_type_index2 = None

        self.fields = {
            "name":    {"rect": pygame.Rect(450, 100, 400, 40), "text": ""},
            "type":    {"rect": pygame.Rect(450, 180, 400, 40), "text": ""},
            "level":   {"rect": pygame.Rect(450, 260, 400, 40), "text": ""},
            "hp":      {"rect": pygame.Rect(450, 390, 400, 40), "text": "50"},
            "attack":  {"rect": pygame.Rect(450, 500, 400, 40), "text": ""},
            "defense": {"rect": pygame.Rect(450, 580, 400, 40), "text": ""}
        }
        
        self.fields["type"]["text"] = self.available_types[self.selected_type_index1]
        self.active_field = None
        self.save = pygame.Rect(540, 650, 200, 50)
    
    def event_gestion(self, event):

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "MENU"
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if self.fields["type"]["rect"].collidepoint(mouse_pos):
             if event.button == 1: 
              self.selected_type_index1 = (self.selected_type_index1 + 1) % len(self.available_types)
  
             elif event.button == 3: 
              if self.selected_type_index2 is None:
                self.selected_type_index2 = 0
              else:
                self.selected_type_index2 += 1
                if self.selected_type_index2 >= len(self.available_types):
                    self.selected_type_index2 = None
  
             type1 = self.available_types[self.selected_type_index1]
             if self.selected_type_index2 is not None:
              type2 = self.available_types[self.selected_type_index2]
              self.fields["type"]["text"] = f"{type1} / {type2}"
             else:
              self.fields["type"]["text"] = type1
            
             self.sound.play("click")
             return None

            for key, field in self.fields.items():
                if field["rect"].collidepoint(mouse_pos):
                    self.active_field = key

            if self.save.collidepoint(mouse_pos):
                self.save_new_pokemon()
                return "MENU"
        
        if event.type == pygame.KEYDOWN and self.active_field:
            if event.key == pygame.K_BACKSPACE:
                self.fields[self.active_field]["text"] = self.fields[self.active_field]["text"][:-1]          
            elif event.key == pygame.K_RETURN:
                self.active_field = None           
            else:
                if event.unicode.isprintable():
                    self.fields[self.active_field]["text"] += event.unicode
    
        return None
    
    
    def save_new_pokemon(self):
        f = self.fields
        def safe_int(text, default):
            return int(text) if text.isdigit() else default
        
        raw_name = f["name"]["text"].strip().capitalize() or "Unknow"
        selected_type = f["type"]["text"]
        default_sprite = "assets/images/default.png"
        hp_value = safe_int(f["hp"]["text"], 50)

        types_list = [self.available_types[self.selected_type_index1]]
        if self.selected_type_index2 is not None:
         types_list.append(self.available_types[self.selected_type_index2])
         
        Pokemon.add_pokemon(
            file_path=self.save_path,
            name=raw_name,
            type=[selected_type],
            level=safe_int(f["level"]["text"],1),
            hp=hp_value,
            attack=safe_int(f["attack"]["text"],10),
            defense=safe_int(f["defense"]["text"],10),
            sprite=default_sprite
        )

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        for key, field in self.fields.items():
    
            label = self.font_simple.render(f"{key.replace('_', ' ').capitalize()}:", True, (255, 255, 255))
            screen.blit(label, (250, field["rect"].y + 5))
                
            color = (255, 215, 0) if self.active_field == key else (255, 255, 255)
            pygame.draw.rect(screen, color, field["rect"], 2)        
          
            txt_surface = self.font_simple.render(field["text"], True, (255, 255, 255))
            screen.blit(txt_surface, (field["rect"].x + 10, field["rect"].y + 5))

        pygame.draw.rect(screen, (0, 150, 0), self.save)
        btn_txt = self.font_simple.render("SAVE", True, (255, 255, 255))
        screen.blit(btn_txt, (self.save.x + 65, self.save.y + 10))

        cancel_txt = self.font_simple.render("ESC to Return", True, (200, 200, 200))
        screen.blit(cancel_txt, (20, 680))

        hint_txt = self.font_simple.render("Left Click: Type 1 | Right Click: Type 2", True, (180, 180, 180))
        screen.blit(hint_txt, (450, 225))







    

