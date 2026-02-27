"""
fight.py
Logic module handling battle mechanics, including damage calculation,
type advantages, capturing mechanics, and Pokédex persistence.
"""

import random
from src.pokemon import *
from src.type import *
import json
from src.sound_management import SoundManager

class Fight:
    """
    Manages the core battle logic between the player's Pokémon and a random opponent.
    Includes healing, damage multipliers, and saving progress.
    """
    def __init__(self, pokemon, all_data):
        """Initializes a new fight with a random opponent from available data."""
        self.pokemon=pokemon
        # Select a random ID from the dictionary of all existing Pokémon
        random_id=random.choice(list(all_data.keys()))
        self.opponent=Pokemon(random_id, all_data)
        self.sound=SoundManager()

    def check_victory(self, msg):
        """Checks if the opponent has been defeated and returns a result message."""
        if not self.opponent.is_alive():
            msg=f"{self.pokemon.name} won! {self.opponent.name} lost!"
            return True, msg
        else:
            msg=f"{self.opponent.name} managed to win! You lost!"
            return False, msg
    
    def catch_pokemon(self):
        """Calculates the 50/50 chance of capturing the wild Pokémon."""
        catching_chances=random.randint(1, 100)
        if catching_chances <= 50:
            msg="Oh no! This pokemon escaped!"
            return False, msg
        else:
            self.sound.play("capture")
            msg="Good Job! You caught this pokemon!"
            return True, msg
       
    def potion(self):
        """Heals the player's Pokémon by up to 40 HP, capped at max HP."""
        msg="Already at max HP!"
        if self.pokemon.is_alive():
            if self.pokemon.hp < self.pokemon.hp_max:
                old_hp=self.pokemon.hp
                self.pokemon.hp=min(self.pokemon.hp + 40, self.pokemon.hp_max) 
                heal=self.pokemon.hp - old_hp 
                msg=f"{self.pokemon.name} healed {heal} HP"
        return msg
                        
    def save_to_pokedex(self, pokemon_to_save, caught):
        """
        Updates pokedex.json with the encounter data. 
        If the Pokémon is already listed, updates its 'captured' status.
        """
        try:
            with open("pokedex.json", "r") as f:
                pokedex=json.load(f)
        except(FileNotFoundError, json.JSONDecodeError):
            pokedex=[]
        
        # Check if Pokémon already exists in Pokedex to update instead of append
        found=False
        for p in pokedex:
            if p["name"]==pokemon_to_save.name:
                if caught: p["captured"]=True
                found=True
                break

        if not found:
            new_data={
                "name":pokemon_to_save.name,
                "type":pokemon_to_save.type,
                "defense":pokemon_to_save.defense,
                "attack":pokemon_to_save.attack,
                "hp":pokemon_to_save.hp,
                "sprite":pokemon_to_save.sprite_path,
                "captured":caught
            }
            pokedex.append(new_data)
        
        with open("pokedex.json", "w") as f:
            json.dump(pokedex, f, indent=4)
        
        return f"{pokemon_to_save.name} has been added to the pokedex!"

    def attack_power(self, attacker, target):
        """
        Calculates damage using attacker's stats vs target's defense.
        Incorporates a 10% chance to miss and type advantage multipliers.
        """
        accuracy=random.randint(1, 10)
        if accuracy > 1: # 90% accuracy rate
            attacker_type=attacker.type[0]
            def_type=target.type
            multiplicator=self.damage_mutliplying(attacker_type, def_type)

            # Core damage formula: (Atk / Def) * 10 * Multiplier
            base_damage=(attacker.attack / max(1, target.defense)) * 10
            total_damage=int(base_damage * multiplicator)
            target.take_damage(total_damage)

            # Feedback message based on effectiveness
            if multiplicator > 1:
                msg=f"{attacker.name} attacked! {total_damage} DMG! It's super effective!"
            elif multiplicator < 1:
                msg=f"{attacker.name} attacked! {total_damage} DMG! It's not very effective..."
            else:
                msg=f"{attacker.name} attacked! {total_damage} DMG!"
        else:
            msg="Oups! Attack missed!"

        return msg

    def damage_mutliplying(self, attacker_type, defender_type):
        """
        Determines the total damage multiplier by checking the attacker's type 
        against all types of the defender.
        """
        
        total_multiplicator=1
        for t in defender_type:       
            # Lookup bonus in TYPE_DAMAGE dictionary from src.type
            bonus=TYPE_DAMAGE.get(attacker_type, {}).get(t, 1)
            total_multiplicator *= bonus
        return total_multiplicator