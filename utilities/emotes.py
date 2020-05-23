import re

def _extract_tokens(msg):
    return re.findall(msg, r"(@[\w_]+)")

def msg_tokenize(name, msg):
    # Replace all tokens directed to the character with first-person pronouns.
    msg = msg.replace(f"@{name}_they", "you")
    msg = msg.replace(f"@{name}_them", "you")
    msg = msg.replace(f"@{name}_their", "your")
    msg = msg.replace(f"@{name}_theirs", "yours")
    msg = msg.replace(f"@{name}", "you")

    # All other tokens are to be parsed with their own pronouns accordingly.
    # TODO: regex compilation of all tokens

    return msg