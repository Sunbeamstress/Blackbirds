"""
Command sets

All commands in the game must be grouped in a cmdset.  A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.

"""

from evennia import default_cmds
from commands.command_roleplay import *
from commands.command_general import *
from commands.command_character import *
from commands.command_admin import *
from commands.command_room import *
from commands.command_ability import *
from commands.command_environment import *
from commands.command_area import *
from commands.command_zone import *
from commands.command_movement import *
from commands.command_account import *


class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
    """
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()

        self.add(CmdEmote())
        self.add(CmdLook())
        self.add(CmdSay())
        self.add(CmdDescribe())
        self.add(CmdAbilities())
        self.add(CmdStand())
        self.add(CmdSit())
        self.add(CmdLie())
        self.add(CmdWho())
        self.add(CmdRoom())
        self.add(CmdReload())
        self.add(CmdEnvironment())
        self.add(CmdArea())
        self.add(CmdZone())

        self.add(CmdNorthwest())
        self.add(CmdNorth())
        self.add(CmdNortheast())
        self.add(CmdWest())
        self.add(CmdEast())
        self.add(CmdSouthwest())
        self.add(CmdSouth())
        self.add(CmdSoutheast())
        self.add(CmdUp())
        self.add(CmdDown())
        self.add(CmdIn())
        self.add(CmdOut())

class AdminCmdSet(default_cmds.CharacterCmdSet):
    key = "DefaultAdmin"
    def at_cmdset_creation(self):
        super().at_cmdset_creation()

        # self.add(CmdRoom())
        # self.add(CmdReload())
        # self.add(CmdClassUpdate())

class AccountCmdSet(default_cmds.AccountCmdSet):
    """
    This is the cmdset available to the Account at all times. It is
    combined with the `CharacterCmdSet` when the Account puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """
    key = "DefaultAccount"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        self.add(CmdChar())


class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.  This
    holds commands like creating a new account, logging in, etc.
    """
    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in. It
    is empty by default.
    """
    key = "DefaultSession"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        As and example we just add the empty base `Command` object.
        It prints some info.
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
