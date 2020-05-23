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

from evennia import default_cmds, CmdSet

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
from commands.command_map import *
from commands.command_chargen import *


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
        self.add(CmdEnvironments())
        self.add(CmdArea())
        self.add(CmdAreas())
        self.add(CmdZone())
        self.add(CmdZones())
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
        self.add(CmdMap())
        self.add(CmdTest())
        self.add(CmdSpeciesChange())
        self.add(CmdSetHp())
        self.add(CmdScore())
        self.add(CmdPronounChange())
        self.add(CmdUpdate())
        self.add(CmdList())
        self.add(CmdGoto())
        self.add(CmdDelete())
        self.add(CmdInflect())
        self.add(CmdColors())
        self.add(CmdBody())
        self.add(CmdRelocate())

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

class ChargenCmdSet(CmdSet):
    key = "Chargen"
    # If it turns out it's just too much of a pain in the ass to let players have their default commands.
    # If used, need to add commands such as help, look, etc. to this command set.
    # mergetype = "Replace"

    # <Griatch> A nice way to do this is to make a catch-all override Command. Just make a command that you add to that cmdset with aliases for all the commands you want to block, and let the Command.func just echo an error message.
    # <Griatch> There are CmdSet mergetypes to filter out commands too, should it come to that, but a catch-all Command is nice in that you can make a nicer error message (like "you cannot use that command while in chargen" or something)

    def at_cmdset_creation(self):
        self.add(CmdChargenBegin())