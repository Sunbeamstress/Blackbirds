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
        return env_id[id]["name"]

    def shortname(self, id = 0):
        short = env_id[id]["short"]
        if not short:
            return env_id[id]["name"]

        return env_id[id]["short"]

    def color(self, id = 0):
        return env_id[id]["color"]

    def is_natural(self, id = 0):
        return env_id[id]["natural"]

    def __str__(self, id = 0):
        "Shortcut for get_name()."
        return self.get_name(id)