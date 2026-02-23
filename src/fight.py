import random
from pokemon import *
from type import *
import json

class Fight:
    def __init__(self,pokemon, all_data):
        self.pokemon=pokemon
        random_id=random.choice(list(all_data.keys()))
        self.opponent=Pokemon(random_id,all_data)
    
    def check_victory(self,msg):
        if not self.opponent.is_alive():
           msg=f"{self.pokemon.name} won! {self.opponent.name} lost!"
           return True,msg
        else:
           msg=f"{self.opponent.name} managed to win! You lost!"
           return False,msg
    
    def catch_pokemon(self):
       catching_chances=random.randint(1,100)
       if catching_chances<=50:
             msg="Oh no! This pokemon escaped!"
             return False,msg
       elif catching_chances>=50:
             msg="Good Job! You caught this pokemon!"
             return True,msg
       
    def potion(self):
     if self.pokemon.is_alive():
        if self.pokemon.hp >= self.pokemon.hp_max:  
            msg="Already at max HP!"
            
        old_hp=self.pokemon.hp
        self.pokemon.hp = min(self.pokemon.hp + 40, self.pokemon.hp_max) 
        heal=self.pokemon.hp-old_hp 
        msg = f"{self.pokemon.name} healed {heal} HP"

     return msg
                        

    def save_to_pokedex(self,pokemon_to_save,caught):
        try:
           with open("pokedex.json","r") as f:
              pokedex=json.load(f)
        except(FileNotFoundError):
           pokedex=[]
        
        for p in pokedex:
         if p["name"] == pokemon_to_save.name:
            if caught: p["captured"] = True
            with open("pokedex.json", "w") as f:
                json.dump(pokedex, f, indent=4)
            return f"{pokemon_to_save.name} updated!"

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
        
        with open("pokedex.json","w") as f:
            json.dump(pokedex, f, indent=4)
        msg=f"{pokemon_to_save.name} have been added to pokedex!"
        return msg
        

    def attack_power(self,attacker,target):
       attack=random.randint(1,10)
       if attack>1:
        attack_type=attacker.type[0]
        def_type=target.type
        multiplicator=self.damage_mutliplying(attack_type,def_type)

        base_damage=(attacker.attack/max(1, target.defense)) * 10
        total_damage=int(base_damage*multiplicator)
        target.take_damage(total_damage)

        if multiplicator>1:
           msg= f"{attacker.name} attacked! {total_damage} DMG! It's super effective"
        elif multiplicator<1:
           msg=f"{attacker.name} attacked! {total_damage} DMG! It's not very effective"
        else:
           msg=f"{attacker.name} attacked! {total_damage} DMG!"

       else:
         msg="Oups! Attack missed"
       return msg


    def damage_mutliplying(self,attacker_type,defender_type):
        total_multiplicator=1
        for t in defender_type:       
         bonus=TYPE_DAMAGE.get(attacker_type,{}).get(t,1)
         total_multiplicator*=bonus
        return total_multiplicator



               
           
           
           

    
    

        