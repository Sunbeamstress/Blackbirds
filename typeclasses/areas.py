area_id = {
    'VOID': 0,
    'BRILLANTE': 1
}

env_id = {
    'URBAN': 0,
    'GRASSLANDS': 1,
    'FOREST': 2
}

class Area():
    def __init__(self, id = 0, name = None):
        self.id = id
        self.name = name

class Environment():
    def __init__(self, id = 0, name = None, color = "321"):
        self.id = id
        self.name = name
        self.color = color

AREA_VOID = Area(0, "The Void")
AREA_BRILLANTE = Area(1, "The City of Brillante")

ENV_URBAN = Environment(0, "Urban", "333")
ENV_GRASSLANDS = Environment(1, "Grasslands", "242")
ENV_FOREST = Environment(2, "Forest", "131")