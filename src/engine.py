import pygame
import json
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
     self.selection_screen=SelectionScreen(self.screen)
     self.fight_screen=FightScreen(self.screen)
     self.width=SCREEN_WIDTH
     self.height=SCREEN_HEIGHT
     pygame.display.set_caption("Pokémon")
     self.clock=pygame.time.Clock()
     self.running=True
     self.pokemon=None
     self.draw_menu=Menu_screen(self.screen)
    
    def event(self):
      for event in pygame.event.get():
        if event.type==pygame.QUIT:
            self.running=False

        if self.state=="SELECTION":
           action=self.selection_screen.event_gestion(event)
           if action=="GO_FIGHT":
              choosen_id=self.selection_screen.pokemon_choosen_id
              all_data=self.selection_screen.all_pokemon
              self.pokemon=Pokemon(choosen_id,all_data)
              self.state=="FIGHT"          
    
    def update(self):
        pass

    def draw(self):
        if self.state=="SELECTION":
           self.selection_screen.draw()

        pygame.display.flip()

    def run(self):
     while self.running:
        self.event()
        self.update()
        self.draw()
        self.clock.tick(60)

     pygame.quit()
     sys.exit()

if __name__=="__main__":
   game=Game()
   game.run()



