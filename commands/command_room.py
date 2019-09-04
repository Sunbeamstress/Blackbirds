"""
All commands related to getting or altering information about rooms.
"""

from commands.command import Command
from utilities.utils_display import Line

def DescribeRoom(ply, room, description):
    room.db.desc = description
    ply.echo(f"|xRoom description changed. The room will now be described as:|n\n{room.db.desc}")

def RoomInfo(ply, tar_room = None):
    # add logic to search for and get info on tar_room instead here

    r_name = tar_room.name
    r_id = tar_room.id
    r_id_str = "#" + str(tar_room.id)
    r_env = tar_room.db.environment
    r_temp = tar_room.db.temperature

    string = Line(80, "|y", f"{r_id_str}, {r_name}", "|W")

    string += f"\n       Name |c|||n {r_name}"
    string += f"\n       Area |c|||n |xNYI|n"
    string += f"\nEnvironment |c|||n {r_env}"
    string += f"\nTemperature |c|||n {r_temp}"

    string += "\n" + Line(80, "|y")

    ply.echo(string)

def RoomRename(ply, tar_room = None, new_name = None):
    if not new_name or new_name == "":
        ply.echo("You must specify a name for the room.")
        return

    ply.echo(new_name)
    r_id = tar_room.id
    r_id_str = "#" + str(tar_room.id)
    previous_name = tar_room.name
    tar_room.name = new_name
    ply.echo(f"Room {r_id_str}'s name has been changed from {previous_name} to {tar_room.name}.")

def RoomRedescribe(ply, tar_room = None):
    pass

def RoomTemperature(ply, tar_room = None):
    pass

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

        self.set_syntax_notes("The |Rroom|w command is a fully-featured suite of commands to make, delete, or otherwise manipulate rooms to your liking. As such, the command by itself does nothing. Refer to each subcommand below for further information.")

        self.set_syntax("info", "Displays a useful breakdown of the current room and its attributes.")
        self.set_syntax("name <name>", "Change the room's name.")
        self.set_syntax("desc <description>", "Change the room's description.")
        self.set_syntax("temp <temperature>", "Change the room's temperature.")

    def func(self):
        ply = self.caller
        sub = self.word(1)
        tar_room = self.word(2)
        args = self.words(3, self.word_count())

        # Display syntax if used by itself - or if the subcommand isn't found.
        if not sub:
            self.get_syntax()
            return

        # All commands default to current room if none is specified.
        if not tar_room or tar_room == "here":
            tar_room = ply.location

        # Determine valid subcommand by argument.
        if sub == "info":
            RoomInfo(ply, tar_room)
        elif sub == "name" or sub == "rename":
            RoomRename(ply, tar_room, args)
        elif sub == "desc" or sub == "description":
            RoomRedescribe(ply, tar_room)
        elif sub == "temp" or sub == "temperature":
            RoomTemperature(ply, tar_room)
        else:
            self.get_syntax()