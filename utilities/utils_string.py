# Evennia modules.
from evennia.utils import ansi

def AutoCap(s):
    s = ansi.strip_ansi(s)
    return "%s%s" % (s[0].upper(), s[1:])

def AutoPunc(s):
    s = ansi.strip_ansi(s)
    punc = s[-1]
    if not punc in [".", ",", "'", '"', "(", ")", "!", "?", "-"]:
        s += "."

    return s

def RPFormat(s):
    """
    Rudimentary formatting of speech and emoting.

    Capitalizes the first letter of the string, and intelligently auto-punctuates the end.
    """

    s = ansi.strip_ansi(s)

    s = AutoCap(s)
    s = AutoPunc(s)

    s = s.replace("$p", "\n\n")
    s = s.replace("$n", "\n")

    return s

def jright(string, width = 0):
    string_len = len(ansi.strip_ansi(string))
    s = " "
    return (s * (width - string_len)) + string

def jleft(string, width = 0):
    string_len = len(ansi.strip_ansi(string))
    s = " "
    return string + (s * (width - string_len))