"""
sound_management.py
Centralized sound system manager. Handles background music, 
UI sound effects, and dynamic Pokémon cries based on their types.
"""

import pygame
import random

class SoundManager:
    """
    Manages all audio assets. Supports playing specific sound effects, 
    looping background music, and generating type-based battle sounds.
    """
    def __init__(self):
        """Initializes the mixer and pre-loads all sound assets into memory."""
        pygame.mixer.init()
        
        # Specific cry for Pikachu
        self.pokemon_cries={
            "Pikachu": pygame.mixer.Sound("assets/sounds/pikachu_cry.mp3"),
        }

        # Generic attack sounds categorized by Pokémon Type
        self.type_sounds={
            "Normal": [
                pygame.mixer.Sound("assets/sounds/normal_1.mp3"),
                pygame.mixer.Sound("assets/sounds/normal_2.mp3"),
                pygame.mixer.Sound("assets/sounds/normal_3.mp3")
            ],
            "Fire": [
                pygame.mixer.Sound("assets/sounds/fire_1.mp3"),
                pygame.mixer.Sound("assets/sounds/fire_2.mp3"),
                pygame.mixer.Sound("assets/sounds/fire_3.mp3")
            ],
            "Water": [
                pygame.mixer.Sound("assets/sounds/water_1.mp3"),
                pygame.mixer.Sound("assets/sounds/water_2.mp3"),
                pygame.mixer.Sound("assets/sounds/water_3.mp3")
            ],
            "Grass": [
                pygame.mixer.Sound("assets/sounds/grass_1.mp3"),
                pygame.mixer.Sound("assets/sounds/grass_2.mp3"),
                pygame.mixer.Sound("assets/sounds/grass_3.mp3")
            ],
            "Electric": [
                pygame.mixer.Sound("assets/sounds/elec_1.mp3"),
                pygame.mixer.Sound("assets/sounds/elec_2.mp3"),
                pygame.mixer.Sound("assets/sounds/elec_3.mp3")
            ],
            "Ice": [
                pygame.mixer.Sound("assets/sounds/ice_1.mp3"),
                pygame.mixer.Sound("assets/sounds/ice_2.mp3"),
                pygame.mixer.Sound("assets/sounds/ice_3.mp3")
            ],
            "Fighting": [
                pygame.mixer.Sound("assets/sounds/fight_1.mp3"),
                pygame.mixer.Sound("assets/sounds/fight_2.mp3"),
                pygame.mixer.Sound("assets/sounds/fight_3.mp3")
            ],
            "Poison": [
                pygame.mixer.Sound("assets/sounds/poison_1.mp3"),
                pygame.mixer.Sound("assets/sounds/poison_2.mp3"),
                pygame.mixer.Sound("assets/sounds/poison_3.mp3")
            ],
            "Ground": [
                pygame.mixer.Sound("assets/sounds/ground_1.mp3"),
                pygame.mixer.Sound("assets/sounds/ground_2.mp3"),
                pygame.mixer.Sound("assets/sounds/ground_3.mp3")
            ],
            "Flying": [
                pygame.mixer.Sound("assets/sounds/fly_1.mp3"),
                pygame.mixer.Sound("assets/sounds/fly_2.mp3"),
                pygame.mixer.Sound("assets/sounds/fly_3.mp3")
            ],
            "Psychic": [
                pygame.mixer.Sound("assets/sounds/psy_1.mp3"),
                pygame.mixer.Sound("assets/sounds/psy_2.mp3"),
                pygame.mixer.Sound("assets/sounds/psy_3.mp3")
            ],
            "Bug": [
                pygame.mixer.Sound("assets/sounds/bug_1.mp3"),
                pygame.mixer.Sound("assets/sounds/bug_2.mp3"),
                pygame.mixer.Sound("assets/sounds/bug_3.mp3")
            ],
            "Rock": [
                pygame.mixer.Sound("assets/sounds/rock_1.mp3"),
                pygame.mixer.Sound("assets/sounds/rock_2.mp3"),
                pygame.mixer.Sound("assets/sounds/rock_3.mp3")
            ],
            "Ghost": [
                pygame.mixer.Sound("assets/sounds/ghost_1.mp3"),
                pygame.mixer.Sound("assets/sounds/ghost_2.mp3"),
                pygame.mixer.Sound("assets/sounds/ghost_3.mp3")
            ],
            "Dragon": [
                pygame.mixer.Sound("assets/sounds/dragon_1.mp3"),
                pygame.mixer.Sound("assets/sounds/dragon_2.mp3"),
                pygame.mixer.Sound("assets/sounds/dragon_3.mp3")
            ],
            "Dark": [
                pygame.mixer.Sound("assets/sounds/dark_1.mp3"),
                pygame.mixer.Sound("assets/sounds/dark_2.mp3"),
                pygame.mixer.Sound("assets/sounds/dark_3.mp3")
            ],
            "Steel": [
                pygame.mixer.Sound("assets/sounds/steel_1.mp3"),
                pygame.mixer.Sound("assets/sounds/steel_2.mp3"),
                pygame.mixer.Sound("assets/sounds/steel_3.mp3")
            ],
            "Fairy": [
                pygame.mixer.Sound("assets/sounds/fairy_1.mp3"),
                pygame.mixer.Sound("assets/sounds/fairy_2.mp3"),
                pygame.mixer.Sound("assets/sounds/fairy_3.mp3")
            ]
        }

        # General UI and Gameplay sound effects
        self.sounds={
            "click": pygame.mixer.Sound("assets/sounds/click.mp3"),
            "level_up": pygame.mixer.Sound("assets/sounds/level_up.mp3"),
            "victory": pygame.mixer.Sound("assets/sounds/victory.mp3"),
            "capture": pygame.mixer.Sound("assets/sounds/capture.mp3"),
            "potion": pygame.mixer.Sound("assets/sounds/potion.mp3"),
            "missed_attack": pygame.mixer.Sound("assets/sounds/missed.wav"),
            "evolution": pygame.mixer.Sound("assets/sounds/evolution.mp3"),
        }

    def play(self, name):
        """Plays a specific sound effect from the general sounds dictionary."""
        if name in self.sounds:
            self.sounds[name].play()

    def play_pokemon_sound(self, pokemon_obj):    
        """
        Determines and plays a sound for a Pokémon. 
        Prioritizes unique cries, then type-specific sounds, falling back to 'Normal'.
        """
        if pokemon_obj.name in self.pokemon_cries:
            self.pokemon_cries[pokemon_obj.name].play()
            return

        p_type=pokemon_obj.type
        if isinstance(p_type, list): p_type=p_type[0]

        if p_type in self.type_sounds:
            random.choice(self.type_sounds[p_type]).play()
        else:
            random.choice(self.type_sounds["Normal"]).play()

    def play_music(self, file_path):
        """Loads and plays background music on an infinite loop."""
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(0.3) 
        pygame.mixer.music.play(-1) 

    def stop_music(self):
        """Stops all active sound channels and background music."""
        pygame.mixer.stop()
        pygame.mixer.music.stop()