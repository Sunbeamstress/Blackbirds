"""
Room

Rooms are simple containers that has no location of their own.

"""

# Evennia modules.
from evennia import DefaultRoom
from collections import defaultdict
from evennia.utils.utils import (variable_from_module, lazy_property, make_iter, is_iter, list_to_string, to_str)

# Blackbirds modules.
from utilities.utils_string import AutoPunc
from typeclasses.areas import (area_id, env_id)

class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    def at_object_creation(self):
        self.db.area = area_id['VOID']
        self.db.environment = env_id['URBAN']
        self.db.temperature = 0 # How hot/cold the room is.
        self.db.illumination = 15 # The general light level in the room. 0 - dark, 15 - fully lit
        self.db.darkness = False # Whether or not the room is unnaturally dark. Overrides illumination.

        # Room flags - physical states
        self.db.indoors = False # Is the room outside or not?
        self.db.natural = False # Is the room characterized by greenery, earth, and other non-manmade environs?
        self.db.water_level = 0 # How much water does the room have in it? 0: None; 10: Completely submerged.

        # Room flags - municipal states
        self.db.public = False # Represents whether or not people will freak out about certain things (nudity, fighting, etc.)
        self.db.shop = False # The room contains goods for sale.
        self.db.house = False # The room is a house, dwelling, apartment, etc. Does not imply player ownership.
        self.db.battleground = False # The room is open for PVP with no rules whatsoever.
        self.db.craft_hall = False # You can customize and create goods in this room.
        self.db.chapel = False # This room allows you to pray to deities, or make a pact with the Blackbirds.
        self.db.bank = False # You can WITHDRAW, DEPOSIT, LOAN, and check your BALANCE here.

        # Room flags - powernet
        self.db.powered = False # Does the room contain facilities that run off of electricity?
        self.db.power_sink = False # Does the room contain facilities that constantly draw power?
        self.db.radio_tower = False # Does the room contain a kingdom's broadcast tower?
        self.db.neon_well = False # Is the room generating Neon?

        # Room flags - player housing/shops
        self.db.player_owned = False # Does a player own this room?
        self.db.player_owner_id = None # Who owns the room, if so?

    def at_desc(self, looker=None, **kwargs):
        # Seems to process things before the room is looked at.
        pass

    def return_appearance(self, looker, **kwargs):
        if not looker:
            return ""
        # Grab all accessible objects in room.
        visible = (con for con in self.contents if con != looker and
                   con.access(looker, "view"))

        exits, users, things = [], [], defaultdict(list)

        for con in visible:
            # Get the content's name.
            key = con.get_display_name(looker)

            # If the content is an exit, add to our exits list.
            if con.destination:
                exits.append(key)

            # If the content is a player, add to the players list.
            elif con.has_account:
                if con.account.is_superuser:
                    users.append(f"|Y{key}|n")
                else:
                    users.append(key)

            else:
                # Goes into our generic list of items.
                things[key].append(con)

        # Get the thing's description; build the appropriate string.
        # string = "%s\n" % self.get_display_name(looker)
        string = "|y[#%s] %s|n\n" % (self.id, AutoPunc(self.key))
        desc = self.db.desc

        if desc:
            desc = desc.replace("$p", "\n\n")
            desc = desc.replace("$n", "\n")
            string += desc

        string += "\n%s\n" % self.get_temperature_string()

        if exits:
            string += "\n|wExits:|n " + list_to_string(exits)

        if users or things:
            # Pluralize non-player objects.
            thing_strings = []
            for key, itemlist in sorted(things.items()):
                nitem = len(itemlist)
                if nitem == 1:
                    key, _ = itemlist[0].get_numbered_name(nitem, looker, key=key)

                else:
                    key = [item.get_numbered_name(nitem, looker, key=key)[1] for item in itemlist][0]

                thing_strings.append(key)

            string += "\n\n|xYou see:|n\n  " + AutoPunc(list_to_string(users + thing_strings))

        return string

    def get_temperature_string(self):
        temp = self.db.temperature

        if not temp:
            return ""

        if temp <= -23: # -10 F
            return "|WIt's deathly cold.|n"
        elif temp <= -17: # 0 F
            return "|BIt feels incredibly cold.|n"
        elif temp <= 0: # 32 F
            return "|CIt feels freezing cold.|n"
        elif temp <= 12: # 55 F
            return "|cIt feels cold.|n"
        elif temp <= 21: # 70 F
            return "It feels cool."
        elif temp <= 26: # 80 F
            return "It feels pleasant."
        elif temp <= 32: # 90 F
            return "|yIt's warm.|n"
        elif temp <= 38: # 100 F
            return "|YIt feels hot.|n"
        elif temp <= 43: # 110 F
            return "|rIt feels very hot.|n"
        else:
            return "|RIt's incredibly hot.|n"