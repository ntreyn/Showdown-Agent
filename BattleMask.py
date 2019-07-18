





class Mask:

    

    def __init__(self):

        """
        *** Must manually check for extender (terrain extender, damp rock, light clay, etc)

        """
        
        self.field = {
            "conditions": {},
            "hazards": {
                "A": {
                    "Spikes": 0, 
                    "Stealth Rock": 0, 
                    "Toxic Spikes": 0, 
                    "Sticky Web": 0
                },
                "O": {
                    "Spikes": 0, 
                    "Stealth Rock": 0, 
                    "Toxic Spikes": 0, 
                    "Sticky Web": 0
                },
            }
        }

        self.opponent_team = {}
        self.agent_team = {}
    

    def update(self, opponent_team, opponent_active, agent_team, agent_active, field_changes):
        self.field = field_changes

        self.opponent_team = opponent_team
        self.opponent_active = opponent_active

        self.agent_team = agent_team
        self.agent_active = agent_active

        