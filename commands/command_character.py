"""
Commands that pertain to altering attributes and other states in regards to your character.
"""

from commands.command import Command
from commands.command_room import DescribeRoom

def DescribeCharacter(ply, description):
    ply.db.desc = description
    ply.echo(f"|xDescription changed. You will now be described as:|n\n{ply.db.desc}")

class CmdDescribe(Command):
    key = "describe"
    aliases = ["desc"]
    locks = "cmd:all()"

    def func(self):
        ply = self.caller

        if not self.args or (not self.word(1) in ["self", "here", "room"]):
            ply.echo("|xUsage:|n\n  |Rdescribe self <description>|n")
            return

        description = self.words(2)

        if self.word(1) == "self":
            DescribeCharacter(self.caller, description)
        elif self.word(1) == "here" or self.word(1) == "room":
            room = self.caller.location
            DescribeRoom(self.caller, room, description)

class CmdScore(Command):
    key = "score"
    aliases = ["sc"]
    locks = "cmd:all()"

    def func(self):
        ply = self.caller
        ply.echo(ply.score())