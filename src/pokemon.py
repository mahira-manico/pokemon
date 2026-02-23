import json
import pygame


class Pokemon:
    def __init__(self,pokemon_id,all_data):
        file=all_data[str(pokemon_id)]
        self.id=pokemon_id
        self.xp=0
        self.load_attributes(file)

    def load_attributes(self,file):
        self.name=file["name"]
        self.type=file["type"]
        self.level=file["level"]
        self.hp=int(file["hp"])
        self.hp_max=int(file["hp"])
        self.attack=int(file["attack"])
        self.defense=int(file["defense"])
        self.xp = file.get("xp", 0)
        self.evolution_id=file.get("evolution_id",None)
        self.evolution_level=file.get("evolution_level",None)
        self.sprite_path=file["sprite"]
        self.sprite=pygame.image.load(self.sprite_path)

    def __str__(self):
        display=f"--Pokémon Data--\n"
        display+=f"Name: {self.name}(lv.{self.level}\n)"
        display+=f"Type: {'/'.join(self.type)}\n"
        display+=f"Health: {self.hp}/{self.hp_max}\n"
        display+=f"Stats: ATK:{self.attack}/DEF: {self.defense}\n"
        if self.evolution_id:
            display+=f"Evolve at level: {self.evolution_level} in {self.evolution_id}\n"
        else:
            display+=f"This Pokemon is at his final stage of evolution\n"

    def is_alive(self):
        if self.hp>0:
            return True
        return False
    
    def evolve(self,new_data):
        if self.evolution_level is not None and self.level>=self.evolution_level and self.evolution_id is not None:
            self.id=self.evolution_id
            new_file=new_data[str(self.evolution_id)]
            self.load_attributes(new_file)
            return True
        return False
    

    def raise_xp_level(self,new_data):
        self.xp+=100
        if self.xp>=100:
           self.level+=1
           self.xp=0
           self.hp=int(self.hp+5)
           self.hp_max=int(self.hp_max+5)
           self.attack=int(self.attack+3)
           self.defense=int(self.defense+3)
           self.evolve(new_data)
    
    def take_damage(self,damage):
       reduction=self.defense * 0.1
       total_damage = max(5, damage - reduction)  
       self.hp -=int(total_damage)
       self.hp = max(0, int(self.hp))

    @staticmethod
    def add_pokemon(name, type, level, hp, hp_max, attack, defense, sprite, evolution_id=None, evolution_level=None):

        with open("data/pokemon.json", "r") as file:
          try:
            all_pokemon=json.load(file)
          except FileNotFoundError:
              all_pokemon={}
          except json.JSONDecodeError:
              print("JSON file not found")
              return False
          
          if all_pokemon:
              max_id=max(int(key) for key in all_pokemon.keys())
              new_id=str(max_id+1)
          else:
              new_id="1"

          new_pokemon= {
              "name":name,
              "type":type if isinstance(type,list) else [type],
              "level":level,
              "hp":hp,
              "hp_max":hp,
              "attack":attack,
              "defense":defense,
              "evolution_id": evolution_id,
              "evolution_level": evolution_level,   
              "sprite":sprite
         }
          
          all_pokemon[new_id]=new_pokemon

          try:
              import shutil
              shutil.copy("data/pokemon.json", "data/pokemon.json.backup")

              with open("data/pokemon.json", "w") as file:
                  json.dump(all_pokemon, file, indent=2)
              
              print(f"file succesfully added {name}, {new_id}")
          
          except Exception as e:
              print("error")
              shutil.copy("data/pokemon.json", "data/pokemon.json.backup")
              return False
        

              

      
    
    
    
    






