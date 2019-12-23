# Evennia modules.
from evennia.server.sessionhandler import SESSION_HANDLER

# Blackbirds modules.
from utilities.string import autoformat, jleft, jright, wrap

def notify(title, string):
    """
    Represents standardized and generic OOC messages from the game, most often
    used during system reloads, news updates, etc.
    """
    title = f"|c[|C{title}|c]:|n "
    output_string = title + string
    return output_string

def divider(width = 80, color = "B", indent = 0, symbol = "-"):
    width -= indent * 2
    return "%s|%s%s|n" % (" " * indent, color, symbol * width)

def header(title, width = 80, color = "B", title_color = "W", indent = 0, symbol = "-"):
    color = str(color)
    title_color = str(title_color)
    width -= 4 + len(title) + (indent * 2)

    if not title:
        return divider(width, color, indent, symbol)

    return "%s|%s%s |%s%s |%s%s|n" % (" " * indent, color, symbol * 2, title_color, title, color, symbol * width)

def column(title, value, title_width = None, value_width = None, indent = 2, title_color = "x", value_color = "w", col_color = "c"):
    title_width = title_width if title_width else len(str(title))
    value_width = value_width if value_width else len(str(value))

    title = str(title)
    value = str(value)

    string = "%s|%s%s|n |%s|||n |%s%s|n" % (" " * indent, title_color, jright(title, title_width), col_color, value_color, jleft(value, value_width))

    return string

def bullet(string, width = 80, color = "c", indent = 1):
    prefix = "%s|%s-|n " % (" " * indent, color)
    if not string:
        return prefix

    string = wrap(prefix + string, initial_indent = indent, subsequent_indent = 2 + indent)

    return string

def gecho(string):
    players = [acc.echo(f"{autoformat(string)}") for acc in SESSION_HANDLER.all_connected_accounts()]