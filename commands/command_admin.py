# IRE-like administration commands, aka my effort to get out of MUXland.

from commands.command import Command
from evennia.server.sessionhandler import SESSIONS

from utilities.utils_display import Notify

class CmdRoom(Command):
    """
    The following commands are used to build, edit, or otherwise manipulate rooms. In general, you may type any given subcommand by itself to see help and syntax information for each one.

    |xUsage:|n
      |Rroom info|n
    """
    key = "room"
    locks = "perm(Builder)"
    help_category = "Admin"

    def func(self):
        pass

class CmdReload(Command):
    """
    reload the server

    Usage:
      reload [reason]

    This restarts the server. The Portal is not
    affected. Non-persistent scripts will survive a reload (use
    reset to purge) and at_reload() hooks will be called.
    """
    key = "reload"
    aliases = ['restart']
    locks = "cmd:perm(reload) or perm(Developer)"
    help_category = "System"

    def func(self):
        """
        Reload the system.
        """
        reason = ""
        if self.args:
            reason = "%s" % self.args.rstrip(".")
        SESSIONS.announce_all(Notify("Game", f"The system is reloading{reason}, please be patient."))
        SESSIONS.portal_restart_server()

# class CmdClassUpdate(Command):
#   """
#   Updates all instances of a given character class.
#   """
#   key = "cupdate"
#   locks = "perm(Developer)"
#   help_category = "Admin"

#   def func(self):
#     if not self.args:
#       self.caller.msg("You must specify a valid object class to update.")
#       return

#     if self.args.lower() == "character" or self.args.lower() == "characters":
#       char.at_object_creation() for char in Character.objects
#       self.caller.msg("All characters updated.")