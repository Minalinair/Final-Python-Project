import json
import os
from models import Player

file = "savegame.json"

def save(player):
    try:
        data = {
            "name": player.name,
            "char_class": player.char_class,
            "level": player.level,
            "experience": player.experience,
            "gold": player.gold,
            "enemies_defeated": player.enemies_defeated,
            "bosses_defeated": player.bosses_defeated,
            "base_hp": player.base_hp,
            "base_mana": player.base_mana,
            "base_attack": player.base_attack,
            "base_defense": player.base_defense,
            "base_crit_chance": player.base_crit_chance,
            "current_hp": player.current_hp,
            "current_mana": player.current_mana,
            "equipped_weapon": player.equipped_weapon,
            "equipped_armor": player.equipped_armor,
            "inventory": player.inventory,
            "potions": player.potions
        }
        with open(file, "w") as f:
            json.dump(data, f, indent=4)
        print("\n💾 Game saved successfully!")
    except Exception as e:
        print(f"\n❌ Failed to save game data: {e}")

def load():
    if not os.path.exists(file):
        print("\n❌ No save profile discovered on your disk.")
        return None
    try:
        with open(file, "r") as f:
            data = json.load(f)
        
        player = Player(data["name"], data["char_class"])
        player.level = data["level"]
        player.experience = data["experience"]
        player.gold = data["gold"]
        player.enemies_defeated = data["enemies_defeated"]
        player.bosses_defeated = data["bosses_defeated"]
        player.base_hp = data["base_hp"]
        player.base_mana = data["base_mana"]
        player.base_attack = data["base_attack"]
        player.base_defense = data["base_defense"]
        player.base_crit_chance = data["base_crit_chance"]
        player.current_hp = data["current_hp"]
        player.current_mana = data["current_mana"]
        player.equipped_weapon = data["equipped_weapon"]
        player.equipped_armor = data["equipped_armor"]
        player.inventory = data["inventory"]
        player.potions = data["potions"]
        print(f"\n⚔️ Welcome back, Hero {player.name}! Progress loaded successfully.")
        return player
    except Exception as e:
        print(f"\n❌ Error parsing system save records: {e}")
        return None
    # This script manages saving and loading a player's progress so they don't lose it:
# 
# 1. Saving Progress (`save`): Takes the current player's data (like their name, level, 
#    gold, and gear) and packs it into a tidy list. It then writes this data into a text 
#    file called "savegame.json" on your computer so it stays safe even if the game closes.
#
# 2. Loading Progress (`load`): Checks if a save file exists on your computer. If it finds 
#    one, it opens the file, reads the stored data, and rebuilds the player character 
#    exactly as they were left, letting the player pick up right where they left off.