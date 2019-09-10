# Blackbirds modules.
from commands.command import Command

class CmdInvalidExit(Command):
    """
    Special command stored on the room object - serves only to return an invalid exit message.

    Overridden by valid exit commands on exit objects.
    """
    key = "northwest"
    aliases = ["nw", "north", "n", "northeast", "ne", "west", "w", "east", "e", \
               "southwest", "sw", "south", "s", "southeast", "se", "in", "out", "up", \
               "u", "down", "d"]
    def func(self):
        ply = self.caller

        ply.echo("|xThere is no exit in that direction.|n")

class CmdValidExit(Command):
    """
    Generic command to handle player movement, stored on exit-objects. Sets player's location to appropriate room.
    """
    key = "northwest"
    aliases = ["nw", "north", "n", "northeast", "ne", "west", "w", "east", "e", \
               "southwest", "sw", "south", "s", "southeast", "se", "in", "out", "up", \
               "u", "down", "d"]
    def func(self):
        ply = self.caller

        ply.echo("|RDing! This works. It doesn't do anything, but it works.|n")