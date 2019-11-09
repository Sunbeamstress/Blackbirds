"""
Abilities representing a character's physical characteristics.
"""
from typeclasses.abilities import Ability

class Strength(Ability):
    def __init__(self):
        super().__init__()
        self.key = "strength"
        self.name = "Strength"
        self._description = "A representation of your sheer brawn; a measure of your muscular output. Strength is your ability to hit things harder, lift heavier objects, and perform more work than others."
        self.tiers = {
            1: ("cmd: gutpunch", "cmd: smash", "You can smash certain flimsy objects.", "You do more damage with melee attacks."),
            2: ("cmd: grapple", "cmd: knockout", "You can smash windows and weak doors.", "You do much more damage with melee attacks."),
            3: ("cmd: clothesline", "You can smash through strong doors, weak locks, and weak walls.", "You do considerable damage with melee attacks."),
        }

class Speed(Ability):
    def __init__(self):
        super().__init__()
        self.key = "speed"
        self.name = "Speed"
        self._description = "A fine control over the rapidity of your body. You move faster and can repeat tasks more quickly than others."
        self.tiers = {
            1: ("You move slightly more quickly through rooms."),
            2: ("cmd:sprint", "You move much more quickly through rooms."),
            3: ("You move considerably more quickly through rooms."),
        }

class Acrobatics(Ability):
    def __init__(self):
        super().__init__()
        self.key = "acrobatics"
        self.name = "Acrobatics"
        self._description = "Represents your ability to leap, roll, or otherwise maneuver."
        self.tiers = {
            1: (""),
            2: (""),
            3: ("")
        }

class Vision(Ability):
    def __init__(self):
        super().__init__()
        self.key = "vision"
        self.name = "Vision"
        self._description = "How far or how sharply you can see. Confers a bonus to spotting hidden players and objects."
        self.tiers = {
            1: (""),
            2: (""),
            3: ("")
        }