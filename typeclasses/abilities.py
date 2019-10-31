"""
The primary ability class. All abilities inherit from this.
"""

class Ability():
    "A core ability - each has their own rules and command sets. Training these boosts the appropriate AbilityTree."
    def __init__(self):
        self._can_train = True
        self._costs_rubric = False
        self._levels = 5
        self._description = "An undefined ability."
        self._cost = 10

    def update(self):
        pass

    def can_train(self):
        return self._can_train

    def max_level(self):
        "Get the highest allowable training level for this ability."
        return self._levels

    def cur_level(self, ply):
        "Audit the player's current level in this ability."
        pass

    def get_description(self):
        return self._description

    def at_ability_creation(self):
        "Called when the game initializes the ability. Use to set its properties."
        pass

    def get_cost(self):
        "Returns the base cost of the ability in experience."
        return self._cost

class AbilityTree(Ability):
    """
    A collection of abilities under a unified theme.

    These behave in the same way as abilities, but cannot be directly trained.
    """
    def __init__(self):
        self._can_train = False
        self._supported_abilities = []

    def cur_level(self, ply):
        "Returns the player's summed level in this ability tree, based on the abilities learned under it."
        pass

    def at_ability_tree_creation(self):
        "Hook this method to add abilities to the tree. Needed so that methods such as cur_level() can work properly."
        pass

    def add_ability(self, ab_class):
        "Use this method in conjunction with at_ability_tree_creation() to subscribe abilities to the tree."
        self._supported_abilities.append(ab_class)

    def get_abilities(self):
        return [ab for ab in self._supported_abilities]