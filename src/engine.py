import pygame
import sys
from fight import Fight
from menu import Menu_screen
from pokemon import Pokemon
from fight_screen import FightScreen
from selection_screen import SelectionScreen
from constant import *
from pokedex_screen import PokedexScreen
from add_pokemon_screen import AddPokemonScreen
from gameover_screen import GameOverScreen


class Game:
    def __init__(self):
     pygame.init()

     with open("pokedex.json", "w") as f:
            import json
            json.dump([], f)

     self.screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
     self.state="MENU"
     self.game_over_message = ""
     self.menu_screen=Menu_screen(self.screen)
     self.selection_screen=SelectionScreen(self.screen)
     self.add_pokemon_screen=AddPokemonScreen(self.screen)
     self.game_over_screen=GameOverScreen(self.screen)
     self.width=SCREEN_WIDTH
     self.height=SCREEN_HEIGHT
     pygame.display.set_caption("Pokémon")
     self.clock=pygame.time.Clock()
     self.running=True
     self.pokemon=None
     self.draw_menu=Menu_screen(self.screen)
     self.draw_fight=FightScreen(self.screen)
     self.pokedex_screen = PokedexScreen(self.screen)
    
    
    def event(self):
      for event in pygame.event.get():
        if event.type==pygame.QUIT:
            self.running=False

        if self.state=="MENU":
           action=self.menu_screen.event_gestion(event)
           if action=="GAME":
              self.state="SELECTION"
           elif action=="POKEDEX":
              self.pokedex_screen.load_pokedex()
              self.state = "POKEDEX"
           elif action=="LIST":
              self.state="ADD_POKEMON"
        elif self.state == "POKEDEX":
         action = self.pokedex_screen.event_gestion(event)
         if action == "BACK_TO_MENU":
          self.state = "MENU"   

        elif self.state=="ADD_POKEMON":
          action=self.add_pokemon_screen.event_gestion(event) 
          if action=="MENU":
            self.selection_screen.refresh()
            self.state="MENU"

        elif self.state=="SELECTION":
           action=self.selection_screen.event_gestion(event)
           if action=="GO_FIGHT":
              choosen_id=self.selection_screen.pokemon_choosen_id
              all_data=self.selection_screen.all_pokemon
              self.pokemon=Pokemon(choosen_id,all_data)
              self.state="FIGHT"    
              self.fight=Fight(self.pokemon,all_data)

              self.draw_fight.player_pokemon=self.pokemon
              self.draw_fight.opponent=self.fight.opponent
              self.draw_fight.message="A wild Pokémon appeared!"

        elif self.state=="FIGHT":
           action=self.draw_fight.event_gestion(event)   

           if action=="ATTACK":
              
             player_msg = self.fight.attack_power(self.pokemon, self.fight.opponent) 
             self.draw_fight.message = player_msg  
    
  
             if not self.fight.opponent.is_alive():
              old_level = self.pokemon.level
              
              self.pokemon.xp+=10
              self.pokemon.raise_xp_level(self.selection_screen.all_pokemon)
              pid = str(self.pokemon.id)
              self.selection_screen.all_pokemon[pid]["xp"] = self.pokemon.xp
              self.selection_screen.all_pokemon[pid]["level"] = self.pokemon.level

              xp_msg = f"\n{self.pokemon.name} gained 10 XP!"
              if self.pokemon.level > old_level:
               xp_msg += f"\nLEVEL UP! {self.pokemon.name} is now Lv.{self.pokemon.level}!"
                      
              caught, catch_msg = self.fight.catch_pokemon()
         
              if caught:
               save_msg = self.fight.save_to_pokedex(self.fight.opponent,caught)
               self.game_over_message = f"{self.pokemon.name} won!\n{catch_msg}\n{save_msg}"
              else:
               self.game_over_message = f"{self.pokemon.name} won!\n{catch_msg}{xp_msg}"
      
              self.state = "GAME_OVER"
    
             else:  
               opponent_msg = self.fight.attack_power(self.fight.opponent, self.pokemon)
               self.draw_fight.message = f"{player_msg}\n{opponent_msg}"  
        
               if not self.pokemon.is_alive():
                self.game_over_message = f"{self.pokemon.name} lost..."
                self.state = "GAME_OVER"

           elif action=="POTION":
             msg=self.fight.potion() 
             opponent_msg = self.fight.attack_power(self.fight.opponent, self.pokemon)
             self.draw_fight.message = f"{msg}\n{opponent_msg}"
             
             if self.fight.opponent.is_alive():
                opponent_msg = self.fight.attack_power(self.fight.opponent, self.pokemon)
                self.draw_fight.message = f"{msg}\n{opponent_msg}"
                
                if not self.pokemon.is_alive():
                 self.game_over_message = f"{self.pokemon.name} lost..."
                 self.state = "GAME_OVER"
                                     
           elif action=="ESCAPE":
             self.game_over_message = "You fled from battle!"
             self.state = "GAME_OVER"

        elif self.state == "GAME_OVER":
             if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_SPACE:  
               self.state = "MENU"
              elif event.key == pygame.K_r: 
               self.state = "SELECTION"


    def draw(self):
        
        if self.state == "MENU":
         self.menu_screen.draw(self.screen)

        elif self.state=="FIGHT":
          self.draw_fight.draw(self.screen)

        elif self.state=="SELECTION":
           self.selection_screen.draw(self.screen)
         
        elif self.state == "POKEDEX":
         self.pokedex_screen.draw(self.screen)
      
        elif self.state=="ADD_POKEMON":
          self.add_pokemon_screen.draw(self.screen)

        elif self.state == "GAME_OVER":
           self.draw_fight.draw(self.screen)
           self.game_over_screen.draw(self.game_over_message)
        pygame.display.flip()

    def run(self):
     while self.running:
        self.event()
        self.draw()
        self.clock.tick(60)

     pygame.quit()
     sys.exit()

if __name__=="__main__":
   game=Game()
   game.run()



