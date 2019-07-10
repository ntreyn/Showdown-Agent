





class Mask:

    ConditionCauses = {
        "Sun": { "move": "Sunny Day", "ability": "Drought" },
        "Rain": { "move": "Rain Dance", "ability": "Drizzle" },
        "Sand": { "move": "Sandstorm", "ability": "Sand Stream" },
        "Hail": { "move": "Hail", "ability": "Snow Warning" },

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
        "Mud Sport": { "move": "Mud Sport", "ability": None }
    }

    StatusList = ['BRN', 'TOX', 'PAR', 'PSN', 'SLP', 'FRZ']

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

    def __init__(self):

        """
        *** Must manually check for extender (terrain extender, damp rock, light clay, etc)


        Weather:
            Sun : Sunny Day, Drought
            Heavy sun : Desolate Land
            Rain : Rain Dance, Drizzle
            Heavy Rain : Primordial Sea
            Sand : Sandstorm, Sand Stream
            Hail : Hail, Snow Warning
            Strong winds : Delta Stream


        Terrain:
            Electric : Electric Terrain, Electric Surge
            Misty : Misty Terrain, Misty Surge
            Grassy : Grassy Terrain, Grassy Surge
            Psychic : Psychic Terrain, Psychic Surge

        Screens:
            Light screen : Light Screen
            Reflect : Reflect
            Aurora Veil : Aurora Veil

        Hazards:
            Rocks x
            Spikes x
            Toxic Spikes x
            Webs x

        Magic:
            Trick room : Trick Room
            Wonder room : Wonder Room
            Magic room : Magic Room
            Gravity : Gravity
            Perish Song x

        Sports:
            Water Sport : Water Sport
            Mud Sport : Mud Sport

        Misc:
            Uproar x
            Plegdes ?

        

        """
        
        self.field = {
            "conditions": {},
            "hazards": {}
        }

        self.opponent_team = {}

        self.agent_team = {}
    

    """
    Field:
        Weather
        Terrain
        Screens

    Pokemon:
        Status
        HP
        PP
        Items
        Fainted
        Abilities
        Substitute
        Perish Song
        Leech Seed
        Ingrain

        Opponent Nicknames

        Form change

        Movesets
        Speed Tiers
        Calcs / Spreads (defensive, offensive, etc)


    """
    

    def update(self, set_changes, field_changes):
        pass