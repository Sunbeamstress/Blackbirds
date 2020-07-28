from evennia import create_object

from typeclasses.objects import Object
from utilities.string import jleft, jright, sanitize

def creation_admin_base(caller, raw_string, **kwargs):
    text = "Choose one of the following options."

    options = (
        {"desc": "Nothin' yet, sorry!", "goto": None},
    )

    return text, options