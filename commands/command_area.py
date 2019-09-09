# Blackbirds modules.
from commands.command import Command
from typeclasses.areas import Area
from utilities.utils_display import Line
from utilities.utils_string import jleft, jright

def AreaList(ply):
    area = Area()

    string = Line(80, "|y", "Areas", "|W")
    string += "\n   |222ID Full Name                       Short           City  Warzone|n"

    for i in range(len(area)):
        a_name = area.name(i)
        a_full = area.fullname(i)
        a_is_city = "No"
        a_is_open_pvp = "No"
        if area.is_city(i):
            a_is_city = "|WYes|n"
        if area.is_open_pvp(i):
            a_is_open_pvp = "|WYes|n"
        string += "\n|W%s|n|x:|n %s|x%s|n%s%s" % (jright(str(i), 4), jleft(a_full, 32), jleft(a_name, 16), jleft(a_is_city, 6!), a_is_open_pvp)

    string += "\n" + Line(80, "|y")

    ply.echo(string)

class CmdArea(Command):
    key = "area"
    aliases = ["areas"]
    locks = "perm(Builder)"
    help_category = "Admin"

    def __init__(self):
        super().__init__()

        self.set_syntax_notes("The following commands produce various bits of information about areas in Blackbirds.")

        self.set_syntax("list", "See all defined area types at a glance.")
        self.set_syntax("info <id>", "View an area's detailed info.")

    def func(self):
        ply = self.caller
        sub = self.word(1)
        eid = self.word(2)

        if not sub:
            self.get_syntax()
            return

        if sub == "list":
            AreaList(ply)
        elif sub == "info":
            AreaInfo(ply, eid)
        else:
            self.get_syntax()