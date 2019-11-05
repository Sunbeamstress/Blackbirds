"""
The primary ability class. All abilities inherit from this.
"""

class Ability():
    "A core ability - each has their own rules and command sets. Training these boosts the appropriate AbilityTree."
    def __init__(self):
        self.key = "UndefinedAbility"
        self._can_train = True
        self._costs_rubric = False
        self._levels = 10
        self._cur_level = 0
        self._description = "An undefined ability."
        self._cost = 10
        self._supported_abilities = []

        self.at_ability_creation()

    def update(self):
        pass

    def name(self):
        return self.key

    def can_train(self):
        return self._can_train

    def max_level(self):
        "Get the highest allowable training level for this ability."
        return self._levels

    def level(self):
        pass

    def cur_level(self):
        "Audit the player's current level in this ability."
        return self._cur_level

    def get_description(self):
        return self._description

    def at_ability_creation(self):
        "Called when the game initializes the ability. Use to set its properties."
        pass

    def add_ability(self):
        pass

    def get_abilities(self):
        pass

    def get_cost(self):
        "Returns the base cost of the ability in experience."
        return self._cost

class AbilityTree(Ability):
    """
    A collection of abilities under a unified theme.

    These differ from regular abilities in that they
        1) cannot be directly trained,
        2) feature a list of 'supported abilities' in which regular abilities reside.
    """
    def __init__(self):
        super().__init__()
        self._can_train = False

    def level(self):
        "Returns the player's summed level in this ability tree, based on the abilities learned under it."
        lvl = 0
        for ab in self._supported_abilities:
            lvl += ab.cur_level()

        return lvl

    def add_ability(self, ab_class):
        "Use this method in conjunction with at_ability_creation() to subscribe abilities to the tree."
        self._supported_abilities.append(ab_class)

    def get_abilities(self):
        return [ab for ab in self._supported_abilities]