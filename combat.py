import random
from data import class_skills

def run_battle(player, enemy):
    print(f"\n⚔️ A wild {enemy.name} blocks your path! (HP: {enemy.max_hp}, ATK: {enemy.attack}, DEF: {enemy.defense})")
    
    player_defending = False
    turn_counter = 0
    
    while player.current_hp > 0 and enemy.hp > 0:
        turn_counter += 1
        player_defending = False 
        
        print(f"\n--- {enemy.name} HP: {max(0, enemy.hp)}/{enemy.max_hp} | YOUR HP: {player.current_hp}/{player.max_hp} [Mana: {player.current_mana}/{player.max_mana}] ---")
        print("====================\nYOUR TURN\n====================")
        print("1. Attack\n2. Skills\n3. Use Potion\n4. Defend\n5. View Stats\n6. Run")
        
        choice = input("Select an action (1-6): ").strip()
        
        if choice == "1":
            base_dmg = player.total_attack - enemy.defense
            damage = max(1, base_dmg)
            
            if random.random() < player.total_crit_chance:
                damage = int(damage * player.crit_damage_mult)
                print(f"💥 CRITICAL HIT! You slashed through defense lines for {damage} damage!")
            else:
                print(f"⚔️ You strike the {enemy.name} dealing {damage} damage.")
            enemy.hp -= damage
            
        elif choice == "2":
            skills = [s for s in class_skills[player.char_class] if s["level"] <= player.level]
            print("\n--- AVAILABLE SKILLS ---")
            for idx, sk in enumerate(skills, 1):
                print(f"{idx}. {sk['name']} (Cost: {sk['cost']} MP, Power: x{sk['power']})")
            print(f"{len(skills)+1}. Back")
            
            try:
                sk_choice = int(input("Choose a skill: ")) - 1
                if sk_choice == len(skills): continue
                selected_skill = skills[sk_choice]
                
                if player.current_mana >= selected_skill["cost"]:
                    player.current_mana -= selected_skill["cost"]
                    sk_dmg = max(1, int((player.total_attack * selected_skill["power"]) - enemy.defense))
                    print(f"✨ You channel {selected_skill['name']}! Dealt {sk_dmg} raw spell damage.")
                    enemy.hp -= sk_dmg
                else:
                    print("❌ Insufficient mana resources!")
                    continue
            except (ValueError, IndexError):
                print("❌ Invalid skill index selection.")
                continue
                
        elif choice == "3":
            if not player.potions:
                print("❌ No potions in storage pouch.")
                continue
            print("\n--- POTION INVENTORY ---")
            p_list = list(player.potions.items())
            for idx, (p_name, qty) in enumerate(p_list, 1):
                print(f"{idx}. {p_name} x{qty}")
            print(f"{len(p_list)+1}. Back")
            
            try:
                p_choice = int(input("Select Potion: ")) - 1
                if p_choice == len(p_list): continue
                chosen_p, qty = p_list[p_choice]
                
                if qty > 0:
                    player.potions[chosen_p] -= 1
                    # Support both standard layout named items and special custom hybrid elixirs safely
                    if "Health" in chosen_p or "Elixir" in chosen_p or "Ambrosia" in chosen_p:
                        player.current_hp = min(player.max_hp, player.current_hp + 100)
                        print(f"❤️ Drank {chosen_p}. HP recovered to {player.current_hp}.")
                    elif "Mana" in chosen_p:
                        player.current_mana = min(player.max_mana, player.current_mana + 50)
                        print(f"🧪 Drank {chosen_p}. Mana recovered to {player.current_mana}.")
                    if player.potions[chosen_p] == 0:
                        del player.potions[chosen_p]
                else:
                    print("❌ Out of stock.")
                    continue
            except (ValueError, IndexError):
                print("❌ Invalid choice.")
                continue
                
        elif choice == "4":
            player_defending = True
            print("🛡️ You assume a high defensive stance. Next incoming strike damage halved.")
            
        elif choice == "5":
            player.show_stats()
            continue
            
        elif choice == "6":
            if enemy.is_boss:
                print("❌ You cannot flee from a Boss Encounter!")
                continue
            if random.random() < 0.4:
                print("💨 Escaped the combat encounter successfully.")
                return "fled"
            else:
                print("❌ Escape path blocked! You must stand and fight!")
                
        else:
            print("❌ Unknown combat directive command.")
            continue
            
        if enemy.hp > 0:
            print(f"\n👹 {enemy.name}'s turn...")
            e_dmg = enemy.attack - player.total_defense
            e_dmg = max(1, e_dmg)
            
            if player_defending:
                e_dmg = max(1, int(e_dmg * 0.5))
                print("🛡️ Your defensive stance blocked half the damage!")
                
            print(f"💥 {enemy.name} attacks you for {e_dmg} damage.")
            player.current_hp -= e_dmg
            
    if player.current_hp <= 0:
        print("\n💀 You were defeated in battle...")
        return "lost"
    
    print(f"\n🎉 Victory! You have slain {enemy.name}!")
    return "won"
# This script powers the battle engine using an automated turn-by-turn system:
# 
# 1. Battle Loop: Keeps the fight going in a continuous loop until either the player's 
#    or the enemy's health points hit zero, deciding a winner or allowing an escape.
#
# 2. Combat Actions: Calculates physical strikes (with a random dice roll for high-damage
#    critical hits), filters out locked magical skills based on the player's level, and 
#    halves incoming monster damage when the player takes a protective defensive stance.
#
# 3. Item & Escape Rules: Manages inventory by safely tracking potion quantities (cleaning
#    up empty bottles automatically), applies smart text-matching to identify custom healing 
#    items, and uses a random 40% success rate to determine if a player can successfully flee.