import random

from evennia.utils import utils, create, logger, search

from server.conf import settings
from typeclasses.characters import Character
from commands.command import Command

_MAX_NR_CHARACTERS = settings.MAX_NR_CHARACTERS
_MULTISESSION_MODE = settings.MULTISESSION_MODE
_START_LOCATION = settings.START_LOCATION

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

        elif sub == "create":
            charmax = _MAX_NR_CHARACTERS

            if not account.is_superuser and \
                   (account.db._playable_characters and
                   len(account.db._playable_characters) >= charmax):
                self.echo("You may only create a maximum of %i characters." % charmax)
                return

            from evennia.objects.models import ObjectDB
            typeclass = settings.BASE_CHARACTER_TYPECLASS
            new_key = "Character" + str(random.randint(100000,999999))

            if ObjectDB.objects.filter(db_typeclass_path = typeclass, db_key__iexact = new_key):
                # It should be virtually impossible to have a default 'Character123456' character,
                # but just in case.
                self.echo("A character named '%s' already exists." % key)
                return

            # create the character
            permissions = settings.PERMISSION_ACCOUNT_DEFAULT
            new_character = create.create_object(typeclass, key = new_key,
                                                location = _START_LOCATION,
                                                home = None,
                                                permissions = permissions)
            # only allow creator (and developers) to puppet this char
            new_character.locks.add("puppet:id(%i) or pid(%i) or perm(Developer) or pperm(Developer);delete:id(%i) or perm(Admin)" %
                                    (new_character.id, account.id, account.id))
            account.db._playable_characters.append(new_character)
            new_character.db.desc = "This is a character."
            self.echo(f"You create a new character. Use the command |Rchar play {new_key}|n to begin character generation.")
            logger.log_sec('Character Created: %s (Caller: %s, IP: %s).' % (new_character, account, self.session.address))