"""
Commands that pertain to altering attributes and other states in regards to your character.
"""

from commands.command import Command

class CmdDescribe(Command):
    key = "describe"
    aliases = ["desc"]
    locks = "cmd:all()"

    def func(self):
        if not self.args or self.word(1) != "self":
            self.caller.msg("|xUsage:|n\n  |Rdescribe self <description>|n")
            return

        description = self.words(2)
        self.caller.db.desc = description

        self.caller.msg(f"|xDescription changed. You will now be described as:|n\n{self.caller.db.desc}")