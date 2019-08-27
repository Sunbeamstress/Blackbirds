def AutoCap(s):
    return "%s%s" % (s[0].upper(), s[1:])

def AutoPunc(s):
    punc = s[-1]
    if not punc in [".", ",", "'", '"', "(", ")", "!", "?", "-"]:
        s += "."

    return s

def RPFormat(s):
    """
    Rudimentary formatting of speech and emoting.

    Capitalizes the first letter of the string, and intelligently auto-punctuates the end.
    """

    s = AutoCap(s)
    s = AutoPunc(s)

    s = s.replace("$p", "\n\n")
    s = s.replace("$n", "\n")

    return s

def jright(string, width = 0):
    s = " "
    return (s * (width - len(string))) + string

def jleft(string, width = 0):
    s = " "
    return string + (s * (width - len(string)))