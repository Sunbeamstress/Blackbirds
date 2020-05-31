import time
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import utils

from commands.command import Command
from utilities.string import (jleft, jright)
from utilities.display import header, divider, color_chart
from utilities.targetting import find_living_target

class CmdPunch(Command):
    key = "punch"

    def __init__(self):
        super().__init__()
        self.needs_balance = True
        self.uses_balance = True
        self.balance_time = 4

    def func(self):
        ply = self.caller
        tar = find_living_target(ply, self.word(1))

        if not tar:
            ply.error_echo("You cannot see that person here.")
            return

        ply.echo(f"You cock back your fist and sock {tar} in the gut.")
        tar.damage(1, f"{ply} cocks back {ply.their()} fist and socks you in the gut.")