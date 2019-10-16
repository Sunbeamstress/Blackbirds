# Evennia modules.
from evennia import DefaultRoom
from collections import defaultdict
from evennia.utils.utils import (variable_from_module, lazy_property, make_iter, is_iter, list_to_string, to_str)

# Blackbirds modules.
from commands.default_cmdsets import ChargenCmdSet
from utilities.utils_display import Line
from utilities.utils_string import jleft, jright, AutoPunc
import utilities.utils_directions as dirs
from typeclasses.environments import Environment
from typeclasses.areas import Area
from typeclasses.zones import Zone
from typeclasses.exits import Exit
from world.map import Map

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
        self.db.x = 0
        self.db.y = 0
        self.db.z = 0

        self.db.exits = {
            "northwest": None,
            "north": None,
            "northeast": None,
            "west": None,
            "east": None,
            "southwest": None,
            "south": None,
            "southeast": None,
            "up": None,
            "down": None,
            "in": None,
            "out": None
        }

        self.db.zone = None
        self.db.environment = 0
        self.db.temperature = 30 # How hot/cold the room is.
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
        self.db.radio_tower = False # Does the room contain a Brillante broadcast tower?
        self.db.neon_well = False # Is the room generating Neon?

        # Room flags - player housing/shops
        self.db.player_owned = False # Does a player own this room?
        self.db.player_owner_id = None # Who owns the room, if so?

        self.db.symbol = None
        self.db.symbol_override = False

    def get_exits(self):
        exit_list = []
        for dir, obj in self.db.exits.items():
            if obj != None:
                exit_list.append(dir)

        return exit_list

    def has_exit(self, dir):
        return True if self.db.exits[dir] != None else False

    def create_exit(self, dir, dest, oneway = False):
        err_msg = "|xCould not create a new exit. %s|n"
        opp_dir = None

        # Check if exit already exists.
        if self.has_exit(dir):
            err_msg = err_msg % f"There is already a {dir}ward exit."
            return False, err_msg

        # Check if destination is valid room.
        if not dest:
            err_msg = err_msg % "There is no room in that direction to link to."
            return False, err_msg

        # If exit is not one-way, make sure the other room doesn't already have the opposite exit.
        if not oneway:
            opp_dir = dirs.opposite_direction(dir)
            if dest.has_exit(opp_dir):
                err_msg = err_msg % f"That room already has a {opp_dir}ward exit."
                return False, err_msg

        self.db.exits[dir] = Exit()
        self.db.exits[dir].source = self
        self.db.exits[dir].destination = dest.id

        if not oneway and opp_dir:
            dest.db.exits[opp_dir] = Exit()
            dest.db.exits[opp_dir].source = dest
            dest.db.exits[opp_dir].destination = self

        return True, ""

    def delete_exit(self, dir, oneway = False):
        err_msg = "Could not delete the exit. %s"
        dest, opp_dir = None, None

        if not self.has_exit(dir):
            err_msg = err_msg % f"There is no {dir}ward exit."
            return False, err_msg

        dest = self.db.exits[dir].destination

        if dest and not oneway:
            opp_dir = dirs.opposite_direction(dir)
            if dest.has_exit(opp_dir):
                dest.db.exits[opp_dir].delete()

        self.db.exits[dir].delete()
        return True, ""

    def get_exit_dest(self, dir):
        exit = self.db.exits[dir]
        return exit.get_destination() if exit else None

    def at_desc(self, looker=None, **kwargs):
        # Seems to process things before the room is looked at.
        pass

    def return_appearance(self, looker, **kwargs):
        if not looker:
            return ""

        # Grab all accessible objects in room.
        visible = (con for con in self.contents if con != looker and con.access(looker, "view"))
        exit_list = self.get_exits()
        users, things = [], []

        for con in visible:
            # Get the content's name.
            key = con.get_display_name(looker)

            # If the content is a player, add to the players list.
            if con.has_account:
                # if con.account.is_superuser:
                #     users.append(f"|Y{key}|n")
                # else:
                users.append(f"{con.name}")

            else:
                # Goes into our generic list of items.
                things.append(con.db.long_desc)

        string = self.format_room_title()

        string += "\n%s" % Map(looker).draw_map()
        string += "\n\n%s" % Map(looker)._get_zone_rooms(looker.zone())

        string += "\n%s" % self.get_temperature_string()

        desc = self.db.desc
        if desc:
            desc = desc.replace("$p", "\n\n")
            desc = desc.replace("$n", "\n")
            string += desc

        if things:
            for item in things:
                string += f" |c{item}|n"

        if users:
            for user in users:
                u_desc = f" |C{user} is here.|n"
                string += u_desc

        # string += "\n  %s" % self.get_illumination_string()
        if self.db.water_level > 0:
            string += "\n  %s" % self.get_water_level_string()

        if exit_list:
            string += "\n|235You see exits leading " + list_to_string(exit_list) + "|n."
        else:
            string += "\n|235You see no exits.|n"

        return string

    def format_room_title(self):
        r_name = self.name
        r_id = self.id
        r_id_zeroes = "0" * (4 - len(str(r_id)))

        r_area = self.areaname()
        r_zone = self.zonefullname()

        env = Environment()
        r_env = env.colorshort(self.db.environment)

        return f"|y{AutoPunc(r_name)}|n |213(|n|525{r_zone}, {r_area}|n|213)|n |x[|n{r_env}|x]|n |213(v|n|202{r_id_zeroes}|n|525{r_id}|n|213)|n"

    def get_temperature_string(self):
        temp = self.db.temperature

        if temp <= -23: # -10 F
            return "|025It's deathly cold.|n"
        elif temp <= -17: # 0 F
            return "|135It feels incredibly cold.|n"
        elif temp <= 0: # 32 F
            return "|245It feels freezing cold.|n"
        elif temp <= 12: # 55 F
            return "|355It feels cold.|n"
        elif temp <= 21: # 70 F
            return "|455It feels cool."
        elif temp <= 26: # 80 F
            return "|wIt feels pleasant.|n"
        elif temp <= 32: # 90 F
            return "|543It's warm.|n"
        elif temp <= 38: # 100 F
            return "|532It feels hot.|n"
        elif temp <= 43: # 110 F
            return "|521It feels very hot.|n"
        else:
            return "|510It's incredibly hot.|n"

    def get_illumination_string(self):
        light = self.db.illumination

        if light <= 0:
            return "|212It's completely dark.|n"
        elif light <= 4:
            return "|322There's barely enough light to read by.|n"
        elif light <= 9:
            return "|432The surroundings are dimly lit.|n"
        elif light <= 14:
            return "|541It's well lit here.|n"
        else:
            return "|553The place is bathed in bright light.|n"

    def get_water_level_string(self):
        level = self.db.water_level

        if level <= 0:
            return None
        elif level <= 4:
            return "Your footfalls disturb puddles of water."
        elif level <= 9:
            return "Water flows around your thighs."
        elif level <= 14:
            return "You wade through chest-high water."
        else:
            return "This area is submerged underwater."

    def areaname(self):
        if not self.db.zone or not self.db.zone.area:
            return "Static"

        return self.db.zone.area.name

    def areafullname(self):
        if not self.db.zone or not self.db.zone.area:
            return "An expanse of static"

        return self.db.zone.area.db.fullname

    def zone(self):
        return self.db.zone

    def zonename(self):
        if not self.db.zone:
            return "Void"

        return self.db.zone.name

    def zonefullname(self):
        if not self.db.zone:
            return "The Void"

        return self.db.zone.fullname

class ChargenRoom(Room):
    def at_object_creation(self):
        self.cmdset.add(ChargenCmdSet, permanent = True)

    def format_room_title(self):
        return Line(col_string = "|035", label = "Character Creation", col_label = "|055")

    def return_appearance(self, looker, **kwargs):
        if not looker:
            return ""

        string = self.format_room_title() + "\n"

        desc = self.db.desc
        if desc:
            desc = desc.replace("$p", "\n\n")
            desc = desc.replace("$n", "\n")
            string += desc

        return string