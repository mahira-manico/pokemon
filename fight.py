import random
from pokemon import *
from config import *
import json

class Fight:
    def __init__(self,pokemon, all_data):
        self.pokemon=pokemon
        random_id=random.choice(list(all_data.keys()))
        self.opponent=Pokemon(random_id,all_data)
    
    def check_victory(self):
        if not self.opponent.is_alive():
           print(f"{self.pokemon.name} won! {self.opponent.name} lost!")
           return True
        else:
         print(f"{self.opponent.name} managed to win! You lost!")
         return False
    
    def catch_pokemon(self):
       catching_chances=random.randint(1,100)
       if self.check_victory:
          if catching_chances<=50:
             print("Oh no! This pokemon escaped!")
             return False
          elif catching_chances>=50:
             print("Good Job! You caught this pokemon!")
             return True
          
    def save_to_pokedex(self,pokemon_to_save):
        try:
           with open("pokedex.json","r") as f:
              pokedex=json.load(f)
        except(FileNotFoundError):
           pokedex=[]
        
        exist=any(p["name"]==pokemon_to_save.name for p in pokedex)

        if not exist:
           new_data={
              "name":pokemon_to_save.name,
              "type":pokemon_to_save.type,
              "defense":pokemon_to_save.defense,
              "attack":pokemon_to_save.attack,
              "hp":pokemon_to_save.hp,
              "captured":self.catch_pokemon()
          }
           pokedex.append(new_data)
        
           with open("pokedex.json","w") as f:
            json.dump(pokedex, f, indent=4)
           print(f"{pokemon_to_save.name} have been added to pokedex!")
        else:
           print(f"{pokemon_to_save.name} already exist")
        

    def attack_power(self,attacker,target):
       attack=random.randint(1,10)
       if attack>1:
        attack_type=attacker.type[0]
        def_type=target.type[0]
        multiplicator=self.damage_mutliplying(attack_type,def_type)
        total_damage=attacker.attack*multiplicator
        target.take_damage(total_damage)
       else:
        print("Oups! Attack missed")

    def damage_mutliplying(self,attacker_type,defender_type):
        return TYPE_DAMAGE.get(attacker_type,{}).get(defender_type,1)

    def fight(self, all_data):
       
       while self.pokemon.is_alive() and self.opponent.is_alive():
           self.attack_power(self.pokemon,self.opponent)
        
           if self.opponent.is_alive():
               self.attack_power(self.opponent,self.pokemon)
           
       if self.check_victory():
          print(f"{self.pokemon.name} is evolving!")
          self.pokemon.raise_xp_level(all_data)
          self.save_to_pokedex(self.opponent)
       else:
          return
          

               
           
           
           

    
    

        