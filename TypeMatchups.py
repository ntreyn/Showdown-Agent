



class TypeMatchups:

    default_chart = {
        "normal": 1.0,
        "fighting": 1.0,
        "flying": 1.0,
        "poison": 1.0,
        "ground": 1.0,
        "rock": 1.0,
        "bug": 1.0,
        "ghost": 1.0,
        "steel": 1.0,
        "fire": 1.0,
        "water": 1.0,
        "grass": 1.0,
        "electric": 1.0,
        "psychic": 1.0,
        "ice": 1.0,
        "dragon": 1.0,
        "dark": 1.0,
        "fairy": 1.0
    }

    type_chart = {
        "normal": default_chart,
        "fighting": default_chart,
        "flying": default_chart,
        "poison": default_chart,
        "ground": default_chart,
        "rock": default_chart,
        "bug": default_chart,
        "ghost": default_chart,
        "steel": default_chart,
        "fire": default_chart,
        "water": default_chart,
        "grass": default_chart,
        "electric": default_chart,
        "psychic": default_chart,
        "ice": default_chart,
        "dragon": default_chart,
        "dark": default_chart,
        "fairy": default_chart
    }

    def __init__(self):
        self.make_chart()

    def type_multiplier(self, attacking_type, defending_type):
        return self.type_chart[attacking_type][defending_type]

    def make_chart(self):
        self.type_chart["normal"]["rock"] = 0.5
        self.type_chart["normal"]["ghost"] = 0.0
        self.type_chart["normal"]["steel"] = 0.5

        self.type_chart["fire"]["fire"] = 0.5
        self.type_chart["fire"]["water"] = 0.5
        self.type_chart["fire"]["grass"] = 2.0
        self.type_chart["fire"]["ice"] = 2.0
        self.type_chart["fire"]["bug"] = 2.0
        self.type_chart["fire"]["rock"] = 0.5
        self.type_chart["fire"]["dragon"] = 0.5
        self.type_chart["fire"]["steel"] = 2.0

        self.type_chart["water"]["fire"] = 2.0
        self.type_chart["water"]["water"] = 0.5
        self.type_chart["water"]["grass"] = 0.5
        self.type_chart["water"]["ground"] = 2.0
        self.type_chart["water"]["rock"] = 2.0
        self.type_chart["water"]["dragon"] = 0.5

        self.type_chart["electric"]["water"] = 2.0
        self.type_chart["electric"]["electric"] = 0.5
        self.type_chart["electric"]["grass"] = 0.5
        self.type_chart["electric"]["ground"] = 0.0
        self.type_chart["electric"]["flying"] = 2.0
        self.type_chart["electric"]["dragon"] = 0.5

        self.type_chart["grass"]["fire"] = 0.5
        self.type_chart["grass"]["water"] = 2.0
        self.type_chart["grass"]["grass"] = 0.5
        self.type_chart["grass"]["poison"] = 0.5
        self.type_chart["grass"]["ground"] = 2.0
        self.type_chart["grass"]["flying"] = 0.5
        self.type_chart["grass"]["bug"] = 0.5
        self.type_chart["grass"]["rock"] = 2.0
        self.type_chart["grass"]["dragon"] = 0.5
        self.type_chart["grass"]["steel"] = 0.5

        self.type_chart["ice"]["fire"] = 0.5
        self.type_chart["ice"]["water"] = 0.5
        self.type_chart["ice"]["grass"] = 2.0
        self.type_chart["ice"]["ice"] = 0.5
        self.type_chart["ice"]["ground"] = 2.0
        self.type_chart["ice"]["flying"] = 2.0
        self.type_chart["ice"]["dragon"] = 2.0
        self.type_chart["ice"]["steel"] = 0.5

        self.type_chart["fighting"]["normal"] = 2.0
        self.type_chart["fighting"]["ice"] = 2.0
        self.type_chart["fighting"]["poison"] = 0.5
        self.type_chart["fighting"]["flying"] = 0.5
        self.type_chart["fighting"]["psychic"] = 0.5
        self.type_chart["fighting"]["bug"] = 0.5
        self.type_chart["fighting"]["rock"] = 2.0
        self.type_chart["fighting"]["ghost"] = 0.0
        self.type_chart["fighting"]["dark"] = 2.0
        self.type_chart["fighting"]["steel"] = 2.0
        self.type_chart["fighting"]["fairy"] = 0.5

        self.type_chart["poison"]["grass"] = 2.0
        self.type_chart["poison"]["poison"] = 0.5
        self.type_chart["poison"]["ground"] = 0.5
        self.type_chart["poison"]["rock"] = 0.5
        self.type_chart["poison"]["ghost"] = 0.5
        self.type_chart["poison"]["steel"] = 0.0
        self.type_chart["poison"]["fairy"] = 2.0

        self.type_chart["ground"]["fire"] = 2.0
        self.type_chart["ground"]["electric"] = 2.0
        self.type_chart["ground"]["grass"] = 0.5
        self.type_chart["ground"]["poison"] = 2.0
        self.type_chart["ground"]["flying"] = 0.0
        self.type_chart["ground"]["bug"] = 0.5
        self.type_chart["ground"]["rock"] = 2.0
        self.type_chart["ground"]["steel"] = 2.0

        self.type_chart["flying"]["electric"] = 0.5
        self.type_chart["flying"]["grass"] = 2.0
        self.type_chart["flying"]["fighting"] = 2.0
        self.type_chart["flying"]["bug"] = 2.0
        self.type_chart["flying"]["rock"] = 0.5
        self.type_chart["flying"]["steel"] = 0.5

        self.type_chart["psychic"]["fighting"] = 2.0
        self.type_chart["psychic"]["poison"] = 2.0
        self.type_chart["psychic"]["psychic"] = 0.5
        self.type_chart["psychic"]["dark"] = 0.0
        self.type_chart["psychic"]["steel"] = 0.5

        self.type_chart["bug"]["fire"] = 0.5
        self.type_chart["bug"]["grass"] = 2.0
        self.type_chart["bug"]["fighting"] = 0.5
        self.type_chart["bug"]["poison"] = 0.5
        self.type_chart["bug"]["flying"] = 0.5
        self.type_chart["bug"]["psychic"] = 2.0
        self.type_chart["bug"]["ghost"] = 0.5
        self.type_chart["bug"]["dark"] = 2.0
        self.type_chart["bug"]["steel"] = 0.5
        self.type_chart["bug"]["fairy"] = 0.5

        self.type_chart["rock"]["fire"] = 2.0
        self.type_chart["rock"]["ice"] = 2.0
        self.type_chart["rock"]["fighting"] = 0.5
        self.type_chart["rock"]["ground"] = 0.5
        self.type_chart["rock"]["flying"] = 2.0
        self.type_chart["rock"]["bug"] = 2.0
        self.type_chart["rock"]["steel"] = 0.5

        self.type_chart["ghost"]["normal"] = 0.0
        self.type_chart["ghost"]["psychic"] = 2.0
        self.type_chart["ghost"]["ghostl"] = 2.0
        self.type_chart["ghost"]["dark"] = 0.5

        self.type_chart["dragon"]["dragon"] = 2.0
        self.type_chart["dragon"]["steel"] = 0.5
        self.type_chart["dragon"]["fairy"] = 0.0

        self.type_chart["dark"]["fighting"] = 0.5
        self.type_chart["dark"]["psychic"] = 2.0
        self.type_chart["dark"]["ghost"] = 2.0
        self.type_chart["dark"]["dark"] = 0.5
        self.type_chart["dark"]["fairy"] = 0.5

        self.type_chart["steel"]["fire"] = 0.5
        self.type_chart["steel"]["water"] = 0.5
        self.type_chart["steel"]["electric"] = 0.5
        self.type_chart["steel"]["ice"] = 2.0
        self.type_chart["steel"]["rock"] = 2.0
        self.type_chart["steel"]["steel"] = 0.5
        self.type_chart["steel"]["fairy"] = 2.0

        self.type_chart["fairy"]["fire"] = 0.5
        self.type_chart["fairy"]["fighting"] = 2.0
        self.type_chart["fairy"]["poison"] = 0.5
        self.type_chart["fairy"]["dragon"] = 2.0
        self.type_chart["fairy"]["dark"] = 2.0
        self.type_chart["fairy"]["steel"] = 0.5


