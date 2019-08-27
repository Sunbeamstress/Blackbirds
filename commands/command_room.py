"""
All commands related to getting or altering information about rooms.
"""

from commands.command import Command

def DescribeRoom(ply, room, description):
    room.db.desc = description
    ply.msg(f"`xRoom description changed. The room will now be described as:`n\n{room.db.desc}")

class CmdRoom(Command):
    """
    The following commands are used to build, edit, or otherwise manipulate rooms. In general, you may type any given subcommand by itself to see help and syntax information for each one.

    `xUsage:`n
      `Rroom info`n
    """
    key = "room"
    locks = "perm(Builder)"
    help_category = "Admin"

    def func(self):
        pass