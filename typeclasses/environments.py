# Python modules.
import json

# Blackbirds modules.

# Deserialize the environment data file.
env_data = None
with open("json/environments.json", "r") as json_file:
    env_data = json.load(json_file)

env_id = env_data["id"]

class Environment():
    "A class whose purpose is to retrieve data from the environments defined at json/environments.json."
    def name(self, id = 0):
        if not self._is_valid_id(id):
            return "????"

        return env_id[id]["name"]

    def shortname(self, id = 0):
        if not self._is_valid_id(id):
            return "?????"

        return env_id[id]["short"]

    def color(self, id = 0):
        if not self._is_valid_id(id):
            return "500"

        return env_id[id]["color"]

    def colorname(self, id = 0):
        if not self._is_valid_id(id):
            return "|500????|n"

        e_color = self.color(id)
        e_name = self.name(id)

        return f"|{e_color}{e_name}|n"

    def colorshort(self, id = 0):
        if not self._is_valid_id(id):
            return "|500?????|n"

        e_color = self.color(id)
        e_short = self.shortname(id)

        return f"|{e_color}{e_short}|n"

    def is_natural(self, id = 0):
        if not self._is_valid_id(id):
            return False

        return env_id[id]["natural"]

    def __str__(self, id = 0):
        "Shortcut for get_name()."
        return self.name(id)

    def _is_valid_id(self, id):
        try:
            test_id = env_id[id]
        except IndexError:
            return False

        return True

    def __len__(self):
        "Returns the total number of defined environments."
        return len(env_id)