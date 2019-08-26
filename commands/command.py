"""
Commands

Commands describe the input the account can do to the game.

"""

from evennia import Command as BaseCommand
# from evennia import default_cmds


class Command(BaseCommand):
    """
    Inherit from this if you want to create your own command styles
    from scratch.  Note that Evennia's default commands inherits from
    MuxCommand instead.

    Note that the class's `__doc__` string (this text) is
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
        super().__init__()
        self.cmd_word = []

    def at_pre_cmd(self):
        self.caller.msg("\n")

    def parse(self):
        cmd = (self.cmdstring + self.args).split()
        self.cmd_word = cmd.copy()

    def at_post_cmd(self):
        HP, MP, END, WIL = 500, 500, 1500, 1500
        prompt = f"|cH:|n{HP} |cM:|n{MP} |cE:|n{END} |cW:|n{END} |x-|n "
        self.caller.msg(prompt=prompt)

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