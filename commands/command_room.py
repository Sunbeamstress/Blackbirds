# Evennia modules.
from evennia.utils import create

# Blackbirds modules.
from commands.command import Command
from server.conf import settings
from typeclasses.environments import Environment
from typeclasses.zones import Zone
from utilities.directions import valid_direction, coord_shift
from utilities.display import header, divider
from utilities.room import sanitize_roomname, inc_roomname, roomname_exists
from utilities.string import jleft, jright
import utilities.directions as dirs

VALID_ROOM_VALUES = ("temperature", "illumination", "water_level")
VALID_ROOM_FLAGS = ("indoors", "darkness", "natural", "public", "shop", "house", "battleground", "craft_hall", "chapel", "bank")

def room_info_entry(attr_name, nice_value, var_name, type_reminder, cust_str_color = "W"):
    translated_value = "|c---|n"

    if type(nice_value) is bool:
        if nice_value == True:
            translated_value = "|YYes|n"
        elif nice_value == False:
            translated_value = "|rNo|n"
    elif type(nice_value) is int:
        if nice_value >= 0:
            translated_value = "|W" + str(nice_value) +"|n"
        elif nice_value == 0:
            translated_value = "|x0|n"
    elif type(nice_value) is str:
        translated_value = f"|{cust_str_color}{nice_value}|n"

    string = "\n%s" % (jright(attr_name, 16))
    string += " |c|||n "
    string += "%s" % (jleft(translated_value, 24))
    string += "|x%s|n" % var_name
    string += " |x[%s]|n" % type_reminder
    return string

def room_info(ply, tar_room = None):
    # add logic to search for and get info on tar_room instead here
    r_name = tar_room.fullname()
    r_id = tar_room.id
    r_id_str = "#" + str(tar_room.id)

    r_zone = tar_room.zonename()

    env_name = tar_room.environment()
    env_color = tar_room.environment_color()

    string = header(f"{r_id_str}, {r_name}", color = "y")

    string += room_info_entry("Name", tar_room.name, "name", "str")
    string += room_info_entry("Zone", r_zone, "zone", "id")
    string += room_info_entry("Environment", env_name, "environment", "id", env_color)
    string += room_info_entry("Insulated", tar_room.db.insulated, "insulated", "bool")
    string += room_info_entry("Temperature", tar_room.db.temperature, "temperature", "num")
    string += room_info_entry("Indoors", tar_room.db.indoors, "indoors", "bool")
    string += room_info_entry("Illumination", tar_room.db.illumination, "illumination", "0-15")
    string += room_info_entry("Water Level", tar_room.db.water_level, "water_level", "0-15")

    string += "\n"

    string += room_info_entry("Darkness", tar_room.db.darkness, "darkness", "bool")
    string += room_info_entry("Natural", tar_room.db.natural, "natural", "bool")
    string += room_info_entry("Public", tar_room.db.public, "public", "bool")
    string += room_info_entry("Shop", tar_room.db.shop, "shop", "bool")
    string += room_info_entry("House", tar_room.db.house, "house", "bool")
    string += room_info_entry("Battleground", tar_room.db.battleground, "battleground", "bool")
    string += room_info_entry("Craft Hall", tar_room.db.craft_hall, "craft_hall", "bool")
    string += room_info_entry("Chapel", tar_room.db.chapel, "chapel", "bool")
    string += room_info_entry("Bank", tar_room.db.bank, "bank", "bool")

    string += "\n"

    string += room_info_entry("Powered", tar_room.db.powered, "powered", "bool")
    string += room_info_entry("Power Sink", tar_room.db.power_sink, "power_sink", "bool")
    string += room_info_entry("Radio Tower", tar_room.db.radio_tower, "radio_tower", "bool")
    string += room_info_entry("Neon Well", tar_room.db.neon_well, "neon_well", "bool")

    string += "\n"

    string += room_info_entry("Player Owned", tar_room.db.player_owned, "player_owned", "bool")
    string += room_info_entry("Owning Player", tar_room.db.player_owner_id, "player_owner_id", "bool")

    string += "\n" + divider(color = "y")

    ply.echo(string)

def room_create(ply, dir = None):
    # Get information from the player's current room.
    orig = ply.location
    r_name = inc_roomname(orig.name)
    r_zone = orig.db.zone
    r_env = orig.db.environment
    r_powned = orig.db.player_owned
    r_pid = orig.db.player_owner_id
    r_x, r_y, r_z = orig.db.x, orig.db.y, orig.db.z

    # Make sense of our supplied direction.
    dir = valid_direction(dir)

    if dir and orig.has_exit(dir):
        ply.error_echo("This room already has an exit in that direction.")
        return

    # Create the room.
    typeclass = settings.BASE_ROOM_TYPECLASS
    new_room = create.create_object(typeclass, r_name, report_to = ply)
    if r_zone:
        new_room.db.zone = r_zone
        r_zone.add_room(new_room)
    new_room.db.environment = r_env
    new_room.db.player_owned = r_powned
    new_room.db.player_owner_id = r_pid

    dir_append = ""
    if dir:
        # Manipulate coordinates if a direction is supplied.
        new_x, new_y, new_z = coord_shift(dir)
        r_x += new_x
        r_y += new_y
        r_z += new_z

        # Build the appropriate exits.
        orig.create_exit(dir, new_room)
        dir_append = f", {dir} from your current location"

    new_room.db.x, new_room.db.y, new_room.db.z = r_x, r_y, r_z

    ply.echo(f"You created a new room, {r_name}{dir_append} ({new_room.coordinates}).")

