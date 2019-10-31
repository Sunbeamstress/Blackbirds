class Archetype():
    def __init__(self):
        self.name = "Unknown Archetype"
        self.plural_name = "Unknown Archetypes"

        self.rubric_cost = 0
        self.player_accessible = True

    def update(self):
        pass

class Blackbird(Archetype):
    def __init__(self):
        super().__init__()

        self.name = "Blackbird"
        self.plural_name = "Blackbirds"
        self.rubric_cost = 999999
        self.player_accessible = False

class Citizen(Archetype):
    def __init__(self):
        super().__init__()

        self.name = "Citizen"
        self.plural_name = "Citizens"

class Privileged(Archetype):
    def __init__(self):
        super().__init__()

        self.name = "Privileged"
        self.plural_name = "The Privileged"
        self.rubric_cost = 100

class Survivalist(Archetype):
    def __init__(self):
        super().__init__()

        self.name = "Survivalist"
        self.plural_name = "Survivalists"
        self.rubric_cost = 25