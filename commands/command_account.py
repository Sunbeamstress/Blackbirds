import random

from evennia.utils import utils, create, logger, search

from commands.command import Command
from server.conf import settings
from typeclasses.characters import Character
from utilities.characters import name_is_taken

_MAX_NR_CHARACTERS = settings.MAX_NR_CHARACTERS
_MULTISESSION_MODE = settings.MULTISESSION_MODE
_START_LOCATION = settings.START_LOCATION

def play_character(ply, account, session, char_name):
    new_character = [char for char in search.object_search(char_name) if char.access(account, "puppet")]

    if not new_character:
        ply.error_echo("No character by the name was found.")
        return

    if len(new_character) > 1:
        ply.error_echo("There appear to be multiple characters with that name:\n %s"
                % ", ".join("%s(#%s)" % (obj.key, obj.id) for obj in new_character))
        return

    new_character = new_character[0]

    try:
        account.puppet_object(session, new_character)
        account.db._last_puppet = new_character
        logger.log_sec('Puppet Success: (Caller: %s, Target: %s, IP: %s).' % (account, new_character, session.address))
    except RuntimeError as exc:
        ply.error_echo("You cannot become %s: %s" % (new_character.name, exc))
        logger.log_sec('Puppet Failed: %s (Caller: %s, Target: %s, IP: %s).' % (exc, account, new_character, session.address))

def create_character(ply, account, session):
    charmax = _MAX_NR_CHARACTERS

    if not account.is_superuser and (account.db._playable_characters and len(account.db._playable_characters) >= charmax):
        ply.error_echo(f"You may only create a maximum of {charmax} characters.")
        return

    typeclass = settings.BASE_CHARACTER_TYPECLASS
    new_key = "Character" + str(random.randint(100000, 999999))

    if name_is_taken(new_key):
        # If by some ridiculous chance the number gen spins up a duplicate 'Character123456'.
        ply.error_echo(f"A character named {key} already exists. Try creating your character again.")
        return

    # Create the character.
    permissions = settings.PERMISSION_ACCOUNT_DEFAULT
    new_character = create.create_object(typeclass, key = new_key, location = _START_LOCATION, home = None, permissions = permissions)
    new_character.db.desc = "A person of utter nondescription."

    # Only allow the creator (and developers) to puppet this character.
    new_character.locks.add(f"puppet:id({new_character.id}) or pid({account.id}) or pperm(Developer);delete:id({account.id}) or perm(Admin)")
    account.db._playable_characters.append(new_character)

    ply.echo(f"You create a new character. Use the command |Rchar play {new_key}|n to begin character generation.")
    logger.log_sec(f"Character Created: {new_character} (Creator: {account}, IP: {session.address}).")

def delete_character(ply, account, session, char_name):
    if not char_name or char_name == "":
        ply.error_echo("You must supply a character to delete. This action cannot be undone.")
        return

    match = [char for char in utils.make_iter(account.db._playable_characters) if char.key.lower() == char_name.lower()]
    if not match:
        ply.error_echo("You have no such character by that name. Please ensure you've spelled it correctly.")
        return

    elif len(match) > 1:
        ply.error_echo("You appear to somehow have multiple characters with the same name. Please contact an admin or developer for assistance with deleting your character.")
        return

    else:
        char = match[0]

        if not char.access(account, "delete"):
            ply.error_echo("You must be given permission to delete this character.")
            return

        del_char = char
        key = del_char.key
        ply.db._playable_characters = [c for c in ply.db._playable_characters if c != del_char]
        del_char.delete()
        ply.echo(f"You delete {key}.")
        logger.log_sec(f"Character Deleted: {key} (Caller: {account}, IP: {session.address})")

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
            play_character(ply, account, session, arg)

        elif sub == "create":
            create_character(ply, account, session)

        elif sub == "delete":
            delete_character(ply, account, session, arg)

        else:
            self.get_syntax()