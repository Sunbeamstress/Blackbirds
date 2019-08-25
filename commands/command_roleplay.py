from evennia import Command as BaseCommand
from utilities.utils_string import RPFormat

class CmdEmote(BaseCommand):
    """
    Write an emote to express an action or set of actions your character is performing, whether to scratch their nose or to belt out a love song before an audience.

    Although your name must always be included in the message, the token |R@me|n can be used to determine where your name appears in the emote, enabling you finer control over the message's structure.

    |xUsage:|n
      |Rem <text>|n

    |xExample:|n
      |Rem rubs his stomach.|n

      |Rem Shaking out her hair, @me says, "Couldn't be better."|n

    The command will automatically capitalize the beginning and punctuate the ending of your emote, but care must be taken to ensure the rest of it is grammatically correct.
    """
    key = "pose"
    aliases = [":", "em", "me", "emote"]
    locks = "cmd:all()"

    def parse(self):
        """
        Custom parse the cases where the emote
        starts with some special letter, such
        as 's, at which we don't want to separate
        the caller's name and the emote with a
        space.
        """
        args = self.args
        if args and not args[0] in ["'", ",", ":"]:
            args = " %s" % args.strip()
        self.args = args

    def func(self):
        em_msg = self.args
        speech_mode = False # Toggle var to detect whether or not we're in the midst of speech.

        # Player supplied a blank emote.
        if not em_msg:
            msg = "|xSyntax:|n\n  |Rem <text>|n"
            self.caller.msg(msg)
            return

        # Only begin the emote with a name if @me wasn't used.
        if not "@me" in em_msg:
            # Did they capitalize the first letter? They may have meant to use a @me.
            if em_msg[1].isupper():
                self.caller.msg("Did you mean to include |R@me|n in your emote?")
                return

            # Prepend the emote with the player's name.
            em_msg = "%s%s" % (self.caller.name, em_msg)

        # Replace all @me tokens with our name.
        em_msg = em_msg.replace("@me", self.caller.name)

        em_msg = em_msg.strip()
        em_msg = RPFormat(em_msg)

        self.caller.msg("|xYou emote:|n")
        self.caller.location.msg_contents(text=(em_msg, {"type": "pose"}), from_obj=self.caller)