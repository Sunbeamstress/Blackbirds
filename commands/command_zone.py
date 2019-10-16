# Blackbirds modules.
from commands.command import Command
from utilities.menu import Menu
from utilities.utils_display import Line
from utilities.utils_string import jleft, jright

class CmdZone(Command):
    key = "zone"
    aliases = ["zones"]
    locks = "perm(Builder)"
    help_category = "Admin"

    def __init__(self):
        super().__init__()

    def func(self):
        Menu(self.caller, "menus.zone_admin", cmdset_mergetype = "Replace", cmd_on_exit = "look", startnode = "zone_admin_base")