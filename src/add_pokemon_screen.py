import pygame
from constant import *
from pokemon import Pokemon

class AddPokemonScreen:
    def __init__(self, screen):
        self.screen = screen
        # Chargement et redimensionnement propre
        original_bg = pygame.image.load("assets/images/add_pokemon.jpg").convert()
        self.background = pygame.transform.smoothscale(original_bg, (1280, 720))
        
        self.font_simple = FONT2
        self.font_bold = FONT1

        # On espace les champs de 80 pixels verticalement pour remplir l'écran 720p
        self.fields = {
            "name":    {"rect": pygame.Rect(450, 100, 400, 40), "text": ""},
            "type":    {"rect": pygame.Rect(450, 180, 400, 40), "text": ""},
            "level":   {"rect": pygame.Rect(450, 260, 400, 40), "text": ""},
            "hp":      {"rect": pygame.Rect(450, 390, 400, 40), "text": "50"},
            "attack":  {"rect": pygame.Rect(450, 500, 400, 40), "text": ""},
            "defense": {"rect": pygame.Rect(450, 580, 400, 40), "text": ""}
        }
        
        self.active_field = None
        # Bouton SAVE centré en bas
        self.save = pygame.Rect(540, 650, 200, 50)
    
    def event_gestion(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active_field = None
            for key, field in self.fields.items():
                if field["rect"].collidepoint(event.pos):
                    self.active_field = key
            
            if self.save.collidepoint(event.pos):
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
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "MENU"
        return None
    
    def save_new_pokemon(self):
        f = self.fields
        default_sprite = "assets/images/default.png"
        hp_value=int(f["hp"]["text"] or 50)
         
        # Correction des parenthèses pour les conversions int
        Pokemon.add_pokemon(
            f["name"]["text"] or "Unknow",
            f["type"]["text"] or "Normal",
            int(f["level"]["text"] or 1),
            hp_value,
            hp_value,
            int(f["attack"]["text"] or 10),
            int(f["defense"]["text"] or 10),
            default_sprite
        )

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        for key, field in self.fields.items():
            # Label à gauche du rectangle
            label = self.font_simple.render(f"{key.replace('_', ' ').capitalize()}:", True, (255, 255, 255))
            screen.blit(label, (250, field["rect"].y + 5))
            
            # Champ de saisie
            color = (255, 215, 0) if self.active_field == key else (255, 255, 255)
            pygame.draw.rect(screen, color, field["rect"], 2)
            
            # Texte dans le champ
            txt_surface = self.font_simple.render(field["text"], True, (255, 255, 255))
            screen.blit(txt_surface, (field["rect"].x + 10, field["rect"].y + 5))

        # Bouton Sauvegarder
        pygame.draw.rect(screen, (0, 150, 0), self.save)
        btn_txt = self.font_simple.render("SAVE", True, (255, 255, 255))
        screen.blit(btn_txt, (self.save.x + 65, self.save.y + 10))







    

