from commands.command import Command
from utilities.room import room_characters
from utilities.string import autoformat

class CmdEmote(Command):
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

    def __init__(self):
        super().__init__()
        self.uses_balance = True
        self.needs_balance = True
        self.balance_time = 1
        self.no_prompt = True

    def parse(self):
        """
        Custom parse the cases where the emote
        starts with some special letter, such
        as 's, at which we don't want to separate
        the caller's name and the emote with a
        space.
        """
        super().parse()
        args = self.args
        if args and not args[0] in ["'", ",", ":"]:
            args = " %s" % args.strip()
        self.args = args

    def func(self):
        ply = self.caller
        em_msg = self.args
        speech_mode = False # Toggle var to detect whether or not we're in the midst of speech.

        # Player supplied a blank emote.
        if not em_msg:
            ply.echo("|xSyntax:|n\n  |Rem <text>|n")
            return

        # Only begin the emote with a name if @me wasn't used.
        if not "@me" in em_msg:
            # Did they capitalize the first letter? They may have meant to use a @me.
            if em_msg[1].isupper():
                ply.echo("Did you mean to include |R@me|n in your emote?")
                return

            # Prepend the emote with the player's name.
            em_msg = "%s%s" % (self.caller.name, em_msg)

        # Remove superfluous whitespace.
        em_msg = em_msg.strip()

        # Replace all @me tokens with our name.
        em_msg = em_msg.replace("@me", self.caller.name)

        # Pass entire emote through formatter to auto-capitalize and punctuate.
        em_msg = autoformat(em_msg)

        # Speech detection:
        if '"' in em_msg:
            new_em_msg = []
            temp = em_msg.split('"')
            for segment in temp:
                if speech_mode:
                    new_em_msg.append('|C"%s"|n' % segment)
                else:
                    new_em_msg.append(segment)
                speech_mode = not speech_mode

            em_msg = ''.join(new_em_msg)

        # Give out XP/Rubric, if applicable.
        self.grant_rewards(em_msg)

        # Send the message out!
        ply.echo("|xYou emote:|n")
        ply.location.echo(em_msg, type = "emote", origin = ply, prompt = True)

    def grant_rewards(self, msg):
        ply = self.caller
        room = ply.location
        ply_list = room_characters(room)
        ply_count = len(ply_list)
        ply_targets = 0

        if len(msg) < 16:
            return

        if not ply_count or ply_count == 0:
            return

        # XP Formula:
        # 1 XP per character in emote
        xp_score = len(msg)
        # A bonus of 15% of the base value for each unique player targetted in the emote.
        xp_ply_target_bonus = (xp_score * 0.15) * ply_targets

        new_xp = xp_score + xp_ply_target_bonus

        # Rubric is fixed currently at 1% of XP gain.
        new_rb = new_xp * 0.01

        ply.db.xp["current"] += new_xp
        ply.account.db.rubric += new_rb
        ply.echo(f"|yYour emote generated {new_xp} experience and {new_rb} Rubric.|n")