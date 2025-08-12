import math

# --- Data storage ---
pokemon_data = {
    "Bulbasaur": {
        "Name": "Bulbasaur",
        "HP": 45,
        "Attack": 49,
        "Defense": 49,
        "Sp. Attack": 65,
        "Sp. Defense": 65,
        "Speed": 45
    }
}

move_data = {
    "Tackle": {
        "Name": "Tackle",
        "Damage Type": "Physical",  # "Physical" or "Special"
        "Power": 40,
        "PP": 35
    }
}

# --- Stat / damage functions ---
def calc_hp(base_hp, level, iv=0, ev=0):
    """Calculate max HP"""
    hp = (((2 * base_hp + iv + (ev // 4)) * level) / 100) + level + 10
    return math.floor(hp)

def calc_stat(base_stat, level, iv=0, ev=0, nature_modifier=1.0):
    """Calculate non-HP stat (Attack, Defense, Sp. Atk, Sp. Def, Speed)"""
    stat = ((((2 * base_stat + iv + (ev // 4)) * level) / 100) + 5) * nature_modifier
    return math.floor(stat)

def calc_damage(level, power, attacker_stat, defender_stat):
    """Simplified damage formula (no STAB, no type, no random, no crit)"""
    part1 = ((2 * level) / 5) + 2
    base = (part1 * power * (attacker_stat / defender_stat)) / 50
    damage = base + 2
    return max(1, math.floor(damage))  # At least 1 damage

# --- Team setup with Level added ---
# Choose a level for both sides (example: 5)
PLAYER_LEVEL = 5
OPPONENT_LEVEL = 5

def make_pokemon_instance(species_name, level):
    base = pokemon_data[species_name]
    instance = {
        "Species": species_name,
        "Name": base["Name"],
        "Level": level,
        "Base HP": base["HP"],
        "Base Attack": base["Attack"],
        "Base Defense": base["Defense"],
        "Base Sp. Attack": base["Sp. Attack"],
        "Base Sp. Defense": base["Sp. Defense"],
        "Base Speed": base["Speed"],
        # computed stats:
        "Max HP": calc_hp(base["HP"], level),
        "Attack": calc_stat(base["Attack"], level),
        "Defense": calc_stat(base["Defense"], level),
        "Sp. Attack": calc_stat(base["Sp. Attack"], level),
        "Sp. Defense": calc_stat(base["Sp. Defense"], level),
        "Speed": calc_stat(base["Speed"], level),
        "Current HP": None,  # we'll set below
        "Moves": [move_data["Tackle"]]
    }
    instance["Current HP"] = instance["Max HP"]
    return instance

player_team = [ make_pokemon_instance("Bulbasaur", PLAYER_LEVEL) ]
opponent_team = [ make_pokemon_instance("Bulbasaur", OPPONENT_LEVEL) ]

# --- Demonstration: compute damage from player's Bulbasaur using Tackle on opponent ---
attacker = player_team[0]
defender = opponent_team[0]
move = attacker["Moves"][0]

# Decide which stats to use based on damage type
if move["Damage Type"] == "Physical":
    atk_stat = attacker["Attack"]
    def_stat = defender["Defense"]
else:
    atk_stat = attacker["Sp. Attack"]
    def_stat = defender["Sp. Defense"]

damage = calc_damage(attacker["Level"], move["Power"], atk_stat, def_stat)

print(f"{attacker['Name']} (Lv{attacker['Level']}) uses {move['Name']}!")
print(f"Attack stat: {atk_stat}, Defense stat: {def_stat}")
print(f"Calculated damage: {damage}")
print(f"Defender HP before: {defender['Current HP']}")
defender["Current HP"] -= damage
if defender["Current HP"] < 0:
    defender["Current HP"] = 0
print(f"Defender HP after: {defender['Current HP']} (Max: {defender['Max HP']})")

