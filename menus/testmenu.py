import random

def _action_two(caller, raw_string, **kwargs):
    num = str(random.randint(1, 1000000))
    return "node_test_two", {"testnum": num}

def node_test(caller, raw_string, **kwargs):
    text = "I'm a test menu, holy shit."
    options = (
        {"desc": "Test option one.", "goto": ("node_test_one")},
        {"desc": "Test option two.", "goto": (_action_two)},
        {"desc": "dumby option", "goto": None},
        {"desc": "dumby option", "goto": None},
        {"desc": "dumby option", "goto": None},
        {"desc": "dumby option", "goto": None},
        {"desc": "dumby option", "goto": None},
        {"desc": "dumby option", "goto": None},
        {"desc": "dumby option", "goto": None},
        {"desc": "dumby option", "goto": None},
        {"desc": "dumby option", "goto": None},
        {"desc": "dumby option", "goto": None},
        {"desc": "dumby option", "goto": None},
        {"desc": "dumby option", "goto": None},
    )

    return text, options

def node_test_one(caller, raw_string, **kwargs):
    text = "Nice job, derpus."
    options = (
        {"key": ("|M1|n", "1", "one"), "desc": "go baaaaack", "goto": ("node_test")},
    )

    return text, options

def node_test_two(caller, raw_string, **kwargs):
    num = kwargs.get("testnum", None)

    text = "This should be the one that had a random number. Let's see... "
    text += num if num else "nope, something went wrong!"
    options = (
        {"key": ("|M1|n", "1", "one"), "desc": "go baaaaack", "goto": ("node_test")},
    )

    return text, options