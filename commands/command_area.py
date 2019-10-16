# Blackbirds modules.
from commands.command import Command
from utilities.menu import Menu

class CmdArea(Command):
    key = "area"
    aliases = ["areas"]
    locks = "perm(Builder)"
    help_category = "Admin"

    def __init__(self):
        super().__init__()

    def func(self):
        Menu(self.caller, "menus.area_admin", cmdset_mergetype = "Replace", cmd_on_exit = "look", startnode = "area_admin_base")