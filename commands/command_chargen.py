# Blackbirds modules.
from commands.command import Command
from utilities.menu import Menu

class CmdChargenBegin(Command):
    key = "begin"

    def __init__(self):
        super().__init__()

    def func(self):
        Menu(self.caller, "menus.chargen", startnode = "chargen_base", cmdset_mergetype = "Replace", cmd_on_exit = "look")