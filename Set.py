

class Set(object):

    # for usage sets, probability for each attribute

    def __init__(self, set_dict):

        self.EVs = {
            "HP": 0,
            "Atk": 0,
            "Def": 0,
            "SpA": 0,
            "SpD": 0,
            "Spe": 0
        }

        self.IVs = {
            "HP": 31,
            "Atk": 31,
            "Def": 31,
            "SpA": 31,
            "SpD": 31,
            "Spe": 31
        }

        self.keys_total = ["team_number", "species", "nickname", "gender", "item", "ability", "level",
                            "shiny", "happiness", "EVs", "nature", "IVs", "moves", "fainted", "hp", 
                            "status",  "afflictions", "stats_changes", "new_types", "added_type", "knocked", "temp_ability"]
        self.keys_in = ["EVs", "IVs", "fainted", "hp", "status", "afflictions", "stats_changes", "new_types", 
                            "added_type", "knocked", "temp_ability"]
        self.battle_reset()
        self.update_set(set_dict)

    def switch_reset(self):
        
        self.afflictions = []
        self.new_types = []
        self.added_type = None
        self.temp_ability = None

        self.stats_changes = {
            "Atk": 0,
            "Def": 0,
            "SpA": 0,
            "SpD": 0,
            "Spe": 0,
            "Evasion": 0,
            "Accuracy": 0
        }

    def battle_reset(self):
        self.fainted = False
        self.hp = 100.0
        self.status = None
        self.knocked = False
        self.switch_reset()

    def update_set(self, set_dict):
        set_dict = self.set_evs_ivs(set_dict)

        for key in set_dict:
            setattr(self, key, set_dict[key])
            self.keys_in.append(key)

    def set_evs_ivs(self, set_dict):
        if "IVs" in set_dict:
            temp_IVs = set_dict.pop("IVs")
            for key in temp_IVs:
                self.IVs[key] = temp_IVs[key]
        
        if "EVs" in set_dict:
            temp_EVs = set_dict.pop("EVs")
            for key in temp_EVs:
                self.EVs[key] = temp_EVs[key]
        
        return set_dict

    def print(self):
        for key in self.keys_total:
            if key in self.keys_in:
                print("{}: {}".format(key, getattr(self, key)))
        print("\n")


        


    