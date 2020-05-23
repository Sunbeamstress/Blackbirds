# Evennia modules.
from commands.command import Command

# Blackbirds modules.
from utilities.accounts import all_accounts
from utilities.display import formatted_channel_msg
from utilities.string import jleft, jright, truncate, autoformat

class CmdNewbie(Command):
    key = "newbie"
    aliases = ["newb", "nt"]
    locks = "cmd:all()"

    def __init__(self):
        super().__init__()

        self.no_prompt = True

    def func(self):
        msg = self.words(1)
        acc = self.caller.account
        acc_color = "Y" if acc.is_superuser else "w"

        ply_list = all_accounts()
        for p in ply_list:
            p.echo(formatted_channel_msg(chan = "Newbie", acc = acc, msg = autoformat(msg)), prompt = True)