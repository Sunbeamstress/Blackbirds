# Blackbirds modules.
from commands.command import Command
from typeclasses.environments import environment_list
from utilities.menu import Menu

class CmdEnvironment(Command):
    key = "environment"
    aliases = ["env"]
    locks = "perm(Builder)"
    help_category = "Admin"

    def __init__(self):
        super().__init__()

    def func(self):
        Menu(self.caller, "menus.environment_admin", cmdset_mergetype = "Replace", cmd_on_exit = "look", startnode = "environment_admin_base")

class CmdEnvironments(Command):
    key = "environments"
    aliases = ["envs"]
    locks = "perm(Builder)"
    help_category = "Admin"

    def __init__(self):
        super().__init__()

    def func(self):
        self.caller.echo(environment_list())