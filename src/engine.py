"""
engine.py
Main game engine that orchestrates screen transitions, event handling, 
and global game states.
"""

import pygame
import json
import shutil
import os
import sys
from src.sound_management import SoundManager
from src.fight import Fight
from src.menu import Menu_screen
from src.pokemon import Pokemon
from src.fight_screen import FightScreen
from src.selection_screen import SelectionScreen
from src.constant import *
from src.pokedex_screen import PokedexScreen
from src.add_pokemon_screen import AddPokemonScreen
from src.gameover_screen import GameOverScreen

class Game:
    """
    Core class responsible for the main game loop, state switching, 
    and data persistence.
    """
    def __init__(self):
        """Initializes Pygame, loads assets, and sets up the initial game state."""
        pygame.init()

        # Data persistence setup
        self.save_path="data/save_data.json"
        self.base_path="data/pokemon.json"      
        
        # Create a fresh save from base data if it doesn't exist
        if not os.path.exists(self.save_path):
            shutil.copy(self.base_path, self.save_path)
      
        self.screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pokémon Adventure")
        
        # State Machine Initialization
        self.state="MENU"
        self.game_over_message=""
        
        # Screen instances
        self.menu_screen=Menu_screen(self.screen)
        self.selection_screen=SelectionScreen(self.screen, self.save_path)
        self.add_pokemon_screen=AddPokemonScreen(self.screen, self.save_path)
        self.game_over_screen=GameOverScreen(self.screen)
        self.draw_fight=FightScreen(self.screen)
        self.pokedex_screen=PokedexScreen(self.screen)
        
        # Systems
        self.clock=pygame.time.Clock()
        self.running=True
        self.pokemon=None
        self.sound_manager=SoundManager()
        self.sound_manager.play_music("assets/sounds/menu_theme.wav")

    def save_pokemon_progress(self):
        """Updates the save_data.json with current Pokémon stats after a battle."""
        pid=str(self.selection_screen.pokemon_choosen_id)
      
        if pid in self.selection_screen.all_pokemon:
            self.selection_screen.all_pokemon[pid].update({
                "level":self.pokemon.level,
                "xp":self.pokemon.xp,
                "hp":self.pokemon.hp_max,
                "hp_max":self.pokemon.hp_max,
                "attack":self.pokemon.attack,
                "defense":self.pokemon.defense,
                "name":self.pokemon.name,
                "sprite":self.pokemon.sprite_path
            })
            
            # Handle evolution
            if self.pokemon.evolution_id:
                self.selection_screen.all_pokemon[pid]["evolution_id"]=self.pokemon.evolution_id
                self.selection_screen.all_pokemon[pid]["evolution_level"]=self.pokemon.evolution_level
        
            with open(self.save_path, "w") as f:
                json.dump(self.selection_screen.all_pokemon, f, indent=2)
        
        self.selection_screen.refresh()

    def event(self):
        """Central event dispatcher that delegates logic based on the current state."""
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running=False

            # MENU STATE 
            if self.state=="MENU":
                action=self.menu_screen.event_gestion(event)
                if action:
                    self.sound_manager.play("click")

                if action=="RESET_DATA":       
                    if os.path.exists(self.save_path):
                        os.remove(self.save_path)
                    if os.path.exists("pokedex.json"):
                        os.remove("pokedex.json")
                    shutil.copy(self.base_path, self.save_path)

                    self.selection_screen.load_pokemon()
                    self.pokedex_screen.load_pokedex()
                    self.menu_screen.trigger_reset_message()
                    self.state="MENU"

                elif action=="GAME": self.state="SELECTION"
                elif action=="POKEDEX":
                    self.pokedex_screen.load_pokedex()
                    self.state="POKEDEX"
                elif action=="LIST": self.state="ADD_POKEMON"

            # POKEDEX STATE 
            elif self.state=="POKEDEX":
                action=self.pokedex_screen.event_gestion(event)
                if action:
                    self.sound_manager.play("click")
                    if action=="BACK_TO_MENU": self.state="MENU"

            # ADD POKEMON STATE 
            elif self.state=="ADD_POKEMON":
                action=self.add_pokemon_screen.event_gestion(event) 
                if action:
                    self.sound_manager.play("click")
                    if action=="MENU":
                        self.selection_screen.refresh()
                        self.state="MENU"

            # SELECTION STATE 
            elif self.state=="SELECTION":
                action=self.selection_screen.event_gestion(event)
                if action:
                    self.sound_manager.play("click")
                    if action=="BACK_TO_MENU":
                        self.state="MENU"
                    elif action=="GO_FIGHT":
                        self.sound_manager.stop_music()
                        self.sound_manager.play_music("assets/sounds/fight.mp3")
                        self.draw_fight.setup_new_fight()
                        
                        # Initialize Battle Entities
                        choosen_id=self.selection_screen.pokemon_choosen_id
                        all_data=self.selection_screen.all_pokemon
                        self.pokemon=Pokemon(choosen_id, all_data) 
                        self.fight=Fight(self.pokemon, all_data)

                        self.draw_fight.player_pokemon=self.pokemon
                        self.draw_fight.opponent=self.fight.opponent
                        self.draw_fight.message="A wild Pokémon appeared!"
                        self.state="FIGHT" 

            # FIGHT STATE 
            elif self.state=="FIGHT":
                action=self.draw_fight.event_gestion(event)   
                if action=="ATTACK":   
                    self.sound_manager.play("click")
                    player_msg=self.fight.attack_power(self.pokemon, self.fight.opponent) 
                    
                    if player_msg==False: # Missed attack
                        self.sound_manager.play("missed")
                    else:
                        self.sound_manager.play_pokemon_sound(self.pokemon)  
                        self.draw_fight.message=player_msg  
                        self.draw_fight.shake_intensity=10
              
                    # Check Victory
                    if not self.fight.opponent.is_alive():
                        self.handle_victory()
                    else:   
                        # Opponent Riposte
                        opponent_msg=self.fight.attack_power(self.fight.opponent, self.pokemon)
                        self.sound_manager.play_pokemon_sound(self.fight.opponent)
                        self.draw_fight.message=f"{player_msg}\n{opponent_msg}"  
                
                        if not self.pokemon.is_alive():
                            self.handle_defeat()

                elif action=="POTION":
                    self.sound_manager.play("potion")
                    msg=self.fight.potion() 
                    opp_msg=self.fight.attack_power(self.fight.opponent, self.pokemon)
                    self.draw_fight.message=f"{msg}\n{opp_msg}"
                    if not self.pokemon.is_alive(): self.handle_defeat()
                                     
                elif action=="ESCAPE":
                    self.game_over_message="You fled from battle!"
                    self.sound_manager.play_music("assets/sounds/game_over.mp3")
                    self.state="GAME_OVER"

            # GAME OVER STATE 
            elif self.state=="GAME_OVER":
                if event.type==pygame.KEYDOWN:
                    self.sound_manager.play("click")
                    if event.key==pygame.K_SPACE:  
                        self.sound_manager.stop_music()
                        self.sound_manager.play_music("assets/sounds/menu_theme.wav")
                        self.state="MENU"
                    elif event.key==pygame.K_r: 
                        self.state="SELECTION"

    def handle_victory(self):
        """Utility method to manage sounds, XP, and state transition upon winning."""
        self.sound_manager.stop_music()
        self.sound_manager.play("victory")
        self.draw_fight.shake_intensity=0

        old_level=self.pokemon.level
        old_name=self.pokemon.name
        
        self.pokemon.raise_xp_level(self.selection_screen.all_pokemon)
        self.save_pokemon_progress()

        msg=f"{old_name} won!\nGained 50 XP!"
        
        # Check Level Up
        if self.pokemon.level > old_level:
            msg+=f"\nLEVEL UP! Now Lv.{self.pokemon.level}!"
        
        # Check Evolution
        if self.pokemon.name != old_name:
            self.sound_manager.play("evolution")
            msg+=f"\nWHAT? {old_name} evolved into {self.pokemon.name}!"
        
        # Check Capture
        caught, catch_msg=self.fight.catch_pokemon()
        msg+=f"\n{catch_msg}"
     
        self.fight.save_to_pokedex(self.fight.opponent, caught)
        
        self.game_over_message=msg
        
        self.sound_manager.play_music("assets/sounds/game_over.mp3")
        self.state="GAME_OVER"

    def handle_defeat(self):
        """Utility method to manage sounds and state transition upon losing."""
        self.sound_manager.stop_music()
        self.sound_manager.play("game_over")
        self.draw_fight.shake_intensity=0
        self.game_over_message=f"{self.pokemon.name} lost..."
        self.sound_manager.play_music("assets/sounds/game_over.mp3")
        self.state="GAME_OVER"

    def draw(self):
        """Calls the draw method of the currently active screen."""
        if self.state=="MENU": 
            self.menu_screen.draw(self.screen)
        elif self.state=="FIGHT": 
            self.draw_fight.draw(self.screen)
        elif self.state=="SELECTION": 
            self.selection_screen.draw(self.screen)
        elif self.state=="POKEDEX": 
            self.pokedex_screen.draw(self.screen)
        elif self.state=="ADD_POKEMON": 
            self.add_pokemon_screen.draw(self.screen)
        elif self.state=="GAME_OVER":
            self.draw_fight.draw(self.screen)
            self.game_over_screen.draw(self.game_over_message)
        
        pygame.display.flip()

    def run(self):
        """The main game loop."""
        while self.running:
            self.event()
            if self.state=="FIGHT":
                self.draw_fight.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__=="__main__":
    game=Game()
    game.run()