def room_shortname(ply, tar_room = None, new_name = None):
    if not new_name or new_name == "":
        ply.error_echo("You must specify an ID for the room.")
        return

    previous_name = tar_room.name
    new_name = sanitize_roomname(new_name)

    if roomname_exists(new_name):
        ply.error_echo("That room ID is already in use.")
        return

    tar_room.name = new_name
    ply.echo(f"You change the ID of the current room from |x{previous_name}|n to |x{new_name}|n.")

def room_rename(ply, tar_room = None, new_name = None):
    if not new_name or new_name == "":
        ply.error_echo("You must specify a name for the room.")
        return

    r_id = tar_room.name
    previous_name = tar_room.db.fullname
    tar_room.db.fullname = new_name
    ply.echo(f"Room {r_id}'s name has been changed from {previous_name} to {tar_room.fullname()}.")

def room_redescribe(ply, tar_room = None, new_desc = None):
    if tar_room:
        if new_desc.lower() in ("none", "clear", "empty", "erase", "wipe"):
            tar_room.db.desc = ""
            ply.echo("Room description cleared.")
        else:
            tar_room.db.desc = new_desc
            ply.echo(f"Room description changed. The room will now be described as:|n\n|x{tar_room.description()}|n")

def room_environment(ply, tar_room = None, new_env = None):
    if not new_env:
        ply.error_echo("You must specify an environment by number. See |Renvironment list|n for all current environments.")
        return

    try:
        eid = int(new_env)
    except ValueError:
        ply.error_echo("You must enter a number.")
        return

    env = ply.search("#" + new_env, global_search = True)
    if not env:
        ply.error_echo("That is not a valid environment.")
        return

    tar_room.db.environment = env

    r_id = tar_room.id
    r_name = tar_room.name
    ply.echo(f"You set room #{r_id}, {r_name}, to use the |{tar_room.environment_color()}{tar_room.environment()}|n environment.")

def room_create_exit(ply, tar_room = None, dir = None, dest = None):
    if not dir:
        ply.error_echo("You must specify a direction.")
        return

    if not dirs.valid_direction(dir):
        ply.error_echo("You must supply a valid direction.")
        return

    destination = ply.search(dest, global_search = True)
    if not destination:
        ply.error_echo("That does not appear to be a valid room.")
        return

    full_dir = dirs.valid_direction(dir)
    e, err_msg = tar_room.create_exit(full_dir, destination)
    if not e:
        ply.echo(err_msg)
        return

    ply.echo(f"You create a {full_dir}ward exit to room {dest}, {destination.name}.")

def room_delete_exit(ply, tar_room = None, dir = None):
    if not dir:
        ply.error_echo("You must specify a direction.")
        return

    if not dirs.valid_direction(dir):
        ply.error_echo("You must supply a valid direction.")
        return

    full_dir = dirs.valid_direction(dir)
    e, err_msg = tar_room.delete_exit(full_dir)
    if not e:
        ply.error_echo(err_msg)
        return

    ply.echo(f"You delete the {full_dir}ward exit.")

def room_shift(ply, tar_room = None, dir = None):
    if not dir:
        ply.error_echo("You must specify a direction.")
        return

    if not dirs.valid_direction(dir):
        ply.error_echo("You must supply a valid direction.")
        return

    full_dir = dirs.valid_direction(dir)
    r_x, r_y, r_z = coord_shift(dir)

    tar_room.db.x += r_x
    tar_room.db.y += r_y
    tar_room.db.z += r_z
    ply.echo(f"You shift the room to the {dir} ({tar_room.coordinates}).")

def room_zone(ply, tar_room = None, zone = None):
    if not zone:
        ply.error_echo("You must specify a zone.")
        return

    tar_zone = ply.search("#" + zone, global_search = True)
    if not tar_zone:
        ply.error_echo(f"No zone with the id {zone} could be found.")
        return

    if tar_room.zone():
        z = tar_room.zone()
        z.remove_room(tar_room)

    tar_room.set_zone(tar_zone)
    tar_zone.add_room(tar_room)

    ply.echo(f"Set the room's zone to |W{tar_zone.name}|n.")

