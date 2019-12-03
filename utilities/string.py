# Python modules.
import re, inflect

# Evennia modules.
from evennia.utils import ansi

def capital(s):
    "Capitalizes the first letter of the string. Differs from Python capitalize() in that it will not perform operations on the rest of the string."
    return "%s%s" % (s[0].upper(), s[1:])

def punctuate(s):
    s = ansi.strip_ansi(s)
    punc = s[-1]
    if not punc in [".", ",", "'", '"', "(", ")", "!", "?", "-"]:
        s += "."

    return s

def autoformat(s):
    """
    Rudimentary formatting of speech and emoting.

    Capitalizes the first letter of the string, and intelligently auto-punctuates the end.
    """

    s = ansi.strip_ansi(s)

    s = capital(s)
    s = punctuate(s)

    s = s.replace("$p", "\n\n")
    s = s.replace("$n", "\n")

    return s

def jright(string, width = 0):
    string = str(string)
    string_len = len(ansi.strip_ansi(string))
    return (" " * (width - string_len)) + string

def jleft(string, width = 0):
    string = str(string)
    string_len = len(ansi.strip_ansi(string))
    return string + (" " * (width - string_len))

def sanitize(string):
    "Removes all extraneous characters and control codes from the string."
    # For now, just removes newlines and whitespace, but will be used later to remove
    # any form of potentially sensitive input.
    string = string.strip("\n")
    string = string.rstrip()
    string = string.lstrip()
    return string

def an(string, capitalize = False):
    "Prefixes a string with 'a ' or 'an ' where appropriate. Pass 'capitalize == True' to capitalize the article."
    inf = inflect.engine()
    string = capital(inf.a(string)) if capitalize == True else inf.a(string)

    return string

def ord(string):
    "Returns the ordinal (1 --> 1st) of the string. You can also pass numbers."
    inf = inflect.engine()
    return inf.ordinal(string)

def wrap(string, width = 80, initial_indent = 0, subsequent_indent = 0):
    str_list = string.split()
    str_list.insert(0, " " * initial_indent)

    output_list = []
    output_string = ""
    cur_len = 0

    for i, word in enumerate(str_list):
        space = " " if i > 1 else ""
        cur_len += len(ansi.strip_ansi(word))
        if i > 1:
            cur_len += 1
        if cur_len <= width:
            output_string += space + word
        else:
            output_list.append(output_string)
            cur_len = len(ansi.strip_ansi(word)) + subsequent_indent
            output_string = (" " * subsequent_indent) + word

    output_list.append(output_string)

    return "\n".join(output_list)

def plural(string):
    inf = inflect.engine()
    inf.classical(ancient = True)
    return inf.plural(string)

def message_token_pluralize(string, token, tar):
    reg = re.search(r"(" + token + "\w+)", string)
    if reg:
        found_words = reg.groups()
        for word in found_words:
            tar_word = word[1:]
            string = string.replace(word, tar.pluralize(tar_word))

    return string

def message_token_capitalize(string):
    reg = re.search(r"(\+\w+)", string)
    if reg:
        found_words = reg.groups()
        for word in found_words:
            tar_word = word[1:]
            string = string.replace(word, capital(tar_word))

    return string