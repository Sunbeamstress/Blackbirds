# Blackbirds modules.
from commands.command import Command
from typeclasses.environments import Environment
from utilities.display import header
from utilities.string import jleft, jright

def EnvironmentList(ply):
    env = Environment()

    string = header(80, "|y", "Environments", "|W")
    string += "\n   |222ID Name                    Short  Natural|n"

    for i in range(len(env)):
        e_name = env.name(i)
        e_short = env.shortname(i)
        e_is_natural = "No"
        e_color = env.color(i)
        if env.is_natural(i):
            e_is_natural = "|WYes|n"
        string += "\n|W%s|n|x:|n |%d%s|n|x%s|n%s" % (jright(str(i), 4), e_color, jleft(e_name, 24), jleft(e_short, 7), e_is_natural)

    string += "\n" + header(80, "|y")

    ply.echo(string)

class CmdEnvironment(Command):
    key = "environment"
    aliases = ["env"]
    locks = "perm(Builder)"
    help_category = "Admin"

    def __init__(self):
        super().__init__()

        self.set_syntax_notes("The following commands produce various bits of information about environments in Blackbirds.")

        self.set_syntax("list", "See all defined environment types at a glance.")
        self.set_syntax("info <id>", "View an environment's detailed info.")

    def func(self):
        ply = self.caller
        sub = self.word(1)
        eid = self.word(2)

        if not sub:
            self.get_syntax()
            return

        if sub == "list":
            EnvironmentList(ply)
        elif sub == "info":
            EnvironmentInfo(ply, eid)
        else:
            self.get_syntax()