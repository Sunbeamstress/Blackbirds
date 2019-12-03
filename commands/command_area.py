# Blackbirds modules.
from commands.command import Command
from typeclasses.areas import area_list
from utilities.menu import Menu

class CmdArea(Command):
    key = "area"
    locks = "perm(Builder)"
    help_category = "Admin"

    def __init__(self):
        super().__init__()

    def func(self):
        Menu(self.caller, "menus.area_admin", cmdset_mergetype = "Replace", cmd_on_exit = "look", startnode = "area_admin_base")

class CmdAreas(Command):
    key = "areas"
    locks = "perm(Builder)"
    help_category = "Admin"

    def __init__(self):
        super().__init__()

    def func(self):
        self.caller.echo(area_list())