




class Agent:
    
    def __init__(self, mask):
        self.mask = mask

    def lead(self):
        raw_act = input("Choose lead: ")
        value = int(raw_act)
        name = "chooseTeamPreview"
        return {"name": name, "value": value}

    def get_switch(self):
        raw_act = input("Choose switch: ")
        value = int(raw_act)
        name = "chooseSwitch"
        return {"name": name, "value": value}

    def get_action(self):
        """
        Action mappings:
        [A/S][1-4/1-6]
        """
        raw_act = input("Choose action: ")
        value = int(raw_act[1])
        mega = False
        zmove = False
        if raw_act[0].upper() == 'A':
            name = "chooseMove"
        elif raw_act[0].upper() == 'M':
            name = "chooseMove"
            mega = True
        elif raw_act[0].upper() == 'Z':
            name = "chooseMove"
            zmove = True
        else:
            name = "chooseSwitch"
        return {"name": name, "value": value, "mega": mega, "zmove": zmove}