# Evennia modules.
from evennia import DefaultObject

# Blackbirds modules.
from utilities.string import jleft, jright

def environment_list():
    text = f"There are |W{Environment.objects.count()}|n environments defined in Blackbirds.\n"
    for env in Environment.objects.all():
        e_id = str(env.id)
        e_name = env.name
        e_short = env.short()
        e_color = env.color()

        text += "\n%s |c|||n |%s%s|g%s|n" % (jright(e_id, 5), e_color, jleft(e_short, 20), jleft(e_name, 32))

    return text

class Environment(DefaultObject):
    def at_object_creation(self):
        self.name = "Void"
        self.db.short = "void"
        self.db.color = "305"
        self.db.natural = False

    def update(self):
        pass

    def short(self):
        return self.db.short

    def color(self):
        return self.db.color

    def is_natural(self):
        return self.db.natural