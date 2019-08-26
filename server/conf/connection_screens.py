# -*- coding: utf-8 -*-
"""
Connection screen

This is the text to show the user when they first connect to the game (before
they log in).

To change the login screen in this module, do one of the following:

- Define a function `connection_screen()`, taking no arguments. This will be
  called first and must return the full string to act as the connection screen.
  This can be used to produce more dynamic screens.
- Alternatively, define a string variable in the outermost scope of this module
  with the connection string that should be displayed. If more than one such
  variable is given, Evennia will pick one of them at random.

The commands available to the user when the connection screen is shown
are defined in evennia.default_cmds.UnloggedinCmdSet. The parsing and display
of the screen is done by the unlogged-in "look" command.

"""

SCREEN = \
     '''
         |CB L A C K B I R D S|n
                 |B.-.|n
                |M/|n |xv|n |M\\|n        |xto create an account|n
               |M(|n|B/|n   |B\|n|M)|n       |Rcreate <username> <password>|n
              |c=|n|M'|n|c=|n|x"|n|c=|n|x"|n|c=|n|M'|n|c=|n
                |M'|n|B)|n |B(|n|M'|n        |xto log in|n
                 |M'w'|n         |Rconnect <username> <password>|n
     
         |xTo all my friends: Blood makes the blade holy!|n
                                           |x- Atmosphere|n
     '''

from django.conf import settings
from evennia import utils

def connection_screen():
     game_name = settings.SERVERNAME
     evennia_version = utils.get_evennia_version("short")

     s = f"         |x{game_name} powered by Evennia v{evennia_version}.|n"
     s += f"\n\n{SCREEN}"
     return s