# Python modules.
import json

# Blackbirds modules.

# Deserialize the environment data file.
area_data = None
with open("json/areas.json", "r") as json_file:
    area_data = json.load(json_file)

area_id = area_data["id"]

class Area():
    "A class whose purpose is to retrieve data from the areas defined at json/areas.json."
    def name(self, id = 0):
        if not self._is_valid_id(id):
            return "????"

        return area_id[id]["name"]

    def fullname(self, id = 0):
        if not self._is_valid_id(id):
            return "?????"

        return area_id[id]["fullname"]

    def is_city(self, id = 0):
        if not self._is_valid_id(id):
            return False

        return area_id[id]["city"]

    def is_open_pvp(self, id = 0):
        if not self._is_valid_id(id):
            return False

        return area_id[id]["open_pvp"]

    def __str__(self, id = 0):
        "Shortcut for get_name()."
        return self.name(id)

    def _is_valid_id(self, id):
        try:
            test_id = area_id[id]
        except IndexError:
            return False

        return True

    def __len__(self):
        "Returns the total number of defined environments."
        return len(area_id)