from abilities.core_stats import *

from typeclasses.abilities import AbilityTree

class Might(AbilityTree):
    def at_ability_creation(self):
        self.key = "Might"
        self._description = "An indication of the character's overall physical prowess and athleticism."
        self.add_ability(Strength())

class Dexterity(AbilityTree):
    def at_ability_creation(self):
        self.key = "Dexterity"
        self._description = "The character's agility, speed, and reflexes."
        self.add_ability(Speed())
        self.add_ability(Acrobatics())

class Acuity(AbilityTree):
    def at_ability_creation(self):
        self.key = "Acuity"
        self._description = "The character's perception - ability to see, hear, or sense things."
        self.add_ability(Vision())