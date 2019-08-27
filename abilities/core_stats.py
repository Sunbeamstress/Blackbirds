"""
Abilities representing a character's physical characteristics.
"""
from abilities import ability as BaseAbility
from abilities import ability as BaseAbilityTree

# ------------------------------------------------------------------------------

class Might(BaseAbilityTree):
    def at_ability_creation(self):
        self.description = "An indication of the character's overall physical prowess and athleticism."

    def at_ability_tree_creation(self):
        self.add(Strength())

class Strength(BaseAbility):
    def at_ability_creation(self):
        self.description = "The character's physical strength."

# ------------------------------------------------------------------------------

class Dexterity(BaseAbilityTree):
    "The character's agility, speed, and reflexes."
    def at_ability_tree_creation(self):
        self.add(Agility())

class Agility(BaseAbility):
    def at_ability_creation(self):
        self.description = "Represents the character's ability to leap, roll, or otherwise maneuver."

# ------------------------------------------------------------------------------

class Acuity(BaseAbilityTree):
    "The character's perception - ability to see, hear, or sense things."
    def at_ability_tree_creation(self):
        self.add(Vision())

class Vision(BaseAbility):
    def at_ability_creation(self):
        self.description = "How far or how sharply the character can see. Confers a bonus to spotting hidden players and objects."