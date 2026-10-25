#creating a dictionary for thhe four classes
class_stats = {
    "Warrior":  {"hp": 150, "mana": 40,  "attack": 25, "defense": 18, "crit_chance": 0.05},
    "Mage":     {"hp": 100, "mana": 120, "attack": 35, "defense": 8,  "crit_chance": 0.10},
    "Archer":    {"hp": 120, "mana": 70,  "attack": 22, "defense": 12, "crit_chance": 0.18},
    "Assassin":  {"hp": 90,  "mana": 60,  "attack": 30, "defense": 6,  "crit_chance": 0.30}
}
#adding skills for each class
class_skills = {
    "Warrior": [
        {"name": "Slash", "cost": 10, "power": 1.4, "level": 1},
        {"name": "Shield Bash", "cost": 15, "power": 1.2, "level": 5},
        {"name": "Rage", "cost": 25, "power": 2.0, "level": 10},
        {"name": "Earthquake", "cost": 40, "power": 3.0, "level": 15}
    ],
    "Mage": [
        {"name": "Fireball", "cost": 15, "power": 1.6, "level": 1},
        {"name": "Ice Blast", "cost": 20, "power": 1.5, "level": 5},
        {"name": "Thunder Strike", "cost": 30, "power": 2.2, "level": 10},
        {"name": "Meteor", "cost": 50, "power": 3.5, "level": 15}
    ],
    "Archer": [
        {"name": "Multi Shot", "cost": 12, "power": 1.3, "level": 1},
        {"name": "Poison Arrow", "cost": 18, "power": 1.5, "level": 5},
        {"name": "Explosive Arrow", "cost": 28, "power": 2.1, "level": 10},
        {"name": "Sniper Shot", "cost": 45, "power": 3.2, "level": 15}
    ],
    "Assassin": [
        {"name": "Backstab", "cost": 12, "power": 1.8, "level": 1},
        {"name": "Smoke Bomb", "cost": 20, "power": 1.2, "level": 5},
        {"name": "Shadow Strike", "cost": 25, "power": 2.2, "level": 10},
        {"name": "Instant Kill", "cost": 60, "power": 6.0, "level": 15}
    ]
}
#creating dictionary for damage multiplier
multipliers = { 
    "Common":     {"damage": 1.0, "crit": 0.00},
    "Uncommon":   {"damage": 1.1, "crit": 0.02},
    "Rare":       {"damage": 1.3, "crit": 0.05},
    "Super Rare": {"damage": 1.5, "crit": 0.08},
    "Epic":       {"damage": 1.8, "crit": 0.12},
    "Mythical":   {"damage": 2.2, "crit": 0.18},
    "Legendary":  {"damage": 2.8, "crit": 0.25}
}
#list of weapons that can be used by the user
weapons = [
    {"name": "Wooden Sword", "rarity": "Common", "base_dmg": 10, "level": 1, "price": 50},
    {"name": "Rusty Axe", "rarity": "Common", "base_dmg": 12, "level": 1, "price": 60},
    {"name": "Training Bow", "rarity": "Common", "base_dmg": 9, "level": 1, "price": 45},
    {"name": "Novice Wand", "rarity": "Common", "base_dmg": 11, "level": 1, "price": 55},
    {"name": "Iron Sword", "rarity": "Rare", "base_dmg": 22, "level": 10, "price": 300},
    {"name": "Steel Axe", "rarity": "Rare", "base_dmg": 26, "level": 12, "price": 350},
    {"name": "Long Bow", "rarity": "Rare", "base_dmg": 20, "level": 10, "price": 280},
    {"name": "Apprentice Staff", "rarity": "Rare", "base_dmg": 24, "level": 11, "price": 320},
    {"name": "Crystal Blade", "rarity": "Super Rare", "base_dmg": 45, "level": 25, "price": 1200},
    {"name": "Shadow Dagger", "rarity": "Super Rare", "base_dmg": 40, "level": 25, "price": 1150},
    {"name": "Lightning Bow", "rarity": "Super Rare", "base_dmg": 42, "level": 27, "price": 1300},
    {"name": "Flame Sword", "rarity": "Epic", "base_dmg": 75, "level": 45, "price": 4000},
    {"name": "Ice Spear", "rarity": "Epic", "base_dmg": 72, "level": 45, "price": 3800},
    {"name": "Thunder Hammer", "rarity": "Epic", "base_dmg": 85, "level": 50, "price": 5000},
    {"name": "Phoenix Blade", "rarity": "Mythical", "base_dmg": 130, "level": 70, "price": 15000},
    {"name": "Demon Slayer", "rarity": "Mythical", "base_dmg": 140, "level": 75, "price": 18000},
    {"name": "Celestial Staff", "rarity": "Mythical", "base_dmg": 125, "level": 70, "price": 14500},
    {"name": "Dragon King's Sword", "rarity": "Legendary", "base_dmg": 250, "level": 90, "price": 50000},
    {"name": "Blade of Eternity", "rarity": "Legendary", "base_dmg": 270, "level": 95, "price": 60000},
    {"name": "Bow of the Gods", "rarity": "Legendary", "base_dmg": 240, "level": 90, "price": 55000}
]
#list of armors
armor = [
    {"name": "Cloth Vest", "rarity": "Common", "def_bonus": 2, "hp_bonus": 10, "mana_bonus": 0, "crit_res": 0.00, "price": 40},
    {"name": "Leather Jerkin", "rarity": "Common", "def_bonus": 4, "hp_bonus": 20, "mana_bonus": 5, "crit_res": 0.01, "price": 80},
    {"name": "Initiate Robe", "rarity": "Common", "def_bonus": 2, "hp_bonus": 10, "mana_bonus": 20, "crit_res": 0.00, "price": 75},
    {"name": "Iron Mail", "rarity": "Rare", "def_bonus": 12, "hp_bonus": 50, "mana_bonus": 0, "crit_res": 0.03, "price": 400},
    {"name": "Ranger Cloak", "rarity": "Rare", "def_bonus": 8, "hp_bonus": 40, "mana_bonus": 15, "crit_res": 0.04, "price": 380},
    {"name": "Heavy Plate", "rarity": "Super Rare", "def_bonus": 25, "hp_bonus": 100, "mana_bonus": 0, "crit_res": 0.06, "price": 1500},
    {"name": "Sorcerer Vestments", "rarity": "Super Rare", "def_bonus": 14, "hp_bonus": 60, "mana_bonus": 60, "crit_res": 0.05, "price": 1600},
    {"name": "Guardian Carapace", "rarity": "Epic", "def_bonus": 45, "hp_bonus": 200, "mana_bonus": 20, "crit_res": 0.10, "price": 6000},
    {"name": "Vanguard Hauberk", "rarity": "Epic", "def_bonus": 50, "hp_bonus": 250, "mana_bonus": 0, "crit_res": 0.08, "price": 6500},
    {"name": "Dreadnought Armor", "rarity": "Mythical", "def_bonus": 90, "hp_bonus": 500, "mana_bonus": 50, "crit_res": 0.15, "price": 22000},
    {"name": "Eclipse Shroud", "rarity": "Mythical", "def_bonus": 75, "hp_bonus": 400, "mana_bonus": 120, "crit_res": 0.18, "price": 20000},
    {"name": "Eldorian Royal Plate", "rarity": "Legendary", "def_bonus": 160, "hp_bonus": 1000, "mana_bonus": 200, "crit_res": 0.25, "price": 75000}
]
#dictionary of potions used in the game
potion = {
    "Health": [
        {"name": "Small Health Potion", "value": 50, "price": 15},
        {"name": "Medium Health Potion", "value": 100, "price": 30},
        {"name": "Large Health Potion", "value": 250, "price": 65},
        {"name": "Giant Health Potion", "value": 500, "price": 120},
        {"name": "Ultimate Health Potion", "value": 99999, "price": 300}
    ],
    "Mana": [
        {"name": "Small Mana Potion", "value": 30, "price": 15},
        {"name": "Medium Mana Potion", "value": 75, "price": 30},
        {"name": "Large Mana Potion", "value": 150, "price": 65},
        {"name": "Giant Mana Potion", "value": 300, "price": 120},
        {"name": "Ultimate Mana Potion", "value": 99999, "price": 300}
    ],
    "Mixed": [
        {"name": "Rejuvenation Elixir", "hp_val": 100, "mana_val": 50, "price": 60},
        {"name": "Grand Elixir", "hp_val": 300, "mana_val": 150, "price": 150},
        {"name": "Miracle Ambrosia", "hp_val": 99999, "mana_val": 99999, "price": 500}
    ],
    "Buff": [
        {"name": "Attack Serum", "stat": "attack", "boost": 15, "duration": 3, "price": 50},
        {"name": "Defense Serum", "stat": "defense", "boost": 10, "duration": 3, "price": 50},
        {"name": "Focus Serum", "stat": "crit_chance", "boost": 0.15, "duration": 3, "price": 60}
    ]
}
#list of enemies in each levels
enemies = [
    {"name": "Village Borders", "min_lv": 1, "max_lv": 10, "enemies": ["Goblin", "Wolf", "Slime", "Zombie", "Skeleton"]},
    {"name": "Whispering Forest", "min_lv": 11, "max_lv": 20, "enemies": ["Orc", "Bandit", "Troll", "Dark Archer", "Giant Spider"]},
    {"name": "Echoing Caves", "min_lv": 21, "max_lv": 30, "enemies": ["Vampire", "Werewolf", "Necromancer", "Ice Golem", "Fire Demon"]},
    {"name": "Scorched Desert", "min_lv": 31, "max_lv": 40, "enemies": ["Sand Scorpion", "Mummy", "Desert Raider", "Basilisk", "Dunewalker"]},
    {"name": "Forgotten Ruins", "min_lv": 41, "max_lv": 50, "enemies": ["Gargoyle", "Cursed Armor", "Wraith", "Lich", "Shadow Stalker"]},
    {"name": "Desolate Castle", "min_lv": 51, "max_lv": 60, "enemies": ["Royal Guard Spectre", "Executioner", "Hellhound", "Banshee", "Blood Knight"]},
    {"name": "Obsidian Volcano", "min_lv": 61, "max_lv": 70, "enemies": ["Magma Slime", "Fire Giant", "Salamander", "Efreet", "Lavabeast"]},
    {"name": "Frozen Mountain", "min_lv": 71, "max_lv": 80, "enemies": ["Frost Wampa", "Ice Elemental", "Snow Leopard", "Winter Witch", "Yeti"]},
    {"name": "Sky Temple", "min_lv": 81, "max_lv": 90, "enemies": ["Storm Griffin", "Archangel Outcast", "Thunder Djinn", "Valkyrie", "Cloud Titan"]},
    {"name": "Demon Realm", "min_lv": 91, "max_lv": 100, "enemies": ["Pit Fiend", "Succubus", "Tormentor", "Chaos Spawn", "Doomguard"]}
]
#dictionary of boss appearing at each level
boss = {
    10: {"name": "Goblin King", "hp": 400, "attack": 30, "defense": 15},
    20: {"name": "Forest Guardian", "hp": 900, "attack": 55, "defense": 30},
    30: {"name": "Ancient Golem", "hp": 1800, "attack": 85, "defense": 60},
    40: {"name": "Vampire Lord", "hp": 3000, "attack": 130, "defense": 80},
    50: {"name": "Dragon Rider", "hp": 5000, "attack": 190, "defense": 110},
    60: {"name": "Demon General", "hp": 8000, "attack": 270, "defense": 150},
    70: {"name": "Ice Titan", "hp": 12000, "attack": 380, "defense": 200},
    80: {"name": "Shadow Emperor", "hp": 18000, "attack": 520, "defense": 260},
    90: {"name": "Celestial Dragon", "hp": 26000, "attack": 700, "defense": 330},
    100: {"name": "Ancient Demon King", "hp": 40000, "attack": 1000, "defense": 450}
}
#dictionary consisting weight of each loot based on rarity
loot_weights = {
    "Common": 0.50,
    "Uncommon": 0.25,
    "Rare": 0.15,
    "Super Rare": 0.06,
    "Epic": 0.03,
    "Mythical": 0.009,
    "Legendary": 0.001
}
