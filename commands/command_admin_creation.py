# Evennia modules.
from evennia.utils import create

# Blackbirds modules.
from commands.command import Command
from utilities.characters import is_builder, is_admin
from utilities.menu import Menu

class CmdCreate(Command):
    key = "create"
    locks = "perm(Builder)"
    help_category = "Admin"

    def __init__(self):
        super().__init__()

    def func(self):
        ply = self.caller
        acc = self.caller.account

        obj_type = self.word(1)
        typeclass = None

        if obj_type != "object":
            ply.error_echo("Currently the only object class you can create is 'object.' More to come later.")
            return

        obj = create.create_object(typeclass, "null object", ply, home = ply.location, aliases = None, locks = None, report_to = ply)

        if not obj:
            ply.error_echo("Something went wrong in the creation of your new object.")
            return

        ply.echo("You create a null object, setting it spinning invisibly in the air.")

        # obj = create.create_object(
        #     typeclass,
        #     name,
        #     caller,
        #     home=caller,
        #     aliases=aliases,
        #     locks=lockstring,
        #     report_to=caller,
        # )
        # if not obj:
        #     continue

class CmdCreation(Command):
    key = "creation"
    locks = "perm(Builder)"
    help_category = "Admin"

    def __init__(self):
        super().__init__()

    def func(self):
        Menu(self.caller, "menus.creation_admin", cmdset_mergetype = "Replace", cmd_on_exit = "look", startnode = "creation_admin_base")