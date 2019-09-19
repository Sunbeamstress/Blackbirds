r"""
Evennia settings file.

The available options are found in the default settings file found
here:

d:\evennia\evennia\evennia\settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

# Blackbirds extensions.
from server.conf import color_definitions as c

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Blackbirds"
GAME_SLOGAN = "For those who love the rain."

TELNET_ENABLED = True
TELNET_OOB_ENABLED = True

WEBSERVER_ENABLED = False
WEBCLIENT_ENABLED = False
WEBSOCKET_CLIENT_ENABLED = False

# Need to set this to whatever the host ends up being when it's time to go live.
# ALLOWED_HOSTS = "mercymyqueen.com"

MAX_CHAR_LIMIT = 10000

# Need to turn this off when game is live.
IN_GAME_ERRORS = True

COLOR_ANSI_EXTRA_MAP = [
    (r'|n', c.ANSI_NORMAL),

    (r'|R', c.A_RED),
    (r'|G', c.A_GREEN),
    (r'|Y', c.A_YELLOW),
    (r'|B', c.A_BLUE),
    (r'|M', c.A_MAGENTA),
    (r'|C', c.A_CYAN),
    (r'|W', c.A_WHITE),
    (r'|X', c.A_GREY),

    (r'|r', c.A_DARKRED),
    (r'|g', c.A_DARKGREEN),
    (r'|y', c.A_DARKYELLOW),
    (r'|b', c.A_DARKBLUE),
    (r'|m', c.A_DARKMAGENTA),
    (r'|c', c.A_DARKCYAN),
    (r'|w', c.A_GREY),
    (r'|x', c.A_DARKGREY),

    # normal ANSI backgrounds
    (r'|_r', c.ANSI_BACK_RED),
    (r'|_g', c.ANSI_BACK_GREEN),
    (r'|_y', c.ANSI_BACK_YELLOW),
    (r'|_b', c.ANSI_BACK_BLUE),
    (r'|_m', c.ANSI_BACK_MAGENTA),
    (r'|_c', c.ANSI_BACK_CYAN),
    (r'|_w', c.ANSI_BACK_WHITE),    # light grey background
    (r'|_x', c.ANSI_BACK_BLACK)     # pure black background
]

COLOR_NO_DEFAULT = False

TIME_FACTOR = 1.0
TIME_GAME_EPOCH = 0
TIME_IGNORE_DOWNTIMES = True

MULTISESSION_MODE = 2
MAX_NR_CHARACTERS = 5

CLIENT_DEFAULT_WIDTH = 80
CLIENT_DEFAULT_HEIGHT = 45

######################################################################
# Typeclasses and other paths
######################################################################

# Server-side session class used.
SERVER_SESSION_CLASS = "evennia.server.serversession.ServerSession"

# These are paths that will be prefixed to the paths given if the
# immediately entered path fail to find a typeclass. It allows for
# shorter input strings. They must either base off the game directory
# or start from the evennia library.
TYPECLASS_PATHS = ["typeclasses", "evennia", "evennia.contrib", "evennia.contrib.tutorial_examples"]

# Typeclass for account objects (linked to a character) (fallback)
BASE_ACCOUNT_TYPECLASS = "typeclasses.accounts.Account"
# Typeclass and base for all objects (fallback)
BASE_OBJECT_TYPECLASS = "typeclasses.objects.Object"
# Typeclass for character objects linked to an account (fallback)
BASE_CHARACTER_TYPECLASS = "typeclasses.characters.Character"
# Typeclass for rooms (fallback)
BASE_ROOM_TYPECLASS = "typeclasses.rooms.Room"
# Typeclass for Exit objects (fallback).
BASE_EXIT_TYPECLASS = "typeclasses.exits.Exit"
# Typeclass for Channel (fallback).
BASE_CHANNEL_TYPECLASS = "typeclasses.channels.Channel"
# Typeclass for Scripts (fallback). You usually don't need to change this
# but create custom variations of scripts on a per-case basis instead.
BASE_SCRIPT_TYPECLASS = "typeclasses.scripts.Script"
# The default home location used for all objects. This is used as a
# fallback if an object's normal home location is deleted. Default
# is Limbo (#2).
DEFAULT_HOME = "#2"
# The start position for new characters. Default is Limbo (#2).
#  MULTISESSION_MODE = 0, 1 - used by default unloggedin create command
#  MULTISESSION_MODE = 2, 3 - used by default character_create command
START_LOCATION = "#2"
# Lookups of Attributes, Tags, Nicks, Aliases can be aggressively
# cached to avoid repeated database hits. This often gives noticeable
# performance gains since they are called so often. Drawback is that
# if you are accessing the database from multiple processes (such as
# from a website -not- running Evennia's own webserver) data may go
# out of sync between the processes. Keep on unless you face such
# issues.
TYPECLASS_AGGRESSIVE_CACHE = True

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
