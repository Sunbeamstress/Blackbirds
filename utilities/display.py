# Evennia modules.
from evennia.server.sessionhandler import SESSION_HANDLER

# Blackbirds modules.
from utilities.string import autoformat, jleft, jright, wrap

# For use with the color chart.
_LETTER_MAP = {
    "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9, "k": 10, "l": 11, "m": 12,
    "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25
}

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

def color_chart():
    chart = [
        ["000", "010", "020", "030", "040", "050", "150", "140", "130", "120", "110", "100"],
        ["001", "011", "021", "031", "041", "051", "151", "141", "131", "121", "111", "101"],
        ["002", "012", "022", "032", "042", "052", "152", "142", "132", "122", "112", "102"],
        ["003", "013", "023", "033", "043", "053", "153", "143", "133", "123", "113", "103"],
        ["004", "014", "024", "034", "044", "054", "154", "144", "134", "124", "114", "104"],
        ["005", "015", "025", "035", "045", "055", "155", "145", "135", "125", "115", "105"],
        ["205", "215", "225", "235", "245", "255", "355", "345", "335", "325", "315", "305"],
        ["204", "214", "224", "234", "244", "254", "354", "344", "334", "324", "314", "304"],
        ["203", "213", "223", "233", "243", "253", "353", "343", "333", "323", "313", "303"],
        ["202", "212", "222", "232", "242", "252", "352", "342", "332", "322", "312", "302"],
        ["201", "211", "221", "231", "241", "251", "351", "341", "331", "321", "311", "301"],
        ["200", "210", "220", "230", "240", "250", "350", "340", "330", "320", "310", "300"],
        ["400", "410", "420", "430", "440", "450", "550", "540", "530", "520", "510", "500"],
        ["401", "411", "421", "431", "441", "451", "551", "541", "531", "521", "511", "501"],
        ["402", "412", "422", "432", "442", "452", "552", "542", "532", "522", "512", "502"],
        ["403", "413", "423", "433", "443", "453", "553", "543", "533", "523", "513", "503"],
        ["404", "414", "424", "434", "444", "454", "554", "544", "534", "524", "514", "504"],
        ["405", "415", "425", "435", "445", "455", "555", "545", "535", "525", "515", "505"],
    ]
    gs_chart = [
        ["=a", "=b", "=c", "=d", "=e", "=f", "=g", "=h", "=i", "=j", "=k", "=l", "=m"],
        ["=n", "=o", "=p", "=q", "=r", "=s", "=t", "=u", "=v", "=w", "=x", "=y", "=z"],
    ]
    formatted_chart = ""
    newline = True

    for row in chart:
        newline = True
        for col in row:
            cell = col
            gamma = int(cell[0]) + int(cell[1]) + int(cell[2])
            fgcolor = "555" if gamma <= 8 else "000"
            cellstring = None
            if newline:
                cellstring = "\n"
                newline = False
            else:
                cellstring = " "
            cellstring += f"|[{cell}|{fgcolor}{cell}|n"
            formatted_chart += cellstring

    formatted_chart += "\n"

    for row in gs_chart:
        newline = True
        for col in row:
            cell = col
            gamma = _LETTER_MAP[cell[1]]
            fgcolor = "555" if gamma <= 12 else "000"
            cellstring = None
            if newline:
                cellstring = "\n"
                newline = False
            else:
                cellstring = " "
            cellstring += f"|[{cell}|{fgcolor}{cell} |n"
            formatted_chart += cellstring

    return formatted_chart

def formatted_channel_msg(chan = None, acc = None, msg = None):
    if not chan or not acc or not msg:
        return

    acc_color = "W" if acc.is_superuser else "x"
    return f"|=j[|=o{chan}|=j]|n |{acc_color}{acc.name}:|n {msg}"