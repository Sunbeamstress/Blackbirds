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

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Blackbirds"
GAME_SLOGAN = "For those who love the rain."

TELNET_ENABLED = True
TELNET_OOB_ENABLED = True
# Need to set this to whatever the host ends up being when it's time to go live.
# ALLOWED_HOSTS = "mercymyqueen.com"

MAX_CHAR_LIMIT = 10000

_ANSI_UNDERLINE = "\033[4m"
_ANSI_HILITE = "\033[1m"
_ANSI_UNHILITE = "\033[22m"
_ANSI_BLACK = "\033[30m"
_ANSI_RED = "\033[31m"
_ANSI_GREEN = "\033[32m"
_ANSI_YELLOW = "\033[33m"
_ANSI_BLUE = "\033[34m"
_ANSI_MAGENTA = "\033[35m"
_ANSI_CYAN = "\033[36m"
_ANSI_WHITE = "\033[37m"
_ANSI_BACK_BLACK = "\033[40m"
_ANSI_BACK_RED = "\033[41m"
_ANSI_BACK_GREEN = "\033[42m"
_ANSI_BACK_YELLOW = "\033[43m"
_ANSI_BACK_BLUE = "\033[44m"
_ANSI_BACK_MAGENTA = "\033[45m"
_ANSI_BACK_CYAN = "\033[46m"
_ANSI_BACK_WHITE = "\033[47m"

COLOR_ANSI_EXTRA_MAP = [
    (r'|R', _ANSI_HILITE + _ANSI_RED),
    (r'|G', _ANSI_HILITE + _ANSI_GREEN),
    (r'|Y', _ANSI_HILITE + _ANSI_YELLOW),
    (r'|B', _ANSI_HILITE + _ANSI_BLUE),
    (r'|M', _ANSI_HILITE + _ANSI_MAGENTA),
    (r'|C', _ANSI_HILITE + _ANSI_CYAN),
    (r'|W', _ANSI_HILITE + _ANSI_WHITE),  # pure white
    (r'|X', _ANSI_HILITE + _ANSI_BLACK),  # dark grey

    (r'|r', _ANSI_HILITE + _ANSI_RED),
    (r'|g', _ANSI_HILITE + _ANSI_GREEN),
    (r'|y', _ANSI_HILITE + _ANSI_YELLOW),
    (r'|b', _ANSI_HILITE + _ANSI_BLUE),
    (r'|m', _ANSI_HILITE + _ANSI_MAGENTA),
    (r'|c', _ANSI_HILITE + _ANSI_CYAN),
    (r'|w', _ANSI_HILITE + _ANSI_WHITE),  # light grey
    (r'|x', _ANSI_HILITE + _ANSI_BLACK),  # pure black

    # hilight-able colors
    (r'|H', _ANSI_HILITE),
    (r'|h', _ANSI_UNHILITE),

    # normal ANSI backgrounds
    (r'|[r', _ANSI_BACK_RED),
    (r'|[g', _ANSI_BACK_GREEN),
    (r'|[y', _ANSI_BACK_YELLOW),
    (r'|[b', _ANSI_BACK_BLUE),
    (r'|[m', _ANSI_BACK_MAGENTA),
    (r'|[c', _ANSI_BACK_CYAN),
    (r'|[w', _ANSI_BACK_WHITE),    # light grey background
    (r'|[x', _ANSI_BACK_BLACK),     # pure black background
]

COLOR_NO_DEFAULT = True

TIME_FACTOR = 1.0
TIME_GAME_EPOCH = 0
TIME_IGNORE_DOWNTIMES = True

MULTISESSION_MODE = 2
MAX_NR_CHARACTERS = 5

CLIENT_DEFAULT_WIDTH = 0
CLIENT_DEFAULT_HEIGHT = 45


######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
