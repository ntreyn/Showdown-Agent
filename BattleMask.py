




class Mask:

    def __init__(self):

        """
        *** Must manually check for extender (terrain extender, damp rock, light clay, etc)


        Weather:
            Sun * 
            Heavy sun *
            Rain *
            Heavy sun *
            Sand *
            Hail *
            Strong winds *

        Terrain:
            Electric *
            Misty *
            Grassy *
            Psychic *

        Screens:
            Light screen *
            Reflect *
            Aurora Veil *

        Hazards:
            Rocks x
            Spikes x
            Toxic Spikes x
            Webs x

        Magic:
            Trick room *
            Wonder room *
            Magic room *
            Gravity *
            Perish Song x

        Sports:
            Water Sport *
            Mud Sport *

        Misc:
            Uproar x
            Plegdes ?

        

        """
        
        self.field = {
            "conditions": None,
            "hazards": None
        }
    

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



        Movesets
        Speed Tiers
        Calcs / Spreads (defensive, offensive, etc)


    """