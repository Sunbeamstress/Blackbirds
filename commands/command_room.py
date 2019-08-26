"""
All commands related to getting or altering information about rooms.
"""

from commands.command import Command

def DescribeRoom(ply, room, description):
    room.db.desc = description
    ply.msg(f"|xRoom description changed. The room will now be described as:|n\n{room.db.desc}")