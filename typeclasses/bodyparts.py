class BodyPart():
    "Represents one of various regions of the character's body. Stores data regarding coverage, customized description, tattoos, injuries, and other identifiers."
    def __init__(self, key = "body_part", aliases = [], fullname = "", plural_name = "", desc = "", can_be_missing = True, is_missing = False, is_optional = False, is_abstract = False, is_covered = False, is_prosthetic = False, is_inappropriate = False, is_heavy = False, can_be_injured = True, injury_level = 0):
        self.key = key
        self.aliases = aliases
        self._fullname = fullname
        self._plural_name = plural_name
        self._desc = desc # The player's customized description for this part.
        self._can_be_missing = can_be_missing # If False, ignores all aspects of missing messages/mechanics.
        self._is_missing = is_missing # Is the body part omitted from the player?
        self._is_optional = is_optional # If true, the part will not be reported if missing.
        self._is_abstract = is_abstract # Used for the 'general' body part, so you can't put clothes on it somehow.
        self._is_covered = is_covered # Is it covered by clothing or otherwise hidden?
        self._is_prosthetic = is_prosthetic # Does the player have a mechanical/false version?
        self._is_inappropriate = is_inappropriate # Will NPCs freak out if the player walks around with it exposed?
        self._is_heavy = is_heavy # For 3rd/4th arms, tank treads, etc. Imposes balance penalties.
        self._can_be_injured = can_be_injured # Self-explanatory. False for things like hair, etc.
        self._injury_level = injury_level # How injured is it? [0 - 3]

    @property
    def fullname(self):
        return self._fullname if self._fullname else self.key

    @property
    def plural_name(self):
        if self._plural_name:
            return self._plural_name

        return self.fullname + "s"

    @property
    def desc(self):
        if self.is_missing and not self.is_optional:
            return f"|R{self.player_they} have a missing {self.fullname}.|n"

        return self._desc

    @property
    def can_be_missing(self):
        return self._can_be_missing

    @property
    def is_missing(self):
        return self._is_missing if not self.can_be_missing else False

    @property
    def is_optional(self):
        return self._is_optional

    @property
    def is_covered(self):
        return self._is_covered if not self.is_missing else False

    @property
    def is_prosthetic(self):
        return self._is_prosthetic if not self.is_missing else False

    @property
    def is_inappropriate(self):
        return self._is_inappropriate if not self.is_missing else False

    @property
    def is_heavy(self):
        return self._is_heavy if not self.is_missing else False

    @property
    def can_be_injured(self):
        return self._can_be_injured

    @property
    def injury_level(self):
        if not self.can_be_injured:
            return 0

        if self.is_missing:
            return 4

        if self._injury_level < 0:
            return 0

        if self._injury_level > 3:
            return 3

        return self._injury_level