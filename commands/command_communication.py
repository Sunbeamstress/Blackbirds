# Evennia modules.
from commands.command import Command

# Blackbirds modules.
from utilities.accounts import all_accounts, all_accounts_limited
from utilities.display import formatted_channel_msg
from utilities.string import jleft, jright, truncate, autoformat

class Channel(Command):
    def __init__(self):
        super().__init__()
        self.no_prompt = True
        self.speaker_color = "x"
        self.chan_color = "w"
        self.use_account_names = True

    def broadcast(self, chan, msg, speaker, ply_list):
        _ = [p.echo(self.formatted_channel_msg(chan = chan, speaker = speaker, msg = autoformat(msg)), prompt = True) for p in ply_list]

    def formatted_channel_msg(self, chan = None, speaker = None, msg = None, chan_color = None):
        if not chan or not speaker or not msg:
            return

        acc = speaker if self.use_account_names else speaker.account
        speaker_color = "W" if acc.is_superuser else self.speaker_color
        chan_color = chan_color if chan_color else self.chan_color

        if self.use_account_names:
            speaker = acc.name
        else:
            # For now, just uses the character's name, but this can be used for fun extensibility later.
            pass

        return f"|=j[|=o{chan}|=j]|n |{speaker_color}{speaker}:|{chan_color} {msg}"

class CmdNewbieChannel(Channel):
    key = "newbie"
    aliases = ["newb", "nt"]
    locks = "cmd:all()"

    def func(self):
        msg = self.words(1)
        acc = self.caller.account

        self.broadcast("Newbie", msg, self.caller.account, all_accounts())

class CmdAdminChannel(Channel):
    key = "admin"
    aliases = ["at"]
    locks = "perm(Builder)"

    def func(self):
        ply = self.caller
        msg = self.words(1)

        self.speaker_color = "520"
        self.chan_color = "410"

        self.broadcast("Admin", msg, self.caller.account, all_accounts_limited("Builder"))