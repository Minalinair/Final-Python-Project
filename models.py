#using random to get random values
import random
from data import class_stats, weapons, armor, multipliers
#creating two classes- Player and Enemy
class Player:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.level = 1
        self.experience = 0
        self.gold = 200
        self.enemies_defeated = 0
        self.bosses_defeated = 0
        #we use init function for self declaration of variables
        base = class_stats[char_class]
        self.base_hp = base["hp"]
        self.base_mana = base["mana"]
        self.base_attack = base["attack"]
        self.base_defense = base["defense"]
        self.base_crit_chance = base["crit_chance"]
        self.crit_damage_mult = 1.5
        
        self.current_hp = self.base_hp
        self.current_mana = self.base_mana
        
        # Pull clean items as direct dictionaries immediately
        self.equipped_weapon = [w for w in weapons if w["rarity"] == "Common" and w["name"].endswith("Sword" if char_class=="Warrior" else "Wand" if char_class=="Mage" else "Bow" if char_class=="Archer" else "Axe")][0]
        self.equipped_armor = [a for a in armor if a["rarity"] == "Common"][0]
        self.inventory = []
        self.potions = {"Small Health Potion": 2, "Small Mana Potion": 1}
#a decorator used to get attribute values in case of 2 or more functions
    @property
    def max_hp(self):
        armor_obj = self.equipped_armor if not isinstance(self.equipped_armor, list) else self.equipped_armor[0]
        return self.base_hp + armor_obj.get("hp_bonus", 0)

    @property
    def max_mana(self):
        armor_obj = self.equipped_armor if not isinstance(self.equipped_armor, list) else self.equipped_armor[0]
        return self.base_mana + armor_obj.get("mana_bonus", 0)

    @property
    def total_attack(self):
        weapon_obj = self.equipped_weapon if not isinstance(self.equipped_weapon, list) else self.equipped_weapon[0]
        w_rarity = weapon_obj["rarity"]
        mult = multipliers[w_rarity]["damage"]
        return int((self.base_attack + weapon_obj["base_dmg"]) * mult)
    
    @property
    def total_defense(self):
        armor_obj = self.equipped_armor if not isinstance(self.equipped_armor, list) else self.equipped_armor[0]
        return self.base_defense + armor_obj.get("def_bonus", 0)
   
    @property
    def total_crit_chance(self):
        weapon_obj = self.equipped_weapon if not isinstance(self.equipped_weapon, list) else self.equipped_weapon[0]
        w_rarity = weapon_obj["rarity"]
        bonus = multipliers[w_rarity]["crit"]
        return self.base_crit_chance + bonus

    def check_level_up(self):
        req_exp = self.level * 100
        if self.experience >= req_exp:
            self.experience -= req_exp
            self.level += 1
            self.base_hp += 20
            self.base_mana += 10
            self.base_attack += 4
            self.base_defense += 3
            self.current_hp = self.max_hp
            self.current_mana = self.max_mana
            print(f"\n✨ LEVEL UP! You have achieved Level {self.level}! Your power surges!")
            return True
        return False

    def show_stats(self):
        weapon_obj = self.equipped_weapon if not isinstance(self.equipped_weapon, list) else self.equipped_weapon[0]
        armor_obj = self.equipped_armor if not isinstance(self.equipped_armor, list) else self.equipped_armor[0]
        print(f"\n=================== {self.name.upper()}'S PROFILE ===================")
        print(f"Class: {self.char_class} | Level: {self.level} | EXP: {self.experience}/{self.level*100}")
        print(f"HP: {self.current_hp}/{self.max_hp} | Mana: {self.current_mana}/{self.max_mana}")
        print(f"Attack: {self.total_attack} | Defense: {self.total_defense} | Crit Chance: {int(self.total_crit_chance*100)}%")
        print(f"Gold: {self.gold} | Enemies Defeated: {self.enemies_defeated} | Bosses: {self.bosses_defeated}")
        print(f"Equipped Weapon: {weapon_obj['name']} ({weapon_obj['rarity']})")
        print(f"Equipped Armor: {armor_obj['name']} ({armor_obj['rarity']})")
        print("==========================================================")

class Enemy:
    def __init__(self, name, region_level, is_boss=False, boss_stats=None):
        self.name = name
        self.is_boss = is_boss
        if is_boss and boss_stats:
            self.hp = boss_stats["hp"]
            self.max_hp = boss_stats["hp"]
            self.attack = boss_stats["attack"]
            self.defense = boss_stats["defense"]
        else:
            self.hp = int(40 + (region_level * 15) * random.uniform(0.9, 1.1))
            self.max_hp = self.hp
            self.attack = int(10 + (region_level * 4))
            self.defense = int(2 + (region_level * 2))

# 1. The Player: Creates a new level 1 hero. It auto-assigns starter gold, potions, and
#    basic weapons based on their class (like a warrior getting a sword). It uses auto-
#    updating formulas to calculate total attack and defense by adding the player's 
#    base stats to their gear bonuses. It also handles leveling up when enough EXP 
#    is earned and prints out the character's profile card.
#
# 2. The Enemy: Spawns the bad guys. Regular monsters automatically scale up in strength 
#    and health depending on how dangerous the region level is. Major bosses skip this 
#    scaling math and use fixed, super-powerful stats instead.