class Archetype():
    def __init__(self):
        self.name = "Unknown Archetype"
        self.plural_name = "Unknown Archetypes"

class Blackbird(Archetype):
    def __init__(self):
        super().__init__()

        self.name = "Blackbird"
        self.plural_name = "Blackbirds"

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

class Survivalist(Archetype):
    def __init__(self):
        super().__init__()

        self.name = "Survivalist"
        self.plural_name = "Survivalists"