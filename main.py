# sys is a direct bridge between Python script and the operating system
import sys
import random
# importing all the functions and list, dictionaries we created at other files
from models import Player, Enemy
from system_save import save, load
from combat import run_battle
from data import enemies, boss, weapons, armor,potion,loot_weights
def main_menu():
    while True:
        print("\n=========================================")
        print("     LEGENDS OF THE FORGOTTEN REALM      ")
        print("=========================================")
        print("1. New Game\n2. Continue Game\n3. Instructions\n4. Exit")
        choice = input("Enter choice (1-4): ").strip()
        #creating an initial welcome face and choices begin
        if choice == "1":
            name = input("\nEnter player hero name: ").strip()
            if not name: name = "Hero"
            print("\nChoose Your Class:")
            print("1. Warrior\n2. Mage\n3. Archer\n4. Assassin")
            c_input = input("Select class (1-4): ").strip()
            classes = {"1": "Warrior", "2": "Mage", "3": "Archer", "4": "Assassin"}
            chosen_class = classes.get(c_input, "Warrior")
            
            player = Player(name, chosen_class)
            game_loop(player)
        elif choice == "2":
            player = load()
            if player: game_loop(player)
        elif choice == "3":
            print("\n📜 INSTRUCTIONS:\nDefeat enemies to gain EXP and level up. Every 10 levels, you face a regional boss.")
            print("Keep your gear upgraded at the Village Shop using Gold earned from battles. Defeat Level 100 to win!")
        elif choice == "4":
            print("\nFarewell traveler!")
            sys.exit()
        else:
            print("❌ Invalid menu option choice.")