def room_value(ply, tar_room = None, val_name = None, val = None):
    if not val_name:
        ply.error_echo("Which room property are you trying to modify?")
        return

    if not val:
        ply.error_echo("You must specify a value to set that room property to.")
        return

    try:
        val = int(val)
    except ValueError:
        ply.error_echo("You may only set that room property to a number.")
        return

    if val_name == "temperature" and not -294 < val < 10000:
        ply.error_echo("You can only set the temperature to a number between -293 and 10000.")
        return
    elif val_name != "temperature" and (val < 0 or val > 15):
        ply.error_echo("You can only set that room property to a number between 0 and 15.")
        return

    if getattr(tar_room.db, val_name) == None:
        ply.error_echo("That room doesn't seem to have the property you're trying to modify.")
        return

    setattr(tar_room.db, val_name, val)
    ply.echo(f"You set {tar_room.name}'s {val_name} to {str(val)}.")

def room_flag(ply, tar_room = None, flag_name = None, flag = None):
    flag = flag.lower()

    if not flag_name:
        ply.error_echo("Which room property are you trying to modify?")
        return

    if flag and (flag != "true" and flag != "false"):
        ply.error_echo("You may only set that property to true or false.")
        return

    if getattr(tar_room.db, flag_name) == None:
        ply.error_echo("That room doesn't seem to have the property you're trying to modify.")
        return

    if not flag:
        setattr(tar_room.db, flag_name, not getattr(tar_room.db, flag_name))
        # tar_room.db[flag_name] = not tar_room.db[flag_name]
    elif flag == "true":
        setattr(tar_room.db, flag_name, True)
    elif flag == "false":
        setattr(tar_room.db, flag_name, False)

    ply.echo(f"You set {tar_room.name}'s {flag_name} to {str(getattr(tar_room.db, flag_name))}.")

class CmdRoom(Command):
    """
    The following commands are used to build, edit, or otherwise manipulate rooms. In general, you may type any given subcommand by itself to see help and syntax information for each one.

    |xUsage:|n
      |Rroom info|n
    """
    key = "room"
    locks = "perm(Builder)"
    help_category = "Admin"

    def __init__(self):
        super().__init__()

        self.set_syntax_notes("The |Rroom|n command is a fully-featured suite of commands to make, delete, or otherwise manipulate rooms to your liking. As such, the command by itself does nothing. Refer to each subcommand below for further information.")

        self.set_syntax("info", "Displays a useful breakdown of the current room and its attributes.")
        self.set_syntax("name <room> <name>", "Change the room's name.")
        self.set_syntax("desc <room> <description>", "Change the room's description.")
        self.set_syntax("temp <room> <temperature>", "Change the room's temperature.")
        self.set_syntax("env <room> <environment>", "Change the room's environmental type.")
        self.set_syntax("link <dir> <destination>", "Add a new exit to the desired room.")
        self.set_syntax("unlink <dir>", "Remove an exit from the room.")

        self.set_syntax_notes("By default, the |Rroom|n command will affect changes to your current room. You may optionally supply a room yourself by entering its ID after the command.\n\n|xExample:|n\n  |Rroom link south #3|n\n  |Rroom #6 link south #3|n", True)

    def func(self):
        ply = self.caller
        tar_room = ply.location
        shift, sub_cmd, args = 0, None, None

        if not self.word(1):
            self.get_syntax()
            return

        # Check first to see if the player is supplying a room.
        search_room = ply.search(self.word(1), global_search = True, quiet = True)

        if search_room:
            tar_room = search_room[0]
            shift = 1
        elif self.word(1) == "here":
            shift = 1

        # Choose which word to find our subcommand from based on whether or not we supplied a room.
        # Without:
        #   > room link n #6
        # With:
        #   > room #3 link n #6
        sub_cmd = self.word(1 + shift)
        args = self.words(2 + shift, self.word_count())

        # Display syntax if used by itself - or if the subcommand isn't found.
        if not sub_cmd:
            self.get_syntax()
            return

        # Helper for common subcommand shortenings.
        sub_cmd = "temperature" if sub_cmd == "temp" else sub_cmd

        # Determine valid subcommand by argument.
        if sub_cmd == "info":
            room_info(ply, tar_room)
        elif sub_cmd in ("create", "make", "new"):
            room_create(ply, args)
        elif sub_cmd in ("id", "shortname", "godname"):
            room_shortname(ply, tar_room, args)
        elif sub_cmd in ("name", "rename"):
            room_rename(ply, tar_room, args)
        elif sub_cmd in ("desc", "description"):
            room_redescribe(ply, tar_room, args)
        elif sub_cmd in ("env", "environment"):
            room_environment(ply, tar_room, args)
        elif sub_cmd == "link":
            room_create_exit(ply, tar_room, self.word(2 + shift), self.word(3 + shift))
        elif sub_cmd == "unlink":
            room_delete_exit(ply, tar_room, args)
        elif sub_cmd in ("move", "shift"):
            room_shift(ply, tar_room, args)
        elif sub_cmd == "zone":
            room_zone(ply, tar_room, args)
        elif sub_cmd in VALID_ROOM_VALUES:
            # Generic function to set numeric room values.
            room_value(ply, tar_room, sub_cmd, args)
        elif sub_cmd in VALID_ROOM_FLAGS:
            # Generic function to toggle boolean room values.
            room_flag(ply, tar_room, sub_cmd, args)
        else:
            self.get_syntax()