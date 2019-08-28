"""
Commands to manipulate or learn about abilities.

The ability's commands themselves are not implemented here.
"""

from commands.command import Command
from utilities.utils_display import Line
from utilities.utils_string import jright

class CmdAbilities(Command):
    key = "abilities"
    aliases = ["ab", "skills", "sk", "ability"]
    locks = "cmd:all()"

    def func(self):
        ply = self.caller
        headers = {"Might":"Strength", "Acuity":"Vision", "Dexterity":"Agility"}

        ply.msg(Line(80, "|m", "Abilities", "|M"))
        for h, a in headers.items():
            ply.msg(f"\n\n  |C{h}:|n 1\n|c{jright(a, 16)}|n: 1")
        ply.msg("\n")
        ply.msg(Line(80, "|m"))