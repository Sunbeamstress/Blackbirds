# Python modules.
import inspect, sys, inflect, re

# Evennia modules.
from evennia.server.sessionhandler import SESSION_HANDLER
from evennia.utils import search
from evennia.utils.utils import mod_import, variable_from_module, class_from_module

# Blackbirds modules.
from abilities.core_stats import *
from abilities.misc import *

from commands.command import Command

from data import visibility as vis

from utilities.abilities import ability_list
from utilities.classes import class_from_name
from utilities.debugging import debug_echo
from utilities.display import notify, bullet, header, divider, gecho
from utilities.menu import Menu
from utilities.room import inc_roomname, get_room

from server.conf import settings

from typeclasses.abilities import Ability
from typeclasses.accounts import Account
from typeclasses.areas import Area
from typeclasses.characters import Character
from typeclasses.environments import Environment
from typeclasses.species import Species, Human, Carven, Sacrilite, Luum, Idol, Blackbird
from typeclasses.zones import Zone

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
        SESSION_HANDLER.announce_all(notify("Game", f"The system is reloading{reason}, please be patient."))
        SESSION_HANDLER.portal_restart_server()

class CmdUpdate(Command):
    key = "update"
    locks = "perm(Developer)"
    help_category = "Admin"

    def func(self):
        ply = self.caller

        obj_type = self.word(1)
        valid_objs = ("accounts", "rooms", "characters", "environments", "zones", "areas", "species")

        if not obj_type:
            ply.error_echo("You must specify a Python class to update. Valid classes are:")
            for o in valid_objs:
                ply.echo(bullet(o))
            return

        obj_type = obj_type.lower()

        if obj_type == "accounts":
            for o in Account.objects.all():
                o.update()
        elif obj_type == "rooms":
            Room = class_from_module(settings.BASE_ROOM_TYPECLASS)
            for o in Room.objects.all():
                o.update()
        elif obj_type == "characters":
            for o in Character.objects.all():
                o.update()
        elif obj_type == "environments":
            for o in Environment.objects.all():
                o.update()
        elif obj_type == "zones":
            for o in Zone.objects.all():
                o.update()
        elif obj_type == "areas":
            for o in Area.objects.all():
                o.update()
        elif obj_type == "species":
            for o in Species.objects.all():
                o.update()
        else:
            ply.error_echo("You must specify a Python class to update. Valid classes are:")
            for o in valid_objs:
                ply.echo(bullet(o))
            return

        ply.echo(f"All |W{obj_type}|n have been updated.")

class CmdList(Command):
    key = "list"
    locks = "perm(Developer)"

    def func(self):
        ply = self.caller
        obj_type = self.word(1)
        obj_list = []
        valid_objs = ("accounts", "rooms", "characters", "environments", "zones", "areas", "species")

        if obj_type not in valid_objs:
            ply.error_echo("You must specify a valid Python class to list. Valid classes are:")
            for o in valid_objs:
                ply.echo(bullet(o))
            return

        if obj_type == "rooms":
            obj_list = [o for o in class_from_module(settings.BASE_ROOM_TYPECLASS).objects.all()]
        else:
            # To-do: make this less ghetto as all hell
            d_o = obj_type[:-1] if obj_type != "species" else "species" # quick depluralizing of obj_type
            obj_list = [o for o in class_from_name("typeclasses." + obj_type, d_o.capitalize()).objects.all()]

        ply.echo(header(obj_type.capitalize()))

        for o in obj_list:
            ply.echo(bullet(f"{o.name}"))

        ply.echo(divider())

class CmdTest(Command):
    key = "test"
    locks = "perm(Admin)"

    def __init__(self):
        super().__init__()
        self.uses_balance = False
        self.needs_balance = False
        self.balance_time = 0

    def func(self):
        ply = self.caller
        arg = self.words(1)
        acc = ply.account
        debug_echo(str(acc.character))

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
        elif species == "blackbird":
            ply.db.species = Blackbird()
            ply.echo("Species changed to Blackbird.")
        else:
            ply.error_echo("That is not a valid species name.")

class CmdSetHp(Command):
    key = "sethp"
    locks = "perm(Admin)"

    def func(self):
        ply = self.caller
        hp = self.word(1)
        if not hp.isnumeric():
            ply.error_echo("Use a number, ding-dong.")
            return

        ply.db.hp["current"] = int(hp)
        ply.echo(f"You set your HP to |G{hp}|n.")

