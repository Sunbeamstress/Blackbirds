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
# Need to set this to whatever the host ends up being when it's time to go live.
# ALLOWED_HOSTS = "mercymyqueen.com"

MAX_CHAR_LIMIT = 10000

COLOR_ANSI_EXTRA_MAP = [
    (r'`n', c.ANSI_NORMAL),          # reset
    (r'|n', c.ANSI_NORMAL),

    (r'`R', c.A_RED),
    (r'`G', c.A_GREEN),
    (r'`Y', c.A_YELLOW),
    (r'`B', c.A_BLUE),
    (r'`M', c.A_MAGENTA),
    (r'`C', c.A_CYAN),
    (r'`W', c.A_WHITE),
    (r'`X', c.A_GREY),

    (r'`r', c.A_DARKRED),
    (r'`g', c.A_DARKGREEN),
    (r'`y', c.A_DARKYELLOW),
    (r'`b', c.A_DARKBLUE),
    (r'`m', c.A_DARKMAGENTA),
    (r'`c', c.A_DARKCYAN),
    (r'`w', c.A_GREY),
    (r'`x', c.A_DARKGREY),

    # normal ANSI backgrounds
    (r'`_r', c.ANSI_BACK_RED),
    (r'`_g', c.ANSI_BACK_GREEN),
    (r'`_y', c.ANSI_BACK_YELLOW),
    (r'`_b', c.ANSI_BACK_BLUE),
    (r'`_m', c.ANSI_BACK_MAGENTA),
    (r'`_c', c.ANSI_BACK_CYAN),
    (r'`_w', c.ANSI_BACK_WHITE),    # light grey background
    (r'`_x', c.ANSI_BACK_BLACK)     # pure black background
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
