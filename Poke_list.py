import math
import random

# --- PASSIVE DATA STORAGE ---
pokemon_data = {
    "Bulbasaur": {
        "Name": "Bulbasaur",
        "Type": ["Grass", "Poison"],
        "HP": 45,
        "Attack": 49,
        "Defense": 49,
        "Sp. Attack": 65,
        "Sp. Defense": 65,
        "Speed": 45,
        "BST": 318,           # Base Stat Total
        "Ability": "Overgrow" # Placeholder, not implemented yet
    }
}

move_data = {
    "Tackle": {
        "Name": "Tackle",
        "Damage Type": "Physical",
        "Power": 40,
        "PP": 35
    }
}

# --- CALCULATION FUNCTIONS ---
def calc_hp(base_hp, level, iv=0, ev=0):
    return math.floor((((2 * base_hp + iv + (ev // 4)) * level) / 100) + level + 10)

def calc_stat(base_stat, level, iv=0, ev=0, nature_modifier=1.0):
    return math.floor(((((2 * base_stat + iv + (ev // 4)) * level) / 100) + 5) * nature_modifier)

def calc_damage(level, power, attacker_stat, defender_stat):
    part1 = ((2 * level) / 5) + 2
    base = (part1 * power * (attacker_stat / defender_stat)) / 50
    damage = base + 2
    return max(1, math.floor(damage))

def speed_tie():
    """Returns True if Player wins tie, False if Opponent wins"""
    return random.choice([True, False])

# --- TEAM GENERATION ---
def make_pokemon_instance(species_name, level, iv=0, ev=0, nature_modifier=1.0, moveset=None):
    base = pokemon_data[species_name]
    
    # Passive (from data storage)
    passive = {
        "Name": base["Name"],
        "Type": base["Type"],
        "Base Stats": {
            "HP": base["HP"],
            "Attack": base["Attack"],
            "Defense": base["Defense"],
            "Sp. Attack": base["Sp. Attack"],
            "Sp. Defense": base["Sp. Defense"],
            "Speed": base["Speed"]
        },
        "BST": base["BST"],
        "Ability": base["Ability"]
    }
    
    # Team (fixed for match)
    team = {
        "Level": level,
        "IVs": iv,
        "EVs": ev,
        "Nature Modifier": nature_modifier,
        "Held Item": None, # To implement later
        "Moveset": moveset if moveset else []
    }
    
    # Effective stats at match start
    effective_stats = {
        "Max HP": calc_hp(base["HP"], level, iv, ev),
        "Attack": calc_stat(base["Attack"], level, iv, ev, nature_modifier),
        "Defense": calc_stat(base["Defense"], level, iv, ev, nature_modifier),
        "Sp. Attack": calc_stat(base["Sp. Attack"], level, iv, ev, nature_modifier),
        "Sp. Defense": calc_stat(base["Sp. Defense"], level, iv, ev, nature_modifier),
        "Speed": calc_stat(base["Speed"], level, iv, ev, nature_modifier)
    }
    team.update(effective_stats)
    
    # Active (changes during battle)
    active = {
        "Current HP": effective_stats["Max HP"],
        "Stat Boosts": {  # Stages: -6 to +6, all start at 0
            "Attack": 0,
            "Defense": 0,
            "Sp. Attack": 0,
            "Sp. Defense": 0,
            "Speed": 0
        },
        "Status": None
    }
    
    return {
        "Passive": passive,
        "Team": team,
        "Active": active
    }

# --- Example Teams ---
player_team = [
    make_pokemon_instance(
        "Bulbasaur", 
        level=5, 
        moveset=[move_data["Tackle"]]
    )
]

opponent_team = [
    make_pokemon_instance(
        "Bulbasaur", 
        level=5, 
        moveset=[move_data["Tackle"]]
    )
]

# --- Speed Tie Example (not linked to prompts yet) ---
if player_team[0]["Team"]["Speed"] == opponent_team[0]["Team"]["Speed"]:
    tie_winner_is_player = speed_tie()
    # This variable will later control who acts first

# --- MENU FUNCTIONS ---
def display_team(team, player_label):
    print(f"{player_label}:")
    for idx, mon in enumerate(team, start=1):
        print(f"Pokemon {idx}: {mon['Passive']['Name']}")
        print(f"Level: {mon['Team']['Level']}")
        print(f"Ability: {mon['Passive']['Ability']}")
        held_item = mon['Team']['Held Item'] if mon['Team']['Held Item'] else "None"
        print(f"Held Item: {held_item}")
        print("\nMoveset:")
        for i in range(4):
            if i < len(mon['Team']['Moveset']):
                move_name = mon['Team']['Moveset'][i]['Name']
                print(f"- {move_name}")
            else:
                print("- Empty")
        print()  # Blank line between Pokémon

def check_team():
    print("\n=== Team Overview ===\n")
    display_team(player_team, "Player 1")
    display_team(opponent_team, "Player 2")
    input("Press Enter to return to main menu...")

def main_menu():
    while True:
        print("\n=== Main Menu ===")
        print("1. Start Battle!")
        print("2. Check Team")
        print("3. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            # Placeholder for battle logic
            print("\n[Battle start placeholder]\n")
        elif choice == "2":
            check_team()
        elif choice == "3":
            print("Exiting game. Goodbye!")
            break
        else:
            print("Invalid choice, please enter 1, 2, or 3.")

# --- Start the program ---
if __name__ == "__main__":
    main_menu()