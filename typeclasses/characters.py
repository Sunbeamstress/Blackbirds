"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter

from utilities.utils_communication import ProcessSpeech
from utilities.utils_display import Line

class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """
    def at_object_creation(self):
        self.db.surname = ""
        self.db.age = 18
        self.db.app_age = 18
        self.db.intro = ""
        self.db.pronoun_he = "she"
        self.db.pronoun_him = "her"
        self.db.pronoun_his = "her"
        self.db.pronoun_hiss = "hers"
        self.db.species = "Human"
        self.db.archetype = "Citizen"
        self.db.background = "Pauper"
        self.db.prone = 0 # 1 for seated, 2 for lying down

    def at_before_say(self, message, **kwargs):
        return message

    def at_say(self, message, msg_self = None, msg_location = None, receivers = None, msg_receivers = None, **kwargs):
        ProcessSpeech(self, message, msg_self, msg_location, receivers, msg_receivers, **kwargs)

    def at_after_say(self, string):
        # Any processing to be done after saying something.
        pass

    def at_desc(self, looker = None, **kwargs):
        # Passed before the desc appears.
        pass

    def return_appearance(self, looker = None, **kwargs):
        if not looker:
            return ""

        surname = ""
        if self.db.surname:
            surname = f" {self.db.surname}"
        string = f"|xThis is |c{self.key}{surname}|n|x, a|n |c{self.db.species}|n|x.|n\n"
        string += Line()
        string += f"\n{self.db.desc}"

        return string

    def prompt(self):
        "Returns the player's prompt."
        # Placeholder for now - replace with real one later.
        HP, MP, END, WIL = 500, 500, 1500, 1500
        p_string = f"|cH:|n{HP} |cM:|n{MP} |cE:|n{END} |cW:|n{END} |x-|n "
        return p_string

    def echo(self, string, prompt = False):
        # At this moment, simply a lazy method wrapper that sends a message to the player,
        # then displays a prompt.
        self.msg(string)
        if prompt == True:
            self.msg(prompt = self.prompt())