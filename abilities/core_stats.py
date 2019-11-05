"""
Abilities representing a character's physical characteristics.
"""
from typeclasses.abilities import Ability

class Strength(Ability):
    def __init__(self):
        super().__init__()
        self.key = "Strength"
        self._description = "The character's physical strength."

class Speed(Ability):
    def __init__(self):
        super().__init__()
        self.key = "Speed"
        self._description = "The character's ability to traverse distances in a given amount of time."

class Acrobatics(Ability):
    def __init__(self):
        super().__init__()
        self.key = "Acrobatics"
        self._description = "Represents the character's ability to leap, roll, or otherwise maneuver."

class Vision(Ability):
    def __init__(self):
        super().__init__()
        self.key = "Vision"
        self._description = "How far or how sharply the character can see. Confers a bonus to spotting hidden players and objects."