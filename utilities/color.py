def color_ramp(cur_val, max_val, cap = False):
    """Creates a gradient from green to red, based on the values passed to it.
    
    Returns an XTERM color number sequence."""
    perc = (cur_val * 100) / max_val
    color = None
    r, g = None, None

    if cur_val >= max_val and cap == True:
        color = "135"
    else:
        g = 5 if perc > 50 else round((perc * 2) / 20)
        r = 5 if perc < 50 else round(5 - (((perc - 50) * 2) / 20))

        g = 5 if g > 5 else g
        g = 0 if g < 0 else g
        r = 5 if r > 5 else r
        r = 0 if r < 0 else r

        color = f"{r}{g}0"

    return color