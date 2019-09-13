# Blackbirds modules.
from commands.command import Command

class CmdNorthwest(Command):
    key = "northwest"
    aliases = ["nw"]
    def func(self):
        ply = self.caller
        ply.move_call("northwest")

class CmdNorth(Command):
    key = "north"
    aliases = ["n"]
    def func(self):
        ply = self.caller
        ply.move_call("north")

class CmdNortheast(Command):
    key = "northeast"
    aliases = ["ne"]
    def func(self):
        ply = self.caller
        ply.move_call("northeast")

class CmdWest(Command):
    key = "west"
    aliases = ["w"]
    def func(self):
        ply = self.caller
        ply.move_call("west")

class CmdEast(Command):
    key = "east"
    aliases = ["e"]
    def func(self):
        ply = self.caller
        ply.move_call("east")

class CmdSouthwest(Command):
    key = "southwest"
    aliases = ["sw"]
    def func(self):
        ply = self.caller
        ply.move_call("southwest")

class CmdSouth(Command):
    key = "south"
    aliases = ["s"]
    def func(self):
        ply = self.caller
        ply.move_call("south")

class CmdSoutheast(Command):
    key = "southeast"
    aliases = ["se"]
    def func(self):
        ply = self.caller
        ply.move_call("southeast")

class CmdUp(Command):
    key = "up"
    aliases = ["u"]
    def func(self):
        ply = self.caller
        ply.move_call("up")

class CmdDown(Command):
    key = "down"
    aliases = ["d"]
    def func(self):
        ply = self.caller
        ply.move_call("down")

class CmdIn(Command):
    key = "in"
    def func(self):
        ply = self.caller
        ply.move_call("in")

class CmdOut(Command):
    key = "out"
    def func(self):
        ply = self.caller
        ply.move_call("out")
