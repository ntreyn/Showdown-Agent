
from Set import Set


class Pokemon(object):

    def __init__(self, info_dict):
        for key in info_dict:
            setattr(self, key, info_dict[key])

        # (set, probablity)
        self.usage_sets = []

        self.hp = 0

        self.stats_changes = {
            "HP": 1.0,
            "Atk": 1.0,
            "Def": 1.0,
            "SpA": 1.0,
            "SpD": 1.0,
            "Spe": 1.0
        }
        
    
    def create_set(self, set_dict):
        self.set = Set(set_dict)
    
    def update_set(self, set_dict):
        self.set.update_set(set_dict)

    def print(self):
        print(self.id, self.species, self.types, self.abilities)
        for key, val in self.baseStats.items():
            print("{}: {}, ".format(key, val), end='')
        print()
    
    def print_set(self):
        self.set.print()




