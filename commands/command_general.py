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

class CmdSay(Command):
    """
    Say something aloud for other players to hear.

    |xUsage:|n
      |Rsay <message>|n

    You can be heard by almost anyone in the room, as well as people who happen to be nearby and listening in.
    """

    key = "say"
    aliases = ['"', "'"]
    locks = "cmd:all()"

    def func(self):
        ply = self.caller

        if not self.args:
            ply.msg("You must specify something to say!")
            return

        speech = self.args
        if not speech:
            return

        # Call any code that might fire before speaking - e.g. voice disguising, etc.
        speech = ply.at_before_say(speech)

        # Process player speech.
        ply.at_say(speech, msg_self = True)

        # Post-processing for things such as hypnotic suggestion, coded phrases, and more.
        ply.at_after_say(speech)