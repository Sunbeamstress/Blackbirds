# Evennia modules.
from evennia import DefaultObject

class Area(DefaultObject):
    def at_object_creation(self):
        self.name = "Unnamed"
        self.db.fullname = "Unnamed Area"
        self.db.is_city = False
        self.db.open_pvp = False
        self.db.zones = []

    def fullname(self):
        return self.db.fullname

    def is_city(self):
        return self.db.is_city

    def open_pvp(self):
        return self.db.open_pvp

    def add_zone(self, zone):
        self.db.zones.add(zone)

    def remove_zone(self, zone):
        self.db.zones.remove(zone)

    def zones(self):
        return self.db.zones