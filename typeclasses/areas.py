# Evennia modules.
from evennia import DefaultObject

# Blackbirds modules.
from utilities.string import jleft, jright

def area_list():
    text = f"There are |W{Area.objects.count()}|n areas defined in Blackbirds.\n"
    for area in Area.objects.all():
        a_id = str(area.id)
        a_name = area.name
        a_fullname = area.fullname()
        a_is_city = str(area.is_city())
        a_pvp = str(area.open_pvp())

        text += "\n%s |c|||n %s|g%s|n" % (jright(a_id, 5), jleft(a_name, 20), jleft(a_fullname, 32))

    return text

class Area(DefaultObject):
    def at_object_creation(self):
        self.name = "Unnamed"
        self.db.fullname = "Unnamed Area"
        self.db.is_city = False
        self.db.open_pvp = False
        self.db.zones = []

    def fullname(self):
        return self.db.fullname

    def is_city(self):
        return self.db.is_city

    def open_pvp(self):
        return self.db.open_pvp

    def add_zone(self, zone):
        self.db.zones.add(zone)

    def remove_zone(self, zone):
        self.db.zones.remove(zone)

    def zones(self):
        return self.db.zones