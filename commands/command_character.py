"""
Commands that pertain to altering attributes and other states in regards to your character.
"""

from commands.command import Command

class CmdDescribe(Command):
    key = "describe"
    aliases = ["desc"]
    locks = "cmd:all()"

    def func(self):
        ply = self.caller
        arg = self.word(1)

        if not arg or arg != "self":
            ply.echo("|xUsage:|n\n  |Rdescribe self <description>|n")
            return

        ply.change_description(self.words(2))

class CmdScore(Command):
    key = "score"
    aliases = ["sc"]
    locks = "cmd:all()"

    def func(self):
        ply = self.caller
        ply.echo(ply.score())