from evennia.utils import logger, search
from commands.command import Command

class CmdChar(Command):
    def __init__(self):
        super().__init__()

        self.set_syntax("create", "Create a new character. This will use one slot.")
        self.set_syntax("delete <name>", "Delete a character. Irreversible.")
        self.set_syntax("play <name>", "Join the game as the desired character.")

    key = "char"
    locks = "cmd:all()"
    help_category = "General"

    # this is used by the parent
    account_caller = True

    def func(self):
        """
        Main puppet method
        """
        account = self.account
        session = self.session
        ply = self.caller

        sub = self.word(1)
        arg = self.word(2)

        # Display syntax if used by itself - or if the subcommand isn't found.
        if not sub:
            self.get_syntax()
            return

        if sub == "play":
            new_character = [char for char in search.object_search(arg) if char.access(account, "puppet")]
            if not new_character:
                self.echo("No character by the name was found.", error = True)
                return

            if len(new_character) > 1:
                self.echo("There appear to be multiple characters with that name:\n %s"
                        % ", ".join("%s(#%s)" % (obj.key, obj.id) for obj in new_character), error = True)
                return

            new_character = new_character[0]

            try:
                account.puppet_object(session, new_character)
                account.db._last_puppet = new_character
                logger.log_sec('Puppet Success: (Caller: %s, Target: %s, IP: %s).' % (account, new_character, self.session.address))
            except RuntimeError as exc:
                self.echo("You cannot become %s: %s" % (new_character.name, exc), error = True)
                logger.log_sec('Puppet Failed: %s (Caller: %s, Target: %s, IP: %s).' % (exc, account, new_character, self.session.address))