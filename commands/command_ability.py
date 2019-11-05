"""
Commands to manipulate or learn about abilities.

The ability's commands themselves are not implemented here.
"""

from abilities.trees import *
from commands.command import Command
from typeclasses.abilities import AbilityTree
from utilities.display import header, divider
from utilities.string import jleft, jright

class CmdAbilities(Command):
    key = "abilities"
    aliases = ["ab", "skills", "sk", "ability"]
    locks = "cmd:all()"

    def func(self):
        ply = self.caller

        ply.echo(header("Abilities", color = "c", title_color = "M"))

        for tree in ply.db.abilities.values():
            tree_level = "||" * tree.level()
            tree_buffer = "||" * (tree.max_level() - tree.cur_level())
            ply.echo(f"\n  |C{tree_level}|012{tree_buffer}|n |W{tree.name()}|n")

            for ab in tree.get_abilities():
                ab_level = "||" * ab.cur_level()
                ab_buffer = "||" * (ab.max_level() - ab.cur_level())
                ply.echo(f"\n{' ' * 13}|C{ab_level}|012{ab_buffer}|n |W{ab.name()}|n")

        ply.echo(divider(color = "c"))