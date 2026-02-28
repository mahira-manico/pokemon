"""
pokemon.py
Core entity module for Pokémon. Handles attribute initialization, 
stat scaling, leveling, evolution logic, and static data management.
"""

import json
import pygame

class Pokemon:
    """
    Represents a Pokémon instance with dynamic stats that change 
    through battle experience and evolution.
    """
    def __init__(self, pokemon_id, all_data):
        """
        Initializes a Pokémon by fetching its base data from a dictionary.
        
        Args:
            pokemon_id (str/int): The unique ID of the Pokémon in the dataset.
            all_data (dict): The full dictionary of Pokémon data loaded from JSON.
        """
        file=all_data[str(pokemon_id)]
        self.id=pokemon_id
        self.xp=0
        self.load_attributes(file)

    def load_attributes(self, file):
        """
        Maps dictionary data to object attributes and loads the sprite.
        This is called both on initialization and during evolution.
        """
        self.name=file["name"]
        self.type=file["type"]
        self.level=file["level"]
        self.hp=int(file["hp"])
        self.hp_max=int(file["hp"])
        self.attack=int(file["attack"])
        self.defense=int(file["defense"])
        self.xp=file.get("xp", 0)
        self.evolution_id=file.get("evolution_id", None)
        self.evolution_level=file.get("evolution_level", None)
        self.sprite_path=file["sprite"]
        
        # Load visual asset
        self.sprite=pygame.image.load(self.sprite_path)

    def __str__(self):
        """Returns a formatted string representing the Pokémon's current state."""
        display=f"--Pokémon Data--\n"
        display+=f"Name: {self.name}(lv.{self.level}\n)"
        display+=f"Type: {'/'.join(self.type)}\n"
        display+=f"Health: {self.hp}/{self.hp_max}\n"
        display+=f"Stats: ATK:{self.attack}/DEF: {self.defense}\n"
        
        if self.evolution_id:
            display+=f"Evolve at level: {self.evolution_level} in {self.evolution_id}\n"
        else:
            display+=f"This Pokemon is at his final stage of evolution\n"
        return display

    def is_alive(self):
        """Checks if the Pokémon still has Health Points remaining."""
        return self.hp > 0
    
    def evolve(self, new_data):
        """
        Triggers the transformation into a new Pokémon form if requirements are met.
        
        Args:
            new_data (dict): The dataset containing the new evolution's stats.
        Returns:
            bool: True if evolution was successful, False otherwise.
        """
        if self.evolution_level is not None and self.level >= self.evolution_level and self.evolution_id is not None:
            new_id=str(self.evolution_id)
            if new_id in new_data:
                new_form_data=new_data[new_id]
                self.load_attributes(new_form_data)
                return True
        return False

    def raise_xp_level(self, new_data):
        """
        Increases XP and handles Level Up logic including stat growth 
        and evolution checks.
        """
        self.xp += 50
        if self.xp >= 100:
            self.level += 1
            self.xp=0
            # Stat growth per level
            self.hp += 5
            self.hp_max += 5
            self.attack += 3
            self.defense += 3
            # Check for evolution eligibility
            self.evolve(new_data)
    
    def take_damage(self, damage):
        """
        Calculates health reduction after applying defense mitigation.
        
        Args:
            damage (int): Incoming raw damage from an opponent.
        """
        reduction=self.defense * 0.1
        total_damage=max(5, damage - reduction) # Guaranteed minimum damage  
        self.hp -= int(total_damage)
        self.hp=max(0, int(self.hp))

    @staticmethod
    def add_pokemon(file_path, name, type, level, hp, attack, defense, sprite, evolution_id=None, evolution_level=None):
        """
        Static method to append a new custom Pokémon to the persistent storage.
        
        Args:
            file_path (str): Path to the JSON save file.
            ... stats ...
        """
        try:
            with open(file_path, "r") as file:
                all_pokemon=json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            all_pokemon={}
          
        # Auto-increment ID based on existing entries
        if all_pokemon:
            max_id=max(int(key) for key in all_pokemon.keys())
            new_id=str(max_id + 1)
        else:
            new_id="1"

        new_pokemon={
            "name":name,
            "type":type if isinstance(type, list) else [type],
            "level":level,
            "hp":hp,
            "hp_max":hp,
            "attack":attack,
            "defense":defense,
            "evolution_id":evolution_id,
            "evolution_level":evolution_level,   
            "sprite":sprite,
            "xp":0
        }
          
        all_pokemon[new_id]=new_pokemon

        try:    
            with open(file_path, "w") as file:
                json.dump(all_pokemon, file, indent=2)
            return True
        except Exception:
            return False