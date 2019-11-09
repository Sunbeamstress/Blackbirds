"""
The primary ability class. All abilities inherit from this.
"""

class Ability():
    def __init__(self):
        self.key = "UndefinedAbility"
        self.name = "Undefined Ability"
        self._can_train = True
        self._costs_rubric = False
        self._levels = 10
        self._cur_level = 0
        self._description = "An undefined ability."
        self._cost = 10
        self.tiers = {}

    def update(self):
        pass

    def name(self):
        return self.key

    def can_train(self):
        return self._can_train

    def max_level(self):
        "Get the highest allowable training level for this ability."
        return self._levels

    def cur_level(self):
        "Audit the player's current level in this ability."
        return self._cur_level

    def description(self):
        return self._description

    def get_cost(self):
        "Returns the base cost of the ability in experience."
        return self._cost