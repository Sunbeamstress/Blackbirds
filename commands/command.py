"""
Commands

Commands describe the input the account can do to the game.

"""
# Python modules.
import textwrap

# Evennia modules.
from evennia import Command as BaseCommand
# from evennia import default_cmds

# Blackbirds modules.
from utilities.string import (jright, jleft)


class Command(BaseCommand):
    """
    Inherit from this if you want to create your own command styles
    from scratch.  Note that Evennia's default commands inherits from
    MuxCommand instead.

    Note that the class's |__doc__` string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    Each Command implements the following methods, called
    in this order (only func() is actually required):
        - at_pre_cmd(): If this returns anything truthy, execution is aborted.
        - parse(): Should perform any extra parsing needed on self.args
            and store the result on self.
        - func(): Performs the actual work.
        - at_post_cmd(): Extra actions, often things done after
            every command, like prompts.

    """
    def __init__(self):
        # Maintain out-of-the-box Evennia command structure.
        super().__init__()

        # Add Blackbirds-custom command variables.
        self.cmd_word = []
        self._syntax_pre_note = None
        self._syntax_post_note = None
        self._syntax_subcmds = {}

        self.uses_balance = False
        self.needs_balance = False
        self.balance_time = 0
        self.balance_mod = 0
        self.no_prespacing = False
        self.no_prompt = False

    def at_pre_cmd(self):
        # Check to see if this command requires balance, first.
        if self.needs_balance and not self.caller.db.balance:
            self.caller.error_echo("You cannot act yet.", prompt = True)
            return True

        # Space out everything between prompts - looks nice.
        if not self.no_prespacing:
            self.caller.echo("\n")

    def parse(self):
        # Process user's input, divide into words - used for various word-based getter functions below.
        cmd = (self.cmdstring + self.args).split()
        self.cmd_word = cmd.copy()

    def at_post_cmd(self):
        # Use balance, if applicable.
        bt = self.balance_time + self.balance_mod
        bt = 0 if bt < 0 else bt
        if self.uses_balance and self.balance_time > 0:
            self.caller.use_balance(self.balance_time)

        # Every command sends a prompt afterwards.
        if not self.no_prompt:
            self.caller.msg(prompt = self.caller.prompt())

        self.balance_mod = 0

    def echo(self, string, prompt = False, error = False):
        ply = self.caller
        ply.echo(string = string, error = error, prompt = prompt)

    def error_echo(self, string, prompt = False):
        ply = self.caller
        ply.error_echo(string = string, prompt = prompt)

    def word_count(self):
        """
        Usage: self.word_count()

        Returns total number of words in entered command.
        """
        return len(self.cmd_word)

    def words(self, start = 0, end = 0):
        """
        Usage: self.words(start, end)

        Gets the specified range of words in the entered command.
        """
        if not start:
            return ""

        if not end:
            end = len(self.cmd_word)

        separator = " "
        return separator.join(self.cmd_word[start:end])

    def word(self, w = 0):
        """
        Usage: self.word(word num)

        Gets the specified word from the entered command.
        """
        if w < 0 or (w > len(self.cmd_word) - 1):
            return ""

        return self.cmd_word[w]

    def get_syntax(self):
        """
        Usage: self.get_syntax()

        Used in conjunction with self.set_syntax(subcmd, desc) and self.set_syntax_notes(note). Displays command syntax to the player in a unified fashion.
        """
        ply = self.caller
        string = ""

        wrapper = textwrap.TextWrapper()
        wrapper.width = 80
        wrapper.subsequent_indent = " " * 26

        if self._syntax_pre_note:
            string += self._syntax_pre_note + "\n"

        for subcmd, desc in self._syntax_subcmds.items():
            wrapper.initial_indent = "|R%s|n " % jleft("  " + subcmd, 25)
            subcmd_string = wrapper.wrap(desc)
            for line in subcmd_string:
                string += "\n" + line

        if self._syntax_post_note:
            string += "\n\n" + self._syntax_post_note

        ply.echo(string)

    def set_syntax(self, subcmd, desc):
        self._syntax_subcmds[subcmd] = desc

    def set_syntax_notes(self, note, post = None):
        if post:
            self._syntax_post_note = note
        else:
            self._syntax_pre_note = note