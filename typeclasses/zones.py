# Evennia modules.
from evennia import DefaultObject

# Blackbirds modules.
from utilities.utils_string import jleft, jright

def zone_list():
    text = f"There are |W{Zone.objects.count()}|n zones defined in Blackbirds.\n"
    for zone in Zone.objects.all():
        z_id = str(zone.id)
        z_name = zone.name
        z_fullname = zone.fullname()
        z_area = str(zone.area())
        z_pvp = str(zone.open_pvp())

        text += "\n%s |c|||n %s|g%s|n" % (jright(z_id, 5), jleft(z_name, 20), jleft(z_fullname, 32))

    return text

class Zone(DefaultObject):
    def at_object_creation(self):
        self.name = "Unnamed"
        self.db.fullname = "Unnamed Zone"
        self.db.area = 0
        self.db.open_pvp = False
        self.db.rooms = []

    def fullname(self):
        return self.db.fullname

    def area(self):
        return self.db.area

    def open_pvp(self):
        return self.db.open_pvp

    def add_room(self, room):
        self.db.rooms.add(room)

    def remove_room(self, room):
        self.db.rooms.remove(room)

    def rooms(self):
        return self.db.rooms