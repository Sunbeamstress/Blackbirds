# Blackbirds modules.
from commands.command import Command
from typeclasses.zones import zone_list
from utilities.menu import Menu

class CmdZone(Command):
    key = "zone"
    locks = "perm(Builder)"
    help_category = "Admin"

    def __init__(self):
        super().__init__()

    def func(self):
        Menu(self.caller, "menus.zone_admin", cmdset_mergetype = "Replace", cmd_on_exit = "look", startnode = "zone_admin_base")

class CmdZones(Command):
    key = "zones"
    locks = "perm(Builder)"
    help_category = "Admin"

    def __init__(self):
        super().__init__()

    def func(self):
        self.caller.echo(zone_list())