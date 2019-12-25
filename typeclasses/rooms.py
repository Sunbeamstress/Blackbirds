# Python
from datetime import datetime

# Evennia modules.
from evennia import DefaultRoom
from evennia.objects.models import ObjectDB
from collections import defaultdict
from evennia.utils.utils import (variable_from_module, lazy_property, make_iter, is_iter, list_to_string, to_str)

# Blackbirds modules.
from commands.default_cmdsets import ChargenCmdSet
from utilities.display import header, divider
from utilities.room import get_room
from utilities.string import jleft, jright, punctuate
import utilities.directions as dirs
from typeclasses.environments import Environment
from typeclasses.areas import Area
from typeclasses.zones import Zone
from world.map import Map

_ScriptDB = None

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

        self.build_exits()

        self.db.fullname = ""
        self.db.desc = ""

        self.db.zone = None
        self.db.environment = None
        self.db.temperature = 30 # How hot/cold the room is.
        self.db.illumination = 15 # The general light level in the room. 0 - dark, 15 - fully lit
        self.db.darkness = False # Whether or not the room is unnaturally dark. Overrides illumination.

        # Room flags - physical states
        self.db.indoors = False # Is the room outside or not?
        self.db.insulated = False # Does the room ignore weather and maintain a comfortable temperature?
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

    def build_exits(self):
        self.db.exits = {}
        _ = [self.reset_exit(dir) for dir in ("northwest", "north", "northeast", "west", "east", "southwest", "south", "southeast", "up", "down", "in", "out")]

    def update(self):
        pass

    def delete(self):
        global _ScriptDB
        if not _ScriptDB:
            from evennia.scripts.models import ScriptDB as _ScriptDB

        if not self.pk or not self.at_object_delete():
            # This object has already been deleted, or the pre-delete check returned False.
            return False

        # Halt any running scripts on this room.
        for script in _ScriptDB.objects.get_all_scripts_on_obj(self):
            script.stop()

        # Destroy any exits to this room, if any.
        for e in self.get_exits():
            dest_room = get_room(self.db.exits[e]['dest'])
            if dest_room:
                opp_e = dirs.opposite_direction(e)
                dest_room.reset_exit(opp_e)

        # Remove this room from its zone.
        if self.db.zone:
            self.db.zone.remove_room(self)

        # Clear out any non-exit objects located within the object
        self.clear_contents()
        self.attributes.clear()
        self.nicks.clear()
        self.aliases.clear()

        # Perform the deletion of the object
        super().delete()
        return True

    def _valid_exit(self, dir):
        if not self.db.exits[dir]:
            return False

        if self.db.exits[dir] == None:
            return False

        if self.db.exits[dir]["dest"] == None:
            return False

        return True

    def get_exits(self, visible_only = False):
        exit_list = []

        if not self.db.exits:
            return []

        for dir in self.db.exits:
            if not self._valid_exit(dir):
                continue

            if visible_only and self.db.exits[dir]["visible"] != True:
                continue

            exit_list.append(dir)

        return exit_list

    def has_exit(self, dir):
        return self._valid_exit(dir)

    def reset_exit(self, dir):
        self.db.exits[dir] = {"dest": None, "visible": True, "door": False, "locked": False, "accessible": True}

    def exit_destination(self, dir):
        return self.db.exits[dir]["dest"] if self.has_exit(dir) else None

    def create_exit(self, dir, dest):
        err_msg = "|xCould not create a new exit. %s|n"
        opp_dir = None

        # Check if exit already exists.
        if self.has_exit(dir):
            err_msg = err_msg % f"There is already a {dir}ward exit."
            return False, err_msg

        # Check if destination is valid room.
        if not dest:
            err_msg = err_msg % "That doesn't seem to be a valid room to link to."
            return False, err_msg

        opp_dir = dirs.opposite_direction(dir)
        if dest.has_exit(opp_dir):
            err_msg = err_msg % "The specified room already has an exit leading in the other direction."
            return False, err_msg

        self.db.exits[dir]["dest"] = dest.key
        dest.db.exits[opp_dir]["dest"] = self.key

        return True, ""

    def delete_exit(self, dir, oneway = False):
        err_msg = "Could not delete the exit. %s"
        dest, opp_dir = None, None

        if not self.has_exit(dir):
            err_msg = err_msg % f"There is no {dir}ward exit."
            return False, err_msg

        dest = get_room(self.exit_destination(dir))

        if dest and not oneway:
            opp_dir = dirs.opposite_direction(dir)
            if dest.has_exit(opp_dir):
                dest.reset_exit(opp_dir)

        self.reset_exit(dir)
        return True, ""

    def at_desc(self, looker=None, **kwargs):
        # Seems to process things before the room is looked at.
        pass

    def return_appearance(self, looker, **kwargs):
        if not looker:
            return ""

        # Grab all accessible objects in room.
        visible = (con for con in self.contents if con != looker and con.access(looker, "view"))
        exit_list = self.get_exits(visible_only = True)
        players, things = [], []

        for con in visible:
            # Get the content's name.
            key = con.get_display_name(looker)

            # If the content is a player, add to the players list.
            if con.has_account:
                # if con.account.is_superuser:
                #     users.append(f"|Y{key}|n")
                # else:
                players.append(f"{con.name}")

            else:
                # Goes into our generic list of items.
                things.append(con.db.long_desc)

        string = self.format_room_title()
        string += "\n%s" % Map(looker, max_width = 9, max_height = 9).draw_map()

        desc = self.description()
        if desc:
            desc = desc.replace("$p", "\n\n")
            desc = desc.replace("$n", "\n")

            if not self.db.insulated:
                desc = f"{self.get_temperature_string(looker)} {desc}"
            if not self.db.indoors:
                desc = f"{self.get_time_string(looker)} {desc}"

            string += f"\n{desc}"

        if things:
            for item in things:
                string += f" |c{item}|n"

        if players:
            for player in players:
                p_desc = f" |C{player} is here.|n"
                string += p_desc

        # string += "\n  %s" % self.get_illumination_string()
        if self.db.water_level > 0:
            string += "\n  %s" % self.get_water_level_string()

        exit_prepend = ""
        if looker.account.check_permstring("Developer"):
            exit_prepend = f"|124[{self.name}]|n "
        if exit_list:
            string += f"\n\n{exit_prepend}|235You see exits leading {list_to_string(exit_list)}|n."
        else:
            string += f"\n\n{exit_prepend}|235You see no exits.|n"

        return string

    def format_room_title(self):
        r_name = self.fullname()
        r_id = self.id
        r_id_zeroes = "0" * (4 - len(str(r_id)))

        r_area = self.areaname()
        r_zone = self.zonefullname()

        r_env = "|%s%s|n" % (self.environment_color(), self.environment_short())

        return f"|y{punctuate(r_name)}|n |213(|n|525{r_zone}, {r_area}|n|213)|n |x[|n{r_env}|x]|n |213(v|n|202{r_id_zeroes}|n|525{r_id}|n|213)|n"

    def fullname(self):
        return self.db.fullname if self.db.fullname else "Empty Room"

    def description(self):
        if self.db.desc and self.db.desc != "":
            return self.db.desc

        return "The space around you cannot be made sense of - the only concession to the mortal mind is that amidst the inchoate and swirling static that surrounds you, the visual noise underfoot is as solid as stone, serving as a \"floor.\" All around you is a relentless buzzing of junk data, and with it, the sound of an impossibly vast ocean, churning and hissing away into eternity."

    def get_temperature_string(self, ply):
        temp = self.db.temperature
        if ply.precision_information:
            return "|510The current temperature is %d C.|n" % temp
        else:
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

    def get_time_string(self, ply):
        now = datetime.now().time()
        if ply.precision_information:
            return now.strftime("|550The current time is %T.|n")
        else:
            if now.hour >= 0 and now.hour < 4:
                return "|103The moon hangs high in the sky.|n"
            elif now.hour >= 4 and now.hour < 6:
                return "|225A telltale bluish hue in the horizon tells of the oncoming dawn.|n"
            elif now.hour >= 6 and now.hour < 10:
                return "|431The sun begins to peek in the horizon.|n"
            elif now.hour >= 10 and now.hour < 12:
                return "|441Sunlight shines from the east as the Delight slowly climbs to its peak.|n"
            elif now.hour >= 12 and now.hour < 16:
                return "|550The Delight hangs at its peak, causing shadows to grow short.|n"
            elif now.hour >= 16 and now.hour < 18:
                return "|441The sky begins to darken as the sun falls to the west.|n"
            elif now.hour >= 18 and now.hour < 20:
                return "|225A smattering of stars join the moon in the sky.|n"
            elif now.hour >= 20 and now.hour < 23:
                return "|104Moonlight shines down upon you.|n"

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

        return self.db.zone.area_name()

    def areafullname(self):
        if not self.db.zone or not self.db.zone.area:
            return "An expanse of static"

        return self.db.zone.area_fullname()

    def set_zone(self, tar_zone):
        self.db.zone = tar_zone

    def zone(self):
        return self.db.zone

    def zonename(self):
        if not self.db.zone:
            return "Void"

        return self.db.zone.name

    def zonefullname(self):
        if not self.db.zone:
            return "The Void"

        return self.db.zone.fullname()

    def environment(self):
        return self.db.environment.name if self.db.environment else "????????"

    def environment_short(self):
        return self.db.environment.short() if self.db.environment else "?????"

    def environment_color(self):
        return self.db.environment.color() if self.db.environment else "500"

    @property
    def coordinates(self):
        return f"x{self.db.x}, y{self.db.y}, z{self.db.z}"


class ChargenRoom(Room):
    def at_object_creation(self):
        self.cmdset.add(ChargenCmdSet, permanent = True)

    def format_room_title(self):
        return header("Character Creation", color = "035", title_color = "055")

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