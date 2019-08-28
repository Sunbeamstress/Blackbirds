import time
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import utils

from commands.command import Command
from utilities.utils_string import (jleft, jright)
from utilities.utils_display import Line

class CmdLook(Command):
    """
    If entered with no arguments, shows you the current room, vehicle, or container you happen to be in. If used with an argument, will attempt to look at certain specific things.

    `xUsage:`n
      `Rlook`n
      `Rlook <player>`n
      `Rlook <player> <clothing/held item>`n
    """
    key = "look"
    aliases = ["l"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """
        Handle the looking.
        """
        caller = self.caller

        self.args = self.args.strip()

        # If no target specified, default to looking at the room.
        if not self.args:
            target = caller.location
            if not target:
                caller.msg("`xYou can see nothing.`n")
                return

        else:
            if self.args.strip() == "me" or self.args.strip() == "self":
                target = caller
            else:
                target = caller.search(self.args)
            if not target:
                return

        self.msg((caller.at_look(target), {'type': 'look'}), options=None)

class CmdSay(Command):
    """
    Say something aloud for other players to hear.

    `xUsage:`n
      `Rsay <message>`n

    You can be heard by almost anyone in the room, as well as people who happen to be nearby and listening in.
    """

    key = "say"
    aliases = ['"', "'"]
    locks = "cmd:all()"

    def func(self):
        ply = self.caller

        if not self.args:
            ply.msg("You must specify something to say!")
            return

        speech = self.args
        if not speech:
            return

        # Call any code that might fire before speaking - e.g. voice disguising, etc.
        speech = ply.at_before_say(speech)

        # Process player speech.
        ply.at_say(speech, msg_self = True)

        # Post-processing for things such as hypnotic suggestion, coded phrases, and more.
        ply.at_after_say(speech)

class CmdSit(Command):
    """
    Cause your character to sit down. Can optionally specify a bit of furniture to sit on.

    `xUsage:`n
      `Rsit`n
      `Rsit <furniture>`n

    Naturally, you cannot move while seated.
    """
    key = "sit"
    locks = "cmd:all()"

    def func(self):
        ply = self.caller

        if ply.db.prone >= 2:
            ply.db.prone = 1
            ply.msg("You shift up into a seated position.")
        elif ply.db.prone == 0:
            ply.db.prone = 1
            ply.msg("You sit down.")
        else:
            ply.msg("You are already seated.")

class CmdStand(Command):
    """
    If seated or lying down, stand up.

    `xUsage:`n
      `Rstand`n
    """
    key = "stand"
    locks = "cmd:all()"

    def func(self):
        ply = self.caller

        if ply.db.prone == 0:
            ply.msg("You are already standing.")
            return

        ply.db.prone = 0
        ply.msg("You stand up.")

class CmdLie(Command):
    """
    Lie down on the ground. Alternatively, you may specify a piece of furniture to lie on.

    `xUsage:`n
      `Rlie`n
      `Rlie <furniture>`n

    Naturally, you cannot move while lying down. Note that in most cases, you will be considered vulnerable while prone!
    """
    key = "lie"
    aliases = ["lay"]
    locks = "cmd:all()"

    def func(self):
        ply, prone = self.caller, self.caller.db.prone

        if prone >= 2:
            ply.msg("You are already lying down.")
            return

        if prone == 1:
            ply.db.prone = 2
            ply.msg("You ease down onto the ground.")
        elif prone == 0:
            ply.db.prone = 2
            ply.msg("You lie down.")

class CmdWho(Command):
    """
    See who's currently online.

    `xUsage:`n
      `Rwho`n

    Note that you may not be able to see certain people who have taken efforts to conceal themselves.
    """

    key = "who"
    locks = "cmd:all()"

    def func(self):
        """
        Get all connected accounts by polling session.
        """

        account = self.account
        session_list = SESSIONS.get_sessions()
        session_list = sorted(session_list, key = lambda o: o.account.key)

        self.msg(Line(80, "`m", "Currently Online", "`w"))
        self.msg("  `xNAME`n                         `xONLINE FOR`n   `xIDLE FOR`n")

        for session in session_list:
            if not session.logged_in:
                continue

            puppet = session.get_puppet()
            if not puppet:
                continue

            naccounts = SESSIONS.account_count()

            location = puppet.location.key if puppet and puppet.location else ""
            p_name = puppet.get_display_name(account)
            
            idle = utils.time_format(time.time() - session.cmd_last_visible, 1)
            conn = utils.time_format(time.time() - session.conn_time, 0)

            self.msg("  %s%s    %s" % (jleft(p_name, 32), jright(conn, 7), jright(idle, 7)))
            self.msg("  `c%s`n" % (location))

        self.msg("\n\n  `W%s`n `xunique account%s logged in.`n" % (naccounts, "" if naccounts == 1 else "s"))

        self.msg(Line(80, "`m"))