#after choosing a class what the user wants to do
def game_loop(player):
    while player.current_hp > 0:
        region_idx = min((player.level - 1) // 10, len(enemies) - 1)
        region = enemies[region_idx]
        
        print(f"\n📍 CURRENT LOCATION: {region['name']} (Recommended Level: {region['min_lv']}-{region['max_lv']})")
        print("1. Explore (Find Enemy)\n2. Challenge Boss\n3. Visit Village Shop\n4. Manage Inventory\n5. Save Progress\n6. Return to Main Menu")
        choice = input("What would you like to do? ").strip()
        
        if choice == "1":
            e_name = random.choice(region["enemies"])
            enemy = Enemy(e_name, player.level)
            result = run_battle(player, enemy)
            
            if result == "won":
                exp_gain = player.level * 25
                gold_gain = random.randint(15, 40) * player.level
                player.experience += exp_gain
                player.gold += gold_gain
                player.enemies_defeated += 1
                print(f"💰 Found {gold_gain} Gold and gained {exp_gain} EXP.")
                
                if random.random() < 0.30:
                    rarities = list(loot_weights.keys())
                    weights = list(loot_weights.values())
                    
                    rolled_rarity = random.choices(rarities, weights=weights, k=1)[0]
                    
                    item_type = random.choice(["weapon", "armor"])
                    
                    if item_type == "weapon":
                        matching_pool = [w for w in weapons if w["rarity"] == rolled_rarity]
                        if not matching_pool: 
                            matching_pool = [w for w in weapons if w["rarity"] == "Common"]
                    else:
                        matching_pool = [a for a in armor if a["rarity"] == rolled_rarity]
                        if not matching_pool: 
                            matching_pool = [a for a in armor if a["rarity"] == "Common"]
                    
                    dropped_item = random.choice(matching_pool)
                    player.inventory.append(dropped_item)
                    
                    print(f"🎁 LOOT DROP! The enemy dropped a [{rolled_rarity}] item!")
                    print(f"   👉 {dropped_item['name']} added to your inventory pouch.")
                player.check_level_up()
                
            elif result == "lost":
                handle_game_over(player)
                break
                
        elif choice == "2":
            next_boss_lv = ((player.bosses_defeated + 1) * 10)
            if player.level < next_boss_lv:
                print(f"\n🔒 You need to reach at least Level {next_boss_lv} to track down the next boss!")
                continue
                
            b_data = boss.get(next_boss_lv)
            if not b_data:
                print("\n🎉 You have eradicated all evil from the realm! You win!")
                break
                
            boss_enemy = Enemy(b_data["name"], next_boss_lv, is_boss=True, boss_stats=b_data)
            result = run_battle(player, boss_enemy)
            
            if result == "won":
                player.bosses_defeated += 1
                player.gold += next_boss_lv * 100
                print(f"🏆 Milestone Defeated! You broke the seal of the level {next_boss_lv} region!")
                boss_rarities = ["Rare", "Super Rare", "Epic", "Mythical", "Legendary"]
                
                boss_weights = [0.50, 0.30, 0.14, 0.05, 0.01] 
                
                rolled_rarity = random.choices(boss_rarities, weights=boss_weights, k=1)[0]
                item_type = random.choice(["weapon", "armor"])
                
                if item_type == "weapon":
                    matching_pool = [w for w in weapons if w["rarity"] == rolled_rarity]
                else:
                    matching_pool = [a for a in armor if a["rarity"] == rolled_rarity]
                
                
                if not matching_pool:
                    matching_pool = weapons if item_type == "weapon" else armor
                    
                dropped_item = random.choice(matching_pool)
                player.inventory.append(dropped_item)
                
                print(f"💎 BOSS BOUNTY! You secured a guaranteed rare treasure: {dropped_item['name']} ({rolled_rarity})!")
                if next_boss_lv == 100:
                    print("\n👑 The Ancient Demon King is dead! Eldoria is saved! Victory is yours!")
                    break
            elif result == "lost":
                handle_game_over(player)
                break
                
        elif choice == "3":
            open_shop(player)
        elif choice == "4":
            manage_inventory(player)
        elif choice == "5":
            save(player)
        elif choice == "6":
            break
#shop where the user can buy potions , weapons or anything special
def open_shop(player):
    while True:
        print(f"\n🏪 VILLAGE MERCHANT (Your Gold: {player.gold})")
        print("1. Buy Small Health Potion (15 Gold)\n2. Buy Small Mana Potion (15 Gold)\n3. Browse Rare Armors\n4. Exit Shop")
        choice = input("Select an item to purchase: ").strip()
        if choice == "1" and player.gold >= 15:
            player.gold -= 15
            player.potions["Small Health Potion"] = player.potions.get("Small Health Potion", 0) + 1
            print("🛍️ Purchased 1 Small Health Potion.")
        elif choice == "2" and player.gold >= 15:
            player.gold -= 15
            player.potions["Small Mana Potion"] = player.potions.get("Small Mana Potion", 0) + 1
            print("🛍️ Purchased 1 Small Mana Potion.")
        elif choice == "3":
            rare_armor = [a for a in armor if a["rarity"] == "Rare"][0]
            print(f"🛡️ Featured Armor: {rare_armor['name']} | Cost: {rare_armor['price']} Gold")
            confirm = input("Purchase item? (y/n): ").lower()
            if confirm == 'y' and player.gold >= rare_armor["price"]:
                player.gold -= rare_armor["price"]
                player.inventory.append(rare_armor)
                print(f"🛍️ Purchased {rare_armor['name']}!")
            elif confirm == 'y':
                print("❌ You lack the necessary funds.")
        elif choice == "4":
            break
#to check what the user has in the inventory
def manage_inventory(player):
    while True:
        print("\n🎒 INVENTORY ITEMS:")
        if not player.inventory:
            print("[Empty]")
            break
        for idx, item in enumerate(player.inventory, 1):
            details = f"DMG: {item.get('base_dmg')}" if 'base_dmg' in item else f"DEF: {item.get('def_bonus')}"
            print(f"{idx}. {item['name']} ({item['rarity']} | {details})")
        print(f"{len(player.inventory)+1}. Back")
        
        try:
            choice = int(input("Select an item to equip/use: ")) - 1
            if choice == len(player.inventory): break
            selected = player.inventory[choice]
            
            if 'base_dmg' in selected:
                player.inventory.append(player.equipped_weapon)
                player.equipped_weapon = selected
                player.inventory.remove(selected)
                print(f"⚔️ Equipped {selected['name']} successfully.")
            elif 'def_bonus' in selected:
                player.inventory.append(player.equipped_armor)
                player.equipped_armor = selected
                player.inventory.remove(selected)
                print(f"🛡️ Equipped {selected['name']} successfully.")
        except (ValueError, IndexError):
            print("❌ Invalid inventory pointer.")
#when the user exits the game 
def handle_game_over(player):
    print("\n==================\n    GAME OVER     \n==================")
    print("Your journey ends here... For now.")
    print("1. Reload Save\n2. Exit to Desktop")
    c = input("Choose option: ").strip()
    if c == "1":
        loaded = load()
        if loaded: game_loop(loaded)
    else:
        sys.exit()

if __name__ == "__main__":
    main_menu()
#This is where everything is coordinated and the blueprint of the game is laid out- we begin with a welcome and move on to the choices and game play. Each and every python file created is connected over here and this is the main backbone of the project where the main function is called out to begin the game.