class CmdPronounChange(Command):
    key = "pronounchange"
    aliases = ["prochange"]
    locks = "perm(Admin)"

    def func(self):
        ply = self.caller
        pronoun_set = self.word(1)

        if pronoun_set in ["1", "he", "male", "m"]:
            ply.db.pronoun_they = "he"
            ply.db.pronoun_them = "him"
            ply.db.pronoun_their = "his"
            ply.db.pronoun_theirs = "his"
        elif pronoun_set in ["2", "she", "female", "f"]:
            ply.db.pronoun_they = "she"
            ply.db.pronoun_them = "her"
            ply.db.pronoun_their = "her"
            ply.db.pronoun_theirs = "hers"
        elif pronoun_set in ["3", "plural", "t"]:
            ply.db.pronoun_they = "they"
            ply.db.pronoun_them = "them"
            ply.db.pronoun_their = "their"
            ply.db.pronoun_theirs = "theirs"
        elif pronoun_set in ["4", "neuter", "genderless", "n", "g"]:
            ply.db.pronoun_they = "it"
            ply.db.pronoun_them = "it"
            ply.db.pronoun_their = "its"
            ply.db.pronoun_theirs = "its"
        else:
            ply.error_echo("Please choose from the following values:\n  1, 2, 3, 4\n  he, she, plural, neuter\n  male, female, genderless  \n  m, f, t, n/g")
            return

        ply.echo(f"Your pronouns have been set to {ply.pronouns()}.")

class CmdGoto(Command):
    key = "go"
    aliases = ["goto", "tel", "tele", "teleport"]
    locks = "perm(Admin)"

    def func(self):
        ply = self.caller
        tar = self.word(1)
        loc = None

        if tar in ("chargen", "intro", "newbie"):
            tar = settings.START_LOCATION
        elif tar in ("deletion", "trash"):
            tar = settings.DELETION_ROOM
        elif tar in ("admin", "satellite", "pools"):
            tar = settings.ADMIN_ROOM

        dest = ply.search(tar, global_search = True)
        if not dest:
            self.error_echo("No player, object, or room by that name was found.")
            return

        # Target is not a room - try to get their location.
        if dest.has_account:
            loc = dest.location
            if not loc:
                self.error_echo("That target does not seem to have a room you can teleport to.")
                return
        else:
            loc = dest

        # Continue as normal.
        if ply.move_to(loc, quiet = True, move_msg = f"You fling yourself through spacetime, and halt abruptly at {loc.fullname()}."):
            pass
        else:
            self.error_echo("Teleportation failed.")

class CmdRelocate(Command):
    key = "rel"
    aliases = ["reloc", "relocate"]
    locks = "perm(Admin)"

    def func(self):
        ply = self.caller
        tar = self.word(1)
        loc = self.word(2)

        if loc in ("chargen", "intro", "newbie"):
            loc = settings.START_LOCATION
        elif loc in ("deletion", "trash"):
            loc = settings.DELETION_ROOM
        elif tar in ("admin", "satellite", "pools"):
            loc = settings.ADMIN_ROOM

        tar = ply.search(tar, global_search = True)
        if not tar:
            self.error_echo("No player by that name was found.")
            return

        if not tar.has_account:
            self.error_echo("That is not a valid player.")
            return

        loc = ply.search(loc, global_search = True)
        if not loc:
            self.error_echo("No location by that name was found.")
            return

        # Continue as normal.
        if tar.move_to(loc, quiet = True, move_msg = f"You find yourself flung instantly through time and space, arriving at {loc.fullname()}."):
            ply.echo(f"You make a beckoning gesture at {tar}, flinging {tar.them()} through time and space to {loc.fullname()}.")
            pass
        else:
            self.error_echo("Relocation failed.")

class CmdDelete(Command):
    key = "delete"
    aliases = ["del"]
    locks = "perm(Admin)"

    def func(self):
        ply = self.caller
        tar = self.word(1)

        # If the target is a player or object, send it to the deletion room. Everything else is removed the normal way.
        tar = ply.search(tar, global_search = True)

        if not tar:
            self.error_echo("There doesn't appear to be anything by that name to delete.")
            return

        if tar.__class__.__name__ == "Room":
            self.echo(f"You delete {tar.__class__.__name__} #{tar.id}.")
            tar.delete()
            return

        tar.location = ply.search(settings.DELETION_ROOM, global_search = True)
        self.echo(f"You send {tar.name} (#{tar.id}) to deletion for processing.")

class CmdInflect(Command):
    key = "inflect"
    aliases = ["inf"]
    locks = "perm(Developer)"

    def iecho(self, string):
        self.caller.echo(f"|c[|CInflect|c]:|n {string}")

    def func(self):
        ply = self.caller
        arg = self.word(1)
        string = self.words(2)

        inf = inflect.engine()
        inf.classical()

        if arg == "plural":
            self.iecho(inf.plural(string))
        elif arg == "pluraladj" or arg == "plural_adj":
            self.iecho(inf.plural_adj(string))

class CmdAdminHide(Command):
    "Invisibility beyond anything even a Blackbird could inspire to. Silently phase in or out of perfect, total illusiveness."
    key = "ahide"
    aliases = ["adminhide"]
    locks = "perm(Admin)"

    def func(self):
        ply = self.caller
        s_level = ply.db.visibility

        if s_level < vis.ADMIN:
            ply.db.visibility = vis.ADMIN
            ply.echo("You go totally invisible.")
        else:
            ply.db.visibility = vis.NORMAL
            ply.echo("You emerge from your total invisibility.")