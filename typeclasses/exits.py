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

    def __str__(self):
        return self.destination

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

    def get_source(self):
        return self.source

    def set_source(self, new_source):
        self.source = new_source

    def get_destination(self):
        return self.destination

    def set_destination(self, new_destination):
        self.destination = new_destination