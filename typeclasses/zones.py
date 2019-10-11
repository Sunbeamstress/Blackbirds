# Python modules.
import json

# Evennia modules.
from evennia.utils.utils import class_from_module

# Blackbirds modules.
from typeclasses.areas import Area

# Deserialize the environment data file.
zone_data = None
with open("json/zones.json", "r") as json_file:
    zone_data = json.load(json_file)

zone_id = zone_data["id"]

class Zone():
    "A class whose purpose is to retrieve data from the zones defined at json/zones.json."
    def name(self, id = 0):
        if not self._is_valid_id(id):
            return "????"

        return zone_id[id]["name"]

    def fullname(self, id = 0):
        if not self._is_valid_id(id):
            return "?????"

        return zone_id[id]["fullname"]

    def area(self, id = 0):
        if not self._is_valid_id(id):
            return 0

        return zone_id[id]["area"]

    def area_name(self, id = 0):
        if not self._is_valid_id(id):
            return "????"

        a = Area()
        return a.name(self.area(id))

    def area_fullname(self, id = 0):
        if not self._is_valid_id(id):
            return "????"

        a = Area()
        return a.fullname(self.area(id))

    def is_open_pvp(self, id = 0):
        if not self._is_valid_id(id):
            return "????"

        a = Area()
        return a.is_open_pvp(self.area(id))

    def __str__(self, id = 0):
        "Shortcut for get_name()."
        return self.name(id)

    def _is_valid_id(self, id):
        try:
            test_id = zone_id[id]
        except IndexError:
            return False

        return True

    def __len__(self):
        "Returns the total number of defined zones."
        return len(zone_id)

    def rooms(self, id):
        if not self._is_valid_id(id):
            return None

        Room = class_from_module("typeclasses.rooms.Room")
        room_list = [room for room in Room.objects.all() if room.db.zone == id]
        return room_list