import pygame
import sys
from fight import Fight
from menu import Menu_screen
from pokemon import Pokemon
from fight_screen import FightScreen
from selection_screen import SelectionScreen
from constant import *


class Game:
    def __init__(self):
     pygame.init()
     self.screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
     self.state="MENU"
     self.game_over_message = ""
     self.menu_screen=Menu_screen(self.screen)
     self.selection_screen=SelectionScreen(self.screen)
     self.width=SCREEN_WIDTH
     self.height=SCREEN_HEIGHT
     pygame.display.set_caption("Pokémon")
     self.clock=pygame.time.Clock()
     self.running=True
     self.pokemon=None
     self.draw_menu=Menu_screen(self.screen)
     self.draw_fight=FightScreen(self.screen)
    
    
    def event(self):
      for event in pygame.event.get():
        if event.type==pygame.QUIT:
            self.running=False

        if self.state=="MENU":
           action=self.menu_screen.event_gestion(event)
           if action=="GAME":
              self.state="SELECTION"
           elif action=="POKEDEX":
              pass
           elif action=="LIST":
              pass             

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
              msg=self.fight.attack_power(self.pokemon,self.fight.opponent)
              self.draw_fight.message = msg 
              if not self.fight.opponent.is_alive():
               self.draw_fight.message=f"{self.pokemon.name} won!"
               self.pokemon.raise_xp_level(self.selection_screen.all_pokemon)
               caught, catch_msg = self.fight.catch_pokemon()
               self.game_over_message = f"{self.pokemon.name} won!\n{catch_msg}"
               if caught:
                save_msg = self.fight.save_to_pokedex(self.fight.opponent)
                self.game_over_message += f"\n{save_msg}"
               self.state = "GAME_OVER"
              else:
               msg=self.fight.attack_power(self.fight.opponent, self.pokemon)
               self.draw_fight.message+=f"\n{msg}"

               if not self.pokemon.is_alive():
                self.game_over_message = f"{self.pokemon.name} lost..."
                self.state = "GAME_OVER"
           elif self.state == "GAME_OVER":
             if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_SPACE:  
               self.state = "MENU"
              elif event.key == pygame.K_r: 
               self.state = "SELECTION"

           elif action=="POTION":
              msg=self.fight.potion() 
              print(msg) 
              if self.fight.opponent.is_alive():
               msg=self.fight.attack_power(self.fight.opponent, self.pokemon)
               print(msg)
                
               if not self.pokemon.is_alive():
                  print("tu a perdu")
                  self.state="MENU"
                                     
           elif action=="ESCAPE":
              self.state="MENU"


    def draw(self):
        
        if self.state == "MENU":
         self.menu_screen.draw(self.screen)

        elif self.state=="FIGHT":
          self.draw_fight.draw(self.screen)

        elif self.state=="SELECTION":
           self.selection_screen.draw(self.screen)

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



