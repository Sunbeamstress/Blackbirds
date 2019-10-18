"""
Commands to manipulate or learn about abilities.

The ability's commands themselves are not implemented here.
"""

from commands.command import Command
from utilities.display import header
from utilities.string import jright

class CmdAbilities(Command):
    key = "abilities"
    aliases = ["ab", "skills", "sk", "ability"]
    locks = "cmd:all()"

    def func(self):
        ply = self.caller
        headers = {"Might":"Strength", "Acuity":"Vision", "Dexterity":"Agility"}

        ply.echo(header(80, "|m", "Abilities", "|M"))
        for h, a in headers.items():
            ply.echo(f"\n\n  |C{h}:|n 1\n|c{jright(a, 16)}|n: 1")
        ply.echo("\n")
        ply.echo(header(80, "|m"))