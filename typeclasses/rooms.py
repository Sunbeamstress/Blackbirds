"""
Room

Rooms are simple containers that has no location of their own.

"""

# Evennia modules.
from evennia import DefaultRoom
from collections import defaultdict
from evennia.utils.utils import (variable_from_module, lazy_property,
                                 make_iter, is_iter, list_to_string,
                                 to_str)

# Blackbirds modules.
from utilities.utils_string import AutoPunc


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
        self.db.environment = "Urban"
        self.db.temperature = 21

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

            string += "\n|xYou see:|n\n" + list_to_string(users + thing_strings)

        return string