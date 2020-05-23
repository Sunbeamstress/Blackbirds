# Evennia modules.
from commands.command import Command

# Blackbirds modules.
from utilities.accounts import all_accounts
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
        ply = self.caller
        ply_list = all_accounts()

        form_msg = f'|y[Newbie]:|n {ply} says, "{autoformat(msg)}"'

        for p in ply_list:
            p.echo(form_msg, prompt = True)