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

# ANSI definitions

ANSI_BEEP = "\07"
ANSI_ESCAPE = "\033"
ANSI_NORMAL = "\033[0m"

ANSI_UNDERLINE = "\033[4m"
ANSI_HILITE = "\033[1m"
ANSI_UNHILITE = "\033[22m"
ANSI_BLINK = "\033[5m"
ANSI_INVERSE = "\033[7m"
ANSI_INV_HILITE = "\033[1;7m"
ANSI_INV_BLINK = "\033[7;5m"
ANSI_BLINK_HILITE = "\033[1;5m"
ANSI_INV_BLINK_HILITE = "\033[1;5;7m"

# Foreground colors
ANSI_BLACK = "\033[30m"
ANSI_RED = "\033[31m"
ANSI_GREEN = "\033[32m"
ANSI_YELLOW = "\033[33m"
ANSI_BLUE = "\033[34m"
ANSI_MAGENTA = "\033[35m"
ANSI_CYAN = "\033[36m"
ANSI_WHITE = "\033[37m"

# Background colors
ANSI_BACK_BLACK = "\033[40m"
ANSI_BACK_RED = "\033[41m"
ANSI_BACK_GREEN = "\033[42m"
ANSI_BACK_YELLOW = "\033[43m"
ANSI_BACK_BLUE = "\033[44m"
ANSI_BACK_MAGENTA = "\033[45m"
ANSI_BACK_CYAN = "\033[46m"
ANSI_BACK_WHITE = "\033[47m"

# Formatting Characters
ANSI_RETURN = "\r\n"
ANSI_TAB = "\t"
ANSI_SPACE = " "

# Escapes
ANSI_ESCAPES = ("{{", "\\\\", "\|\|")

COLOR_ANSI_EXTRA_MAP = [

    # alternative |-format

    (r'|n', ANSI_NORMAL),          # reset
    (r'|/', ANSI_RETURN),          # line break
    (r'|-', ANSI_TAB),             # tab
    (r'|_', ANSI_SPACE),           # space
    (r'|*', ANSI_INVERSE),         # invert

    (r'|R', ANSI_HILITE + ANSI_RED),
    (r'|G', ANSI_HILITE + ANSI_GREEN),
    (r'|Y', ANSI_HILITE + ANSI_YELLOW),
    (r'|B', ANSI_HILITE + ANSI_BLUE),
    (r'|M', ANSI_HILITE + ANSI_MAGENTA),
    (r'|C', ANSI_HILITE + ANSI_CYAN),
    (r'|W', ANSI_HILITE + ANSI_WHITE),
    (r'|X', ANSI_UNHILITE + ANSI_WHITE),

    (r'|r', ANSI_UNHILITE + ANSI_RED),
    (r'|g', ANSI_UNHILITE + ANSI_GREEN),
    (r'|y', ANSI_UNHILITE + ANSI_YELLOW),
    (r'|b', ANSI_UNHILITE + ANSI_BLUE),
    (r'|m', ANSI_UNHILITE + ANSI_MAGENTA),
    (r'|c', ANSI_UNHILITE + ANSI_CYAN),
    (r'|w', ANSI_UNHILITE + ANSI_WHITE),
    (r'|x', ANSI_HILITE + ANSI_BLACK),

    # hilight-able colors
    (r'|H', ANSI_HILITE),
    (r'|h', ANSI_UNHILITE),

    (r'|!r', ANSI_RED),
    (r'|!g', ANSI_GREEN),
    (r'|!y', ANSI_YELLOW),
    (r'|!b', ANSI_BLUE),
    (r'|!m', ANSI_MAGENTA),
    (r'|!c', ANSI_CYAN),
    (r'|!w', ANSI_WHITE),  # light grey
    (r'|!x', ANSI_BLACK),  # pure black

    # normal ANSI backgrounds
    (r'|[r', ANSI_BACK_RED),
    (r'|[g', ANSI_BACK_GREEN),
    (r'|[y', ANSI_BACK_YELLOW),
    (r'|[b', ANSI_BACK_BLUE),
    (r'|[m', ANSI_BACK_MAGENTA),
    (r'|[c', ANSI_BACK_CYAN),
    (r'|[w', ANSI_BACK_WHITE),    # light grey background
    (r'|[x', ANSI_BACK_BLACK)     # pure black background
]

COLOR_NO_DEFAULT = True

TIME_FACTOR = 1.0
TIME_GAME_EPOCH = 0
TIME_IGNORE_DOWNTIMES = True

MULTISESSION_MODE = 2
MAX_NR_CHARACTERS = 5

CLIENT_DEFAULT_WIDTH = 80
CLIENT_DEFAULT_HEIGHT = 45


######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
