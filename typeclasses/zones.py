# Evennia modules.
from evennia import DefaultObject

class Zone(DefaultObject):
    def at_object_creation(self):
        self.name = "Unnamed"
        self.db.fullname = "Unnamed Zone"
        self.db.area = 0
        self.db.open_pvp = False
        self.db.rooms = []

    def fullname(self):
        return self.db.fullname

    def area(self):
        return self.db.area

    def open_pvp(self):
        return self.db.open_pvp

    def add_room(self, room):
        self.db.rooms.add(room)

    def remove_room(self, room):
        self.db.rooms.remove(room)

    def rooms(self):
        return self.db.rooms