# Blackbirds modules.
from commands.command import Command
from typeclasses.zones import Zone
from utilities.utils_display import Line
from utilities.utils_string import jleft, jright

def ZoneList(ply):
    zone = Zone()

    string = Line(80, "|y", "Zones", "|W")
    string += "\n   |222ID Full Name                       Short           Area|n"

    for i in range(len(zone)):
        z_name = zone.name(i)
        z_full = zone.fullname(i)
        z_area = zone.area_name(i)
        string += "\n|W%s|n|x:|n %s|x%s|n%s" % (jright(str(i), 4), jleft(z_full, 32), jleft(z_name, 16), z_area)

    string += "\n" + Line(80, "|y")

    ply.echo(string)

class CmdZone(Command):
    key = "zone"
    aliases = ["zones"]
    locks = "perm(Builder)"
    help_category = "Admin"

    def __init__(self):
        super().__init__()

        self.set_syntax_notes("The following commands produce various bits of information about zones in Blackbirds.")

        self.set_syntax("list", "See all defined zone types at a glance.")
        self.set_syntax("info <id>", "View a zone's detailed info.")

    def func(self):
        ply = self.caller
        sub = self.word(1)
        eid = self.word(2)

        if not sub:
            self.get_syntax()
            return

        if sub == "list":
            ZoneList(ply)
        elif sub == "info":
            ZoneInfo(ply, eid)
        else:
            self.get_syntax()