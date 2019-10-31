"""
Commands to manipulate or learn about abilities.

The ability's commands themselves are not implemented here.
"""

import sys, inspect

from commands.command import Command
from typeclasses.abilities import Ability, AbilityTree
from utilities.display import header, divider
from utilities.string import jright

class CmdAbilities(Command):
    key = "abilities"
    aliases = ["ab", "skills", "sk", "ability"]
    locks = "cmd:all()"

    def func(self):
        ply = self.caller

        for i in dir(abilities.core_stats):
            ply.echo(f"i: {i}, getattr: {getattr(abilities.core_stats, i)}")