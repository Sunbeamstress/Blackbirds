from evennia import CmdSet
from commands.command_exit import *

class RoomLevelExitCmdSet(CmdSet):
    """
    Contains the Blackbirds-standard exit commands to move from room-to-room (north, south, etc.).

    This command set is room-level and will produce only "no direction" error messages, to be overwritten by exit-level commands.
    """
    key = "RoomLevelExitCommands"
    priority = 0

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        self.add(CmdInvalidExit())

class ExitCmdSet(CmdSet):
    """
    Contains the Blackbirds-standard exit commands to move from room-to-room (north, south, etc.).

    This command set is exit-level and is designed to override identical commands on the room level.
    """
    key = "ExitCommands"
    priority = 1

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        # self.add(CmdNorth())