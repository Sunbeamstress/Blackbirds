# Python modules.
import re, random

# Evennia modules.
from evennia import DefaultCharacter
from evennia import TICKER_HANDLER as tickerhandler
from evennia.utils import logger

# Blackbirds modules.
from typeclasses.species import Human
from utilities.color import color_ramp
from utilities.communication import process_speech
from utilities.display import header, divider, column, bullet
from utilities.string import an, capital, plural, message_token_pluralize, message_token_capitalize, jright, num_word, autoformat
import utilities.directions as dirs
from world.names import CURRENCY, CURRENCY_FULL

class Character(DefaultCharacter):
    def at_object_creation(self):
        self.db.surname = ""
        self.db.prefix = ""
        self.db.suffix = ""
        self.db.age = 18
        self.db.app_age = 18
        self.db.identity = ""
        self.db.height = 172 # Approx. 5' 8" in cm
        self.db.pronoun_they = "they"
        self.db.pronoun_them = "them"
        self.db.pronoun_their = "their"
        self.db.pronoun_theirs = "theirs"
        self.db.species = Human()

        # Stats.
        self.db.hp = {"current": 20, "max": 20} # Hit points.
        self.db.en = {"current": 100, "max": 100} # Endurance.
        self.db.sc = {"current": 0, "max": 3} # Scars (lives).
        self.db.xp = {"current": 0, "max": 1000} # Experience.
        self.db.money = 0
        self.db.neon = 0

        # Abilities.
        self.db.abilities = {}

        # Nicknames.
        self.db.nicks = {}

        # Body system. Stores coverage, descriptions, and more.
        self.build_body()

        # Combat/RP-based statuses.
        self.db.balance = True
        self.db.balance_time = 0
        self.db.prone = 0 # 1 for seated, 2 for lying down

        # Anatomy.
        self.db.has_breasts = True
        self.db.has_genitals = True
        self.db.can_carry_child = True
        self.db.exoskeletal_level = 0
        self.db.has_four_arms = False
        self.db.has_fangs = False
        self.db.has_horns = False
        self.db.has_tail = False
        self.db.is_halfbreed = False
        self.db.has_bioluminescence = False

        # Descriptions.
        self.db.halfbreed_family = "Carven"
        self.db.fang_desc = "fangs"
        self.db.bioluminescence_desc = "white"

    def update(self):
        self.balance = True
        self.balance_time = 0

    def build_body(self):
        # Goddamn what a mess
        self.db.body = {}
        self.init_bodypart(key = "general", aliases = ["self", "base", "basic"], plural_name = "general", can_be_missing = False, can_be_injured = False, is_abstract = True)
        self.init_bodypart(key = "hair", plural_name = "hair", can_be_missing = False, can_be_injured = False)
        if self.db.has_horns:
            self.init_bodypart(key = "horns", aliases = ["horn"], plural_name = "horns")
        self.init_bodypart(key = "eye")
        self.init_bodypart(key = "face", can_be_missing = False)
        self.init_bodypart(key = "neck", aliases = ["throat"], can_be_missing = False)
        if self.db.has_breasts:
            self.init_bodypart(key = "breasts", aliases = ["breast"], plural_name = "breasts", can_be_missing = False)
        else:
            self.init_bodypart(key = "chest", aliases = ["breast"], can_be_missing = False)
        self.init_bodypart(key = "nipples", aliases = ["nip", "nips"], plural_name = "nipples", can_be_injured = False)
        self.init_bodypart(key = "stomach", aliases = ["tummy", "belly", "gut", "stummy"], can_be_missing = False)
        self.init_bodypart(key = "upper_back", fullname = "upper back", aliases = ["ub"], can_be_missing = False)
        self.init_bodypart(key = "lower_back", fullname = "lower back", aliases = ["lb"], can_be_missing = False)
        self.init_bodypart(key = "upper_arms", fullname = "upper arms", aliases = ["ua", "upperarms"])
        self.init_bodypart(key = "lower_arms", fullname = "lower arms", aliases = ["la", "lowerarms"])
        if self.db.has_four_arms:
            self.init_bodypart(key = "extra_arms", fullname = "extra arms", aliases = ["ea", "extraarms"], is_heavy = True)
        self.init_bodypart(key = "hands")
        if self.db.has_tail:
            self.init_bodypart(key = "tail")
        self.init_bodypart(key = "genitals", aliases = ["groin", "loins", "penis", "vagina", "cock", "dick", "pussy"], plural_name = "genitalia", is_inappropriate = True)
        self.init_bodypart(key = "buttocks", aliases = ["butt", "booty", "ass", "derriere"], plural_name = "buttocks", can_be_missing = False)
        self.init_bodypart(key = "upper_leg", fullname = "upper legs", aliases = ["ul"])
        self.init_bodypart(key = "lower_leg", fullname = "lower legs", aliases = ["ll"])
        self.init_bodypart(key = "feet")
        if self.db.has_bioluminescence:
            self.init_bodypart(key = "bioluminescence", aliases = ["bio", "light", "biolight", "luminescence"], plural_name = "bioluminescence", can_be_missing = False, can_be_injured = False, is_abstract = True)
        self.db.bodypart_names = self.build_bodypart_names()

    def init_bodypart(self, key = "body_part", aliases = [], fullname = "", plural_name = "", desc = "", can_be_missing = True, is_missing = False, is_optional = False, is_abstract = False, is_covered = False, is_prosthetic = False, is_inappropriate = False, is_heavy = False, can_be_injured = True, injury_level = 0):
        i = len(self.db.body)
        self.db.body[i] = {}
        self.db.body[i]["key"] = key
        self.db.body[i]["aliases"] = aliases
        self.db.body[i]["fullname"] = fullname if fullname else key
        if plural_name:
            self.db.body[i]["plural_name"] = plural_name
        else:
            self.db.body[i]["plural_name"] = f"{self.db.body[i]['fullname']}{'s' if self.db.body[i]['fullname'][-1:] != 's' else ''}"
        self.db.body[i]["desc"] = desc # The player's customized description for this part.
        self.db.body[i]["can_be_missing"] = can_be_missing # If False, ignores all aspects of missing messages/mechanics.
        self.db.body[i]["is_missing"] = is_missing # Is the body part omitted from the player?
        self.db.body[i]["is_optional"] = is_optional # If true, the part will not be reported if missing.
        self.db.body[i]["is_abstract"] = is_abstract # Used for the 'general' body part, so you can't put clothes on it somehow.
        self.db.body[i]["is_covered"] = is_covered # Is it covered by clothing or otherwise hidden?
        self.db.body[i]["is_prosthetic"] = is_prosthetic # Does the player have a mechanical/false version?
        self.db.body[i]["is_inappropriate"] = is_inappropriate # Will NPCs freak out if the player walks around with it exposed?
        self.db.body[i]["is_heavy"] = is_heavy # For 3rd/4th arms, tank treads, etc. Imposes balance penalties.
        self.db.body[i]["can_be_injured"] = can_be_injured # Self-explanatory. False for things like hair, etc.
        self.db.body[i]["injury_level"] = injury_level # How injured is it? [0 - 3]

    def _reset_species_flags(self):
        self.db.has_four_arms = False
        self.db.has_fangs = False
        self.db.has_horns = False
        self.db.has_tail = False
        self.db.is_halfbreed = False
        self.db.has_bioluminescence = False

    def at_before_say(self, message, proceed = True, **kwargs):
        return message, proceed

    def at_say(self, message, msg_self = None, msg_location = None, receivers = None, msg_receivers = None, **kwargs):
        process_speech(self, message, msg_self, msg_location, receivers, msg_receivers, **kwargs)

    def at_after_say(self, string):
        # Any processing to be done after saying something.
        pass

    def at_desc(self, looker = None, **kwargs):
        # Passed before the desc appears.
        pass

    @property
    def precision_information(self):
        return self.db.species.precision_information

    def compare_height(self, looker):
        l_h, s_h = looker.db.height, self.db.height
        h_perc = (l_h * 100) / s_h
        if h_perc >= 200:
            return "utterly dwarfed by"
        elif h_perc >= 175:
            return "far smaller than"
        elif h_perc >= 150:
            return "much shorter than"
        elif h_perc >= 125:
            return "visibly shorter than"
        elif 80 < h_perc < 125: # This feels dirty
            return "about the same height as"
        elif h_perc <= 80:
            return "visibly taller than"
        elif h_perc <= 60:
            return "much taller than"
        elif h_perc <= 40:
            return "far larger than"
        elif h_perc <= 20:
            return "monstrous compared to"

        return None

    def return_appearance(self, looker = None, **kwargs):
        if not looker:
            return ""

        # Determine whether or not the character is augmented or otherwise privy to precise measurements.
        # Current use cases are for Idols, Blackbirds, and admin players.
        precise = looker.precision_information

        # Build the necessary description components for the header.
        age_string = f"Heuristic analysis suggests {self.they('are')} {an(self.species())}, {self.age} years of age." if precise \
            else f"{capital(self.they('appear'))} to be {an(self.age_description())} {self.species()}."
        h_string = f"approximately {self.height}cm tall" if precise \
            else f"{self.height_description()} for {self.their()} kind"
        h_comp = "about the same height as"
        if precise:
            h_comp = "precisely as tall as" if looker.height == self.height \
                else f"{abs(looker.height - self.height)} {'taller' if self.height > looker.height else 'shorter'} than"
        else:
            h_comp = self.compare_height(looker)

        # Display the description header.
        string  = f"You know this person as {self.nickname(looker)}. {age_string}"
        string += f"\n{capital(self.they('are'))} {h_string}, {h_comp} you."

        # Build a mass description from body parts.
        string += "\n\n" + self.compiled_description

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

    @property
    def hp(self):
        return self.db.hp["current"]

    @property
    def max_hp(self):
        return self.db.hp["max"]

    @property
    def en(self):
        return self.db.en["current"]

    @property
    def max_en(self):
        return self.db.en["max"]

    @property
    def sc(self):
        return self.db.sc["current"]

    @property
    def max_sc(self):
        return self.db.sc["max"]

    @property
    def xp(self):
        return self.db.xp["current"]

    @property
    def max_xp(self):
        return self.db.xp["max"]

    @property
    def prone(self):
        return self.db.prone

    @property
    def prefix(self):
        return self.db.prefix if self.db.prefix else ""

    @property
    def suffix(self):
        if not self.db.suffix:
            return ""

        return f"{' ' if self.db.suffix[0] in (',', chr(39)) else ''}{self.db.suffix}"

    @property
    def height(self):
        return self.db.height

    @property
    def age(self):
        return self.db.age

    def use_balance(self, t):
        self.db.balance = False
        self.db.balance_time = t
        tickerhandler.add(self.db.balance_time, self.recover_balance)

    def recover_balance(self):
        tickerhandler.remove(self.db.balance_time, self.recover_balance)
        self.db.balance = True
        self.db.balance_time = 0
        self.echo("|c(|C!|c)|n You can act again.", prompt = True)

    def in_chargen(self):
        c = self.location.__class__.__name__
        return c == "ChargenRoom"

    def prompt_status(self):
        if self.in_chargen():
            return "chargen"

        return "default"

    def prompt(self):
        "Returns the object's prompt, if applicable."
        status = self.prompt_status()
        p_string = ""

        if status == "default":
            stat_string = ""
            
            # Core stats.
            for stat in ["hp", "en"]:
                m_cur, m_max = getattr(self, stat), getattr(self, "max_" + stat)
                c = color_ramp(m_cur, m_max, cap = True)
                c_string = "".join(c)
                s_string = f"|013{'0' * (3 - len(str(m_cur)))}|n|{c_string}{str(m_cur)}|n"
                p_string += f"|x{stat.upper()}|c|||n{s_string} "

            # Experience.
            r_xp = round(self.xp)
            p_string += f"|504XP|c|||n|202{'0' * (len(str(self.max_xp)) - len(str(r_xp)))}|505{r_xp}|n "

            # Scars.
            p_string += f"|411SC|r|||n|R{'*' * self.sc}|n " if self.sc > 0 else ""

            # Statuses.
            stat_string += "|cp|n" if self.prone > 0 else ""

            stat_string += "" if len(stat_string) >= 1 else ""
            p_string += stat_string

            b_string = f"{' ' if len(stat_string) >= 1 else ''}|{'C!' if self.db.balance == True else 'r_'}|n"
            p_string += f"{b_string} "

            # Cap that bad boy off.
            p_string += "|x-|n "

        elif status == "chargen":
            p_string = f"|035{'-' * 80}"

        return p_string

    def has_ability(self, ability_key, level = 1):
        "Checks to see if the player has a given ability. If a level is provided, it will only pass True if the ability score is that level or higher."
        if not ability_key in self.db.abilities:
            return False

        if self.db.abilities[ability_key] < level:
            return False

        return True

    def coordinates(self):
        if not self.location:
            return [0, 0, 0]

        loc = self.location
        return [loc.db.x, loc.db.y, loc.db.z]

    def can_move(self):
        if self.db.prone > 0:
            return False, "You'll need to get up, first."

        if self.db.balance == False:
            return False, "You're too off-balance to move."

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
        destination = loc.exit_destination(dir)
        self.move_to(destination)

    def move_to(self, destination, quiet = False, move_hooks = True, move_msg = None, **kwargs):
        # self: obvious.
        # destination: handled by dir-based move method
        # quiet: if true, won't display enter/exit messages
        # move_hooks: if False, bypasses at_move/before_move on objects
        # move_msg: A message to be passed on to the at_after_move() method. Displays a custom
        #           message before the room is displayed.

        # should return True if move was successful, and False if not

        # all access/ability checks should be handled before this method!
        # if we've gotten to move_to, everything is green and we are ready
        # to move the object.

        def error_msg(string = "", err = None):
            """Simple log helper method"""
            logger.log_trace()
            self.error_echo("%s%s" % (string, "" if err is None else " (%s)" % err))
            return

        errtxt = ("Method move_to failed at: ('%s').")

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

        # Perform the movement itself.
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
            # (the object has already arrived at this point).
            try:
                destination.at_object_receive(self, source_location)
            except Exception as err:
                error_msg(errtxt % "at_object_receive()", err)
                return False

        # Execute eventual extra commands on this object after moving it
        # (usually calling 'look')
        if move_hooks:
            try:
                self.at_after_move(source_location, move_msg = move_msg)
            except Exception as err:
                error_msg(errtxt % "at_after_move()", err)
                return False

        return True

    def at_after_move(self, source_location, move_msg = None, **kwargs):
        "Performed as the last step after a successful movement. By default, displays the room."
        if move_msg:
            self.echo(move_msg)

        if self.location.access(self, "view"):
            self.msg(self.at_look(self.location))

    def at_look(self, target = None, **kwargs):
        # If the player has no species or their species doesn't override at_look,
        # use the default functionality.
        if not self.db.species or self.db.species.at_look != True:
            if not target.access(self, "view"):
                try:
                    return "Could not view '%s'." % target.get_display_name(self, **kwargs)
                except AttributeError:
                    return "Could not view '%s'." % target.key

            description = target.return_appearance(self, **kwargs)

            # the target's at_desc() method.
            # this must be the last reference to target so it may delete itself when acted on.
            target.at_desc(looker = self, **kwargs)

            return description

        return self.db.species.at_look(self, target = None, **kwargs)

    def zone(self):
        loc = self.location
        return loc.zone()

    def x(self):
        loc = self.location
        return loc.db.x

    def y(self):
        loc = self.location
        return loc.db.y

    def z(self):
        loc = self.location
        return loc.db.z

    def coords(self):
        loc = self.location
        return [loc.db.x, loc.db.y, loc.db.z]

    def surname(self):
        return self.db.surname if self.db.surname else ""

    def species(self):
        return self.db.species.name if self.db.species else "Unknown"

    def they(self, word = None):
        return f"{self.db.pronoun_they} {self.pluralize(word)}" if word else self.db.pronoun_they
        return self.db.pronoun_they

    def them(self):
        return self.db.pronoun_them

    def their(self):
        return self.db.pronoun_their

    def theirs(self):
        return self.db.pronoun_theirs

    def pronouns(self):
        return f"{self.they()}, {self.them()}, {self.their()}, {self.theirs()}"

    @property
    def rubric(self):
        return self.account.db.rubric

    @property
    def neon(self):
        return self.db.neon

    @property
    def money(self):
        return self.db.money

    def score(self):
        col_width = 10

        full_name = f"{self.name} {self.db.surname}" if self.db.surname else self.name
        full_age = f"{self.db.app_age} |x(|n{self.db.age}|x)|n" if self.db.app_age != self.db.age else self.db.age

        hp_string = "|013%s|055%s |013%s|055%s|n" % ("0" * (4 - len(str(self.hp))), self.hp, "0" * (4 - len(str(self.max_hp))), self.max_hp)
        en_string = "|013%s|055%s |013%s|055%s|n" % ("0" * (4 - len(str(self.en))), self.en, "0" * (4 - len(str(self.max_en))), self.max_en)
        r_xp = round(self.xp)
        xp_string = "|202%s|505%s |202%s|505%s|n" % ("0" * (4 - len(str(r_xp))), r_xp, "0" * (4 - len(str(self.max_xp))), self.max_xp)
        sc_string = "|200%s|511%s |200%s|511%s|n" % ("0" * (4 - len(str(self.sc))), self.sc, "0" * (4 - len(str(self.max_sc))), self.max_sc)

        string = ""
        string += f"{self.prefix}|W{full_name}|n{self.suffix}"
        string += "\n" + divider()
        string += "\n|cCharacter Information|n"

        string += "\n" + column("Age", full_age, title_width = col_width, value_width = 24)
        string += column("Health", hp_string, title_width = col_width)
        string += "\n" + column("Species", self.species(), title_width = col_width, value_width = 24)
        string += column("Endurance", en_string, title_width = col_width)
        string += "\n" + column("Pronouns", f"{self.pronouns()}", title_width = col_width, value_width = 24)
        string += column("Experience", xp_string, title_width = col_width)
        string += "\n" + (" " * 39)
        string += column("Scars", sc_string, title_width = col_width)

        string += "\n\n|cOrganizations & Allegiances|n"

        string += "\n" + bullet("You are a |WCitizen|n of the |WState of Brillante|n.")
        string += "\n" + bullet("You are a |WPrefect Initiate|n in the |WCoalhound Corps|n.")
        string += "\n" + bullet("You worship |WNever-Knows-Best, the Massacre Spirit|n.")

        string += "\n\n|cAssets & Money|n"
        string += "\n" + bullet("You do not own any buildings.")
        string += "\n" + bullet(f"You have accumulated |C{round(self.rubric):,}|n Rubric.")
        string += "\n" + bullet(f"You have accumulated |M{self.neon:,}|n Neon.")
        string += "\n" + bullet(f"|yYour {CURRENCY_FULL} stands at |Y{self.money:.3f} {CURRENCY}|y.|n", color = "320")

        string += "\n" + divider()
        string += "\nType |Rab|n to see your learned abilities."
        string += "\nType |Rcr|n to see all currencies you own."

        return string

    def pluralize(self, string):
        "Shortcut for the plural() string utility. Only pluralizes the word if the character's pronouns are not neutral."
        if self.they() == "they":
            return string

        # Sometimes we have to step in, in special cases where the inflect engine fails.
        if string == "are":
            return "is"

        return plural(string)

    def message(self, self_m = None, target = None, tar_m = None, witness_m = None):
        """A specifically formatted message that originates from the Character. Special tokens are used to populate data and facilitate the writing of combat or other game messages.

        self_m = The message the originating character sees.
        target = A valid character object, not the self.
        tar_m = The message the target sees, if any.
        witness_m = A third-party message that others in the room see.
        
        TARGET: The target's name. Not used in tar_m.
        TARGET_THEY, TARGET_THEM, TARGET_THEIR, TARGET_THEIRS: The target's pronouns. Not used in tar_m.
        PLAYER: The character's name. Not used in self_m.
        PLAYER_THEY, PLAYER_THEM, PLAYER_THEIR, PLAYER_THEIRS: The character's pronouns. Not used in self_m.
        !verb: A verb originating from the character. Should be written in singular form, and will become plural if the pronouns accept it.
        #verb: A verb originating from the target. Should be written in singular form, and will become plural if the pronouns accept it.
        +word: The word is to be capitalized."""

        if self_m == None:
            return

        if target and tar_m == None:
            return

        if target:
            self_m = self_m.replace("TARGET_THEY", target.they())
            self_m = self_m.replace("TARGET_THEM", target.them())
            self_m = self_m.replace("TARGET_THEIR", target.their())
            self_m = self_m.replace("TARGET_THEIRS", target.theirs())
            self_m = self_m.replace("TARGET", target.name)
            self_m = message_token_pluralize(self_m, "#", target)
            self_m = message_token_capitalize(self_m)

        if tar_m:
            tar_m = tar_m.replace("PLAYER_THEY", self.they())
            tar_m = tar_m.replace("PLAYER_THEM", self.them())
            tar_m = tar_m.replace("PLAYER_THEIR", self.their())
            tar_m = tar_m.replace("PLAYER_THEIRS", self.theirs())
            tar_m = tar_m.replace("PLAYER", self.name)
            tar_m = message_token_pluralize(tar_m, "!", self)
            tar_m = message_token_capitalize(tar_m)

        if witness_m:
            witness_m = witness_m.replace("TARGET_THEY", target.they())
            witness_m = witness_m.replace("TARGET_THEM", target.them())
            witness_m = witness_m.replace("TARGET_THEIR", target.their())
            witness_m = witness_m.replace("TARGET_THEIRS", target.theirs())
            witness_m = witness_m.replace("TARGET", target.name)
            witness_m = witness_m.replace("PLAYER_THEY", self.they())
            witness_m = witness_m.replace("PLAYER_THEM", self.them())
            witness_m = witness_m.replace("PLAYER_THEIR", self.their())
            witness_m = witness_m.replace("PLAYER_THEIRS", self.theirs())
            witness_m = witness_m.replace("PLAYER", self.name)
            witness_m = message_token_pluralize(witness_m, "!", self)
            witness_m = message_token_pluralize(witness_m, "#", target)
            witness_m = message_token_capitalize(witness_m)

        self.echo(self_m, prompt = True)
        if tar_m:
            target.echo(tar_m, prompt = True)
        if witness_m:
            # room.echo(witness_m, prompt = True)
            pass

    def description(self):
        return self.db.desc if self.db.desc else "A strangely nondescript person."

    def change_description(self, bodypart, new_desc):
        bname = self.bodypart_name(bodypart)
        old_desc = self.bodypart_desc(bodypart)
        if new_desc in ("none", "clear", "empty", "erase", "wipe"):
            self.bodypart_set_desc(bodypart, "")
            self.echo(f"You clear the description of your {bname}.")
        else:
            self.bodypart_set_desc(bodypart, autoformat(new_desc, allow_breaks = False))
            self.echo(f"|xYour {bname} will now be described as:|n\n{self.bodypart_desc(bodypart)}")

        if old_desc:
            self.echo(f"\n\n|xIts old description was:|n\n{old_desc}")

    def identity(self):
        return self.db.identity if self.db.identity else "an unremarkable person"

    def nickname(self, looker):
        if not looker:
            return self.identity()

        if looker == self:
            return self.name

        if looker in self.db.nicks:
            return self.db.nicks[looker]

        return self.identity()

    def age_description(self):
        return self.db.species.age_description(self.db.age)

    def height_description(self):
        return self.db.species.height_description(self.db.height)

    def build_bodypart_names(self):
        "Used to update the list of valid body part aliases the character has. Can change based on removal/additions of body parts."
        b_tbl = {}
        for i in self.db.body:
            b_tbl[self.db.body[i]["key"]] = i
            b_tbl[self.db.body[i]["plural_name"]] = i
            for a in self.db.body[i]["aliases"]:
                b_tbl[a] = i

        return b_tbl

    def _valid_bodypart(self, b_part):
        if len(self.db.bodypart_names) < 1:
            return None

        if b_part in self.db.bodypart_names:
            b_part = self.db.bodypart_names[b_part]

        try:
            b = self.db.body[b_part]
            return b_part
        except KeyError:
            return None

    def has_bodypart(self, b_part):
        if self._valid_bodypart(b_part) == None:
            return False

        b_part = self._valid_bodypart(b_part)

        if self.db.body[b_part]["is_missing"]:
            return False

        return True

    def bodypart_name(self, b_part):
        b_part = self._valid_bodypart(b_part)
        return "" if b_part == None else self.db.body[b_part]["fullname"]

    def bodypart_desc(self, b_part):
        b_part = self._valid_bodypart(b_part)
        return "" if b_part == None else self.db.body[b_part]["desc"]

    def bodypart_set_desc(self, b_part, string):
        b_part = self._valid_bodypart(b_part)
        if b_part != None:
            self.db.body[b_part]["desc"] = string

    @property
    def compiled_description(self):
        string = ""
        for i in self.db.body:
            d = self.db.body[i]["desc"]
            string += f"{' ' if d else ''}{d}"

        return string.strip()

    @property
    def bioluminescence_color_code(self):
        if not self.db.bioluminescence_desc or self.db.bioluminescence_desc == "":
            return "n"

        c = self.db.bioluminescence_desc.lower()
        if c == "white":
            return "554"
        elif c == "blue":
            return "145"
        elif c == "green":
            return "153"
        elif c == "gold":
            return "540"
        elif c == "violet":
            return "525"
        elif c == "red":
            return "521"

        return "n"