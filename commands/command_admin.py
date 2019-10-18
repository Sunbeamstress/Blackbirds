# IRE-like administration commands, aka my effort to get out of MUXland.

from evennia.server.sessionhandler import SESSIONS
from evennia.utils import search

from commands.command import Command
from utilities.display import notify
from utilities.menu import Menu
from typeclasses.zones import Zone
from typeclasses.species import Human, Carven, Sacrilite, Luum, Idol

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
        "Reload the system."
        reason = ""
        if self.args:
            reason = "%s" % self.args.rstrip(".")
        SESSIONS.announce_all(notify("Game", f"The system is reloading{reason}, please be patient."))
        SESSIONS.portal_restart_server()

class CmdMakeAdmin(Command):
    """
    Gives the targetted account admin privileges.

    |xUsage:|n
      |Rmakeadmin <account>|n
    """
    key = "makeadmin"
    locks = "perm(<Superuser>)"
    def func(self):
        ply = self.caller
        # tar = search.account_search(self.word(1))
        if not self.args:
            ply.echo("You must specify the name of an account.")
            return

        tar = search.account_search(self.word(1))[0]
        if not tar:
            ply.echo("No account by that name could be found.")
            return

        ply.echo(f"Ding! Your target account is: {tar}")
        # tar.cmdset.add(default_cmds.AdminCmdSet, permanent = True)


class CmdTest(Command):
    key = "test"
    locks = "perm(Admin)"

    def func(self):
        pass
        # Menu(self.caller, "menus.testmenu", cmdset_mergetype = "Replace", cmd_on_exit = "look", startnode = "node_test", debug = True)

class CmdSpeciesChange(Command):
    key = "specieschange"
    aliases = ["specchange"]
    locks = "perm(Admin)"

    def func(self):
        ply = self.caller
        species = self.word(1).lower()
        if species == "human":
            ply.db.species = Human()
            ply.echo("Species changed to Human.")
        elif species == "carven":
            ply.db.species = Carven()
            ply.echo("Species changed to Carven.")
        elif species == "sacrilite":
            ply.db.species = Sacrilite()
            ply.echo("Species changed to Sacrilite.")
        elif species == "luum":
            ply.db.species = Luum()
            ply.echo("Species changed to Luum.")
        elif species == "idol":
            ply.db.species = Idol()
            ply.echo("Species changed to Idol.")
        else:
            ply.error_echo("That is not a valid species name.")