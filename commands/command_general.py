from commands.command import Command

class CmdLook(Command):
    """
    If entered with no arguments, shows you the current room, vehicle, or container you happen to be in. If used with an argument, will attempt to look at certain specific things.

    |xUsage:|n
      |Rlook|n
      |Rlook <player>|n
      |Rlook <player> <clothing/held item>|n
    """
    key = "look"
    aliases = ["l"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """
        Handle the looking.
        """
        caller = self.caller

        self.args = self.args.strip()

        # If no target specified, default to looking at the room.
        if not self.args:
            target = caller.location
            if not target:
                caller.msg("|xYou can see nothing.|n")
                return

        else:
            if self.args.strip() == "me" or self.args.strip() == "self":
                target = caller
            else:
                target = caller.search(self.args)
            if not target:
                return

        self.msg((caller.at_look(target), {'type': 'look'}), options=None)