"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
# Evennia modules.
from evennia import DefaultCharacter
from evennia.utils import logger

# Blackbirds modules.
from utilities.utils_communication import ProcessSpeech
from utilities.utils_display import Line
import utilities.utils_directions as dirs

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

    def echo(self, string, prompt = False, error = False):
        # At this moment, simply a lazy method wrapper that sends a message to the object,
        # then displays a prompt.
        if error == True:
            string = "|x" + string + "|n"

        self.msg(string)
        if prompt == True:
            self.msg(prompt = self.prompt())

    def error_echo(self, string, prompt = False):
        self.echo(string, prompt = prompt, error = True)

    def prompt(self):
        "Returns the object's prompt, if applicable."
        # Placeholder for now - replace with real one later.
        HP, MP, END, WIL = 500, 500, 1500, 1500
        p_string = f"|cH:|n{HP} |cM:|n{MP} |cE:|n{END} |cW:|n{END} |x-|n "
        return p_string

    def coordinates(self):
        if not self.location:
            return [0, 0, 0]

        loc = self.location
        return [loc.db.x, loc.db.y, loc.db.z]

    def can_move(self):
        if self.db.prone > 0:
            return False, "You'll need to get up, first."

        return True, ""

    def move_call(self, dir = None):
        # Player is not in a room.
        if not self.location:
            self.error_echo("You can't figure out how to move anywhere from here.")
            return

        # Player somehow didn't specify a direction.
        if not dir:
            self.error_echo("Which way are you trying to go?")
            return

        # Direction existence passed, sanitize direction.
        dir = dirs.valid_direction(dir)

        # Check for various factors that might prevent a player from moving.
        # (afflictions, prone status, sleeping, etc.)
        cm_check, cm_msg = self.can_move()
        if cm_check == False:
            cm_msg = cm_msg if cm_msg else "You can't seem to move."
            self.error_echo(f"{cm_msg}")
            return

        # Ensure room has exit in the desired direction.
        loc = self.location
        if not loc.has_exit(dir):
            self.error_echo(f"There is no {dir}ward exit.")
            return

        # Player passed. Get destination, send them on through.
        destination = loc.db.exits[dir]['destination']
        self.move_to(destination)

    def move_to(self, destination, quiet = False, move_hooks = True, **kwargs):
        # self: obvious.
        # destination: handled by dir-based move method
        # quiet: if true, won't display enter/exit messages
        # move_hooks: if False, bypasses at_move/before_move on objects

        # should return True if move was successful, and False if not

        # all access/ability checks should be handled before this method!
        # if we've gotten to move_to, everything is green and we are ready
        # to move the object.

        def error_msg(string = "", err = None):
            """Simple log helper method"""
            logger.log_trace()
            self.error_echo("%s%s" % (string, "" if err is None else " (%s)" % err))
            return

        errtxt = ("Couldn't perform move ('%s'). Contact an admin.")

        # Convert destination to actual room.
        destination = self.search(destination, global_search = True)
        if not destination:
            self.error_echo("You can't seem to figure out how to get there.")
            return False

        if move_hooks:
            try:
                if not self.at_before_move(destination):
                    return False
            except Exception as err:
                error_msg(errtxt % "at_before_move()", err)
                return False

        source_location = self.location
        if move_hooks and source_location:
            try:
                source_location.at_object_leave(self, destination)
            except Exception as err:
                error_msg(errtxt % "at_object_leave()", err)
                return False

        if not quiet:
            try:
                self.announce_move_from(destination, **kwargs)
            except Exception as err:
                error_msg(errtxt % "at_announce_move()", err)
                return False

        try:
            self.location = destination
        except Exception as err:
            error_msg(errtxt % "location change", err)
            return False

        if not quiet:
            # Tell the new room we are there.
            try:
                self.announce_move_to(source_location, **kwargs)
            except Exception as err:
                error_msg(errtxt % "announce_move_to()", err)
                return False

        if move_hooks:
            # Perform eventual extra commands on the receiving location
            # (the object has already arrived at this point)
            try:
                destination.at_object_receive(self, source_location)
            except Exception as err:
                error_msg(errtxt % "at_object_receive()", err)
                return False

        # Execute eventual extra commands on this object after moving it
        # (usually calling 'look')
        if move_hooks:
            try:
                self.at_after_move(source_location)
            except Exception as err:
                error_msg(errtxt % "at_after_move", err)
                return False

        return True