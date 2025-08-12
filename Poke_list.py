# --- Data storage ---
import math


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
        "Damage Type": "Physical",
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

# --- Team setup ---
# Each team has one Pokémon, with a separate current HP
player_team = [
    {
        **pokemon_data["Bulbasaur"],  # Copy base stats
        "Current HP": pokemon_data["Bulbasaur"]["HP"],
        "Moves": [move_data["Tackle"]]
    }
]

opponent_team = [
    {
        **pokemon_data["Bulbasaur"],
        "Current HP": pokemon_data["Bulbasaur"]["HP"],
        "Moves": [move_data["Tackle"]]
    }
]

# Quick check:
print(player_team)
print(opponent_team)
