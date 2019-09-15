# Evennia modules.
from evennia import DefaultObject

class Exit(DefaultObject):
    def at_object_creation(self):
        self.db.open = True
        self.db.locked = False
        self.db.blocked = False
        self.db.visible = True

        self.source = None
        self.destination = None

    def open(self):
        self.db.open = True

    def close(self):
        self.db.open = False

    def is_open(self):
        return self.db.open

    def lock(self):
        self.db.locked = True

    def unlock(self):
        self.db.locked = False

    def is_locked(self):
        return self.db.locked

    def block(self):
        self.db.blocked = True

    def unblock(self):
        self.db.blocked = False

    def is_blocked(self):
        return self.db.blocked

    def hide(self):
        self.db.visible = False

    def show(self):
        self.db.visible = True

    def is_visible(self):
        return self.db.visible

    def source(self):
        return self.source

    def set_source(self, new_source = None):
        self.source = new_source

    def destination(self):
        return self.destination

    def set_destination(self, new_destination = None):
        self.destination = new_destination



# """
# Exits
# 
# Exits are connectors between Rooms. An exit always has a destination property
# set and has a single command defined on itself with the same name as its key,
# for allowing Characters to traverse the exit to its destination.
# 
# """
# from evennia import DefaultExit

# class Exit():
#     """
#     Exits are connectors between rooms. Exits are normal Objects except
#     they defines the `destination` property. It also does work in the
#     following methods:

#      basetype_setup() - sets default exit locks (to change, use `at_object_creation` instead).
#      at_cmdset_get(**kwargs) - this is called when the cmdset is accessed and should
#                               rebuild the Exit cmdset along with a command matching the name
#                               of the Exit object. Conventionally, a kwarg `force_init`
#                               should force a rebuild of the cmdset, this is triggered
#                               by the `@alias` command when aliases are changed.
#      at_failed_traverse() - gives a default error message ("You cannot
#                             go there") if exit traversal fails and an
#                             attribute `err_traverse` is not defined.

#     Relevant hooks to overload (compared to other types of Objects):
#         at_traverse(traveller, target_loc) - called to do the actual traversal and calling of the other hooks.
#                                             If overloading this, consider using super() to use the default
#                                             movement implementation (and hook-calling).
#         at_after_traverse(traveller, source_loc) - called by at_traverse just after traversing.
#         at_failed_traverse(traveller) - called by at_traverse if traversal failed for some reason. Will
#                                         not be called if the attribute `err_traverse` is
#                                         defined, in which case that will simply be echoed.
#     """
#     pass