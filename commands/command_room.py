"""
All commands related to getting or altering information about rooms.
"""

from commands.command import Command

def DescribeRoom(ply, room, description):
    room.db.desc = description
    ply.msg(f"|xRoom description changed. The room will now be described as:|n\n{room.db.desc}")

def RoomInfo(ply, tar_room = None):
    pass

def RoomRename(ply, tar_room = None):
    pass

def RoomRedescribe(ply, tar_room = None):
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

    def func(self):
        ply = self.caller
        sub = self.word(1)
        tar_room = self.word(2)

        # Display syntax if used by itself - or if the subcommand isn't found.
        if not sub:
            self.get_syntax()
            return

        # Determine valid subcommand by argument.
        if sub == "info":
            RoomInfo(ply, tar_room)
        elif sub == "name":
            RoomRename(ply, tar_room)
        elif sub == "desc":
            RoomRedescribe(ply, tar_room)
        else:
            self.get_syntax()