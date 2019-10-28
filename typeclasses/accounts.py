"""
Account

The Account represents the game "account" and each login has only one
Account object. An Account is what chats on default channels but has no
other in-game-world existence. Rather the Account puppets Objects (such
as Characters) in order to actually participate in the game world.


Guest

Guest accounts are simple low-level accounts that are created/deleted
on the fly and allows users to test the game without the commitment
of a full registration. Guest accounts are deactivated by default; to
activate them, add the following line to your settings file:

    GUEST_ENABLED = True

You will also need to modify the connection screen to reflect the
possibility to connect with a guest account. The setting file accepts
several more options for customizing the Guest account system.

"""

# Evennia stuff.
from evennia import DefaultAccount, DefaultGuest
from evennia.utils.utils import (lazy_property, to_str, make_iter, is_iter, variable_from_module)

# Blackbirds stuff.
from server.conf import settings
from utilities.display import header, divider
from utilities.string import jleft, jright

_MAX_NR_CHARACTERS = settings.MAX_NR_CHARACTERS
_MULTISESSION_MODE = settings.MULTISESSION_MODE

class Account(DefaultAccount):
    """
    This class describes the actual OOC account (i.e. the user connecting
    to the MUD). It does NOT have visual appearance in the game world (that
    is handled by the character which is connected to this). Comm channels
    are attended/joined using this object.

    It can be useful e.g. for storing configuration options for your game, but
    should generally not hold any character-related info (that's best handled
    on the character level).

    Can be set using BASE_ACCOUNT_TYPECLASS.


    * available properties

     key (string) - name of account
     name (string)- wrapper for user.username
     aliases (list of strings) - aliases to the object. Will be saved to database as AliasDB entries but returned as strings.
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
     date_created (string) - time stamp of object creation
     permissions (list of strings) - list of permission strings

     user (User, read-only) - django User authorization object
     obj (Object) - game object controlled by account. 'character' can also be used.
     sessions (list of Sessions) - sessions connected to this account
     is_superuser (bool, read-only) - if the connected user is a superuser

    * Handlers

     locks - lock-handler: use locks.add() to add new lock strings
     db - attribute-handler: store/retrieve database attributes on this self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not create a database entry when storing data
     scripts - script-handler. Add new scripts to object with scripts.add()
     cmdset - cmdset-handler. Use cmdset.add() to add new cmdsets to object
     nicks - nick-handler. New nicks with nicks.add().

    * Helper methods

     msg(text=None, **kwargs)
     execute_cmd(raw_string, session=None)
     search(ostring, global_search=False, attribute_name=None, use_nicks=False, location=None, ignore_errors=False, account=False)
     is_typeclass(typeclass, exact=False)
     swap_typeclass(new_typeclass, clean_attributes=False, no_default=True)
     access(accessing_obj, access_type='read', default=False)
     check_permstring(permstring)

    * Hook methods (when re-implementation, remember methods need to have self as first arg)

     basetype_setup()
     at_account_creation()

     - note that the following hooks are also found on Objects and are
       usually handled on the character level:

     at_init()
     at_cmdset_get(**kwargs)
     at_first_login()
     at_post_login(session=None)
     at_disconnect()
     at_message_receive()
     at_message_send()
     at_server_reload()
     at_server_shutdown()

    """

    def at_account_creation(self):
        """
        This is called once, the very first time the account is created
        (i.e. first time they register with the game). It's a good
        place to store attributes all accounts should have, like
        configuration values etc.
        """
        # set an (empty) attribute holding the characters this account has
        lockstring = "attrread:perm(Admins);attredit:perm(Admins);" \
                     "attrcreate:perm(Admins);"
        self.attributes.add("_playable_characters", [], lockstring = lockstring)
        self.attributes.add("_saved_protocol_flags", {}, lockstring = lockstring)

    def at_first_login(self, **kwargs):
        """
        Called the very first time this account logs into the game.
        Note that this is called *before* at_pre_login, so no session
        is established and usually no character is yet assigned at
        this point. This hook is intended for account-specific setup
        like configurations.

        Args:
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).
        """
        pass

    def at_look(self, target = None, session = None, **kwargs):
        """
        Called when this object executes a look. It allows to customize
        just what this means.

        Args:
            target (Object or list, optional): An object or a list
                objects to inspect.
            session (Session, optional): The session doing this look.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).

        Returns:
            look_string (str): A prepared look string, ready to send
                off to any recipient (usually to ourselves)
        """
        if target and not is_iter(target):
            # single target - just show it
            if hasattr(target, "return_appearance"):
                return target.return_appearance(self)
            else:
                return "{} has no in-game appearance.".format(target)
        else:
            # list of targets - make list to disconnect from db
            characters = list(tar for tar in target if tar) if target else []
            sessions = self.sessions.all()
            if not sessions:
                # no sessions, nothing to report
                return ""
            is_su = self.is_superuser

            # The OOC "area" to be displayed when not logged into a character.
            result = [f"   |xWelcome to Blackbirds,|n {self.key}|x.|n"]

            charmax = _MAX_NR_CHARACTERS
            if is_su or len(characters) < charmax:
                result.append("\n")
                if not characters:
                    result.append("\nYou don't have any characters yet. Type |Rchar create|n to establish your first one.")
                else:
                    result.append("\n   |Rchar create       |n |c-|n Create a new character.")
                    result.append("\n   |Rchar delete <name>|n |c-|n Delete a character.")

            if characters:
                string_s_ending = len(characters) > 1 and "s" or ""
                ply_char_max = is_su and "-" or charmax

                result.append("\n   |Rchar play <name>  |n |c-|n Join the game.")
                result.append("\n\n   |xAvailable character%s|n%s|x:|n" % (string_s_ending, charmax > 1 and " |x(|n%s|x/|n%s|x)|n" % (len(characters), ply_char_max) or ""))

                for char in characters:
                    fullname = f"{char.key} {char.surname()}" if char.db.surname else f"{char.key}"

                    csessions = char.sessions.all()
                    if csessions:
                        for sess in csessions:
                            # character is already puppeted
                            sid = sess in sessions and sessions.index(sess) + 1
                            if sess and sid:
                                result.append("\n     |G%s|n [%s] (played by you in session %i)"
                                              % (char.key, ", ".join(char.permissions.all()), sid))
                            else:
                                result.append("\n     |R%s|n [%s] (played by someone else)"
                                              % (char.key, ", ".join(char.permissions.all())))
                    else:
                        # character is "free to puppet"
                        result.append("\n    |C%s|n%s|x%s|n" % (jleft(char.key, 16), jleft(char.species(), 14), fullname))

            look_string = header("Blackbirds", color = "c", title_color = "M") + "\n" + "".join(result) + "\n" + divider(color = "c")
            return look_string

    def at_post_login(self, session = None, **kwargs):
        """
        Called at the end of the login process, just before letting
        the account loose.

        Args:
            session (Session, optional): Session logging in, if any.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).

        Notes:
            This is called *before* an eventual Character's
            |at_post_login` hook. By default it is used to set up
            auto-puppeting based on |MULTISESSION_MODE`.

        """
        # if we have saved protocol flags on ourselves, load them here.
        protocol_flags = self.attributes.get("_saved_protocol_flags", {})
        if session and protocol_flags:
            session.update_flags(**protocol_flags)

        # inform the client that we logged in through an OOB message
        if session:
            session.msg(logged_in={})

        self._send_to_connect_channel("|G%s connected|n" % self.key)
        if _MULTISESSION_MODE == 0:
            # in this mode we should have only one character available. We
            # try to auto-connect to our last conneted object, if any
            try:
                self.puppet_object(session, self.db._last_puppet)
            except RuntimeError:
                self.msg("The Character does not exist.")
                return
        elif _MULTISESSION_MODE == 1:
            # in this mode all sessions connect to the same puppet.
            try:
                self.puppet_object(session, self.db._last_puppet)
            except RuntimeError:
                self.msg("The Character does not exist.")
                return
        elif _MULTISESSION_MODE in (2, 3):
            # In this mode we by default end up at a character selection
            # screen. We execute look on the account.
            # we make sure to clean up the _playable_characters list in case
            # any was deleted in the interim.
            self.db._playable_characters = [char for char in self.db._playable_characters if char]
            self.msg(self.at_look(target=self.db._playable_characters,
                                  session=session), session=session)

    def echo(self, string, prompt = False, error = False):
        # At this moment, simply a lazy method wrapper that sends a message to the object,
        # then displays a prompt.
        if error == True:
            string = "|x" + string + "|n"

        self.msg(string)
        if prompt == True:
            self.msg(prompt = self.prompt())

    def prompt(self):
        "Returns the object's prompt, if applicable."
        p_string = f"|M---|n"
        return p_string


class Guest(DefaultGuest):
    """
    This class is used for guest logins. Unlike Accounts, Guests and their
    characters are deleted after disconnection.
    """
    pass
