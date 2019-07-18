

ConditionCauses = {
    "Sun": { "move": "Sunny Day", "ability": "Drought" },
    "Rain": { "move": "Rain Dance", "ability": "Drizzle" },
    "Sandstorm": { "move": "Sandstorm", "ability": "Sand Stream" },
    "Hail": { "move": "Hail", "ability": "Snow Warning" },

    "Strong Winds": { "move": None, "ability": "Delta Stream" },
    "Intense Sun": { "move": None, "ability": "Desolate Land" },
    "Heavy Rain": { "move": None, "ability": "Primordial Sea" },

    "Electric Terrain": { "move": "Electric Terrain", "ability": "Electric Surge" },
    "Misty Terrain": { "move": "Misty Terrain", "ability": "Misty Surge" },
    "Grassy Terrain": { "move": "Grassy Terrain", "ability": "Grassy Surge" },
    "Psychic Terrain": { "move": "Psychic Terrain", "ability": "Psychic Surge" },

    "Light Screen": { "move": "Light Screen", "ability": None },
    "Reflect": { "move": "Reflect", "ability": None },
    "Aurora Veil": { "move": "Aurora Veil", "ability": None },

    "Trick Room": { "move": "Trick Room", "ability": None },
    "Wonder Room": { "move": "Wonder Room", "ability": None },
    "Magic room": { "move": "Magic Room", "ability": None },
    "Gravity": { "move": "Gravity", "ability": None },

    "Water Sport": { "move": "Water Sport", "ability": None },
    "Mud Sport": { "move": "Mud Sport", "ability": None },

    "Tailwind": { "move": "Tailwind", "ability": None },
    "Lucky Chant": { "move": "Lucky Chant", "ability": None },
    "Safeguard": { "move": "Safeguard", "ability": None },
    "Mist": { "move": "Mist", "ability": None }
}

StatusList = ['BRN', 'TOX', 'PAR', 'PSN', 'SLP', 'FRZ']

HazardsList = ["Spikes", "Stealth Rock", "Toxic Spikes", "Sticky Web"]

Afflictions = {
    "Taunt": None,
    "Confused": None,
    "Ingrain": None,
    "Leech Seed": None,
    "Aqua Ring": None,
    "Attract": None,
    "Protect": None,
    "Drowsy": None,
    "Foresight": None,
    "Endure": None,
    "Rage": None,
    "Whirlpool": None,
    "Fire Spin": None,
    "Bide": None,
    "Magnet Rise": None,
    "Magic Coat": None,
    "Must recharge": None,
    "Curse": None,
    "Disable": None,
    "Destiny Bond": None,
    "Perish in 2": None,
    "Perish in 3": None,
    "Perish next turn": None,
    "Embargo": None,
    "Landed": None,
    "Telekinesis": None,
    "Laser Focus": None,
    "Torment": None,
    "Heal Block": None,
    "Bind": None,
    "Clamp": None,
    "Wrap": None,
    "Encore": None,
    "Crafty Shield": None,
    "Quick Guard": None,
    "Wide Guard": None,
    "Grudge": None,
    "Mat Block": None,
    "Instruct": None,
    "Imprisoning foe": None,
    "Nightmare": None,
    "Stockpile": None,
    "Stockpile×2": None,
    "Stockpile×3": None
}

HazardsMap = {
    "Pointed stones float in the air around your team!": ('A', "Stealth Rock", 1),
    "Spikes were scattered on the ground all around your team!": ('A', "Spikes", 1),
    "Poison spikes were scattered on the ground all around your team!": ('A', "Toxic Spikes", 1),
    "A sticky web spreads out on the ground around your team!": ('A', "Sticky Web", 1),

    "The spikes disappeared from the ground around your team!": ('A', "Stealth Rock", 0),
    "The poison spikes disappeared from the ground around your team!": ('A', "Spikes", 0),
    "The pointed stones disappeared from around your team!": ('A', "Toxic Spikes", 0),
    "The sticky web has disappeared from the ground around your team!": ('A', "Sticky Web", 0),

    "Pointed stones float in the air around the opposing team!": ('O', "Stealth Rock", 1),
    "Spikes were scattered on the ground all around the opposing team!": ('O', "Spikes", 1),
    "Poison spikes were scattered on the ground all around the opposing team!": ('O', "Toxic Spikes", 1),
    "A sticky web spreads out on the ground around the opposing team!": ('O', "Sticky Web", 1),

    "The spikes disappeared from the ground around the opposing team!": ('O', "Stealth Rock", 0),
    "The poison spikes disappeared from the ground around the opposing team!": ('O', "Spikes", 0),
    "The pointed stones disappeared from around the opposing team!": ('O', "Toxic Spikes", 0),
    "The sticky web has disappeared from the ground around the opposing team!": ('O', "Sticky Web", 0)
}

def change_hazards(hazard_dict, hazard_str):
    side, hazard, change = HazardsMap[hazard_str]
    if change == 1:
        hazard_dict[side][hazard] += 1
    else:
        hazard_dict[side][hazard] = 0
    return hazard_dict
