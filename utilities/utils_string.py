import evennia

def RPFormat(s):
    """
    Rudimentary formatting of speech and emoting.

    Capitalizes the first letter of the string, and intelligently auto-punctuates the end.
    """

    s = "%s%s" % (s[0].upper(), s[1:])

    punc = s[-1]
    if not punc in [".", ",", "'", '"', "(", ")", "!", "?", "-"]:
        s += "."

    return s