# Evennia modules.
from commands.command import Command

# Blackbirds modules.
from utilities.string import jleft, jright, truncate

class CmdDescribe(Command):
    key = "describe"
    aliases = ["desc"]
    locks = "cmd:all()"

    def func(self):
        ply = self.caller
        bodypart = self.word(1)
        desc = self.words(2)

        if not ply.has_bodypart(bodypart):
            ply.error_echo("That doesn't seem to be the name of a body part you can modify. Type |RBODY|x to see the complete list.")
            return

        if not desc or desc == "":
            ply.error_echo("You'll need to specify a description for that part. If you want to clear it, try |RDESC <bodypart> CLEAR|x.")
            return

        ply.change_description(bodypart, self.words(2))

class CmdScore(Command):
    key = "score"
    aliases = ["sc"]
    locks = "cmd:all()"

    def func(self):
        ply = self.caller
        ply.echo(ply.score())

class CmdBody(Command):
    key = "body"

    def func(self):
        ply = self.caller
        ply.echo("You take a moment to appraise your own body.")

        for i in ply.db.body:
            desc = ply.bodypart_desc(i).replace("\n", "")
            ply.echo(f"\n|x{jright(i, 4)}|n {jleft(ply.bodypart_name(i), 16)} |x{truncate(desc, 52)}|n")