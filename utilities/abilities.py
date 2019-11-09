from typeclasses.abilities import Ability

def ability_list():
    """
    Returns a dictionary of all defined abilities in the game, formatted as follows:
        ability_key = {"name": name, "description": description}
    """
    ab_list = {}
    for ab in Ability.__subclasses__():
        a = ab()
        ab_list[a.key] = {"name": a.name, "description": a.description(), "tiers": a.tiers}

    return ab_list

def ability_search(ab):
    """
    Accepts any name and attempts to return a valid ability key, whether by supplied key or by full name.
    """
    ab = ab.lower()

    ab_list = ability_list()
    if ab in ab_list.keys():
        # Already have a key, no need to continue.
        return ab

    for a in ab_list.keys():
        if ab == ab_list[a]["name"].lower():
            # Found the name, return the key.
            return a

    return None

def get_ability_name(ab):
    ab = ability_search(ab)
    ab_list = ability_list()
    return ab_list[ab]["name"] if ab in ab_list else None

def get_ability_description(ab):
    ab = ability_search(ab)
    ab_list = ability_list()
    return ab_list[ab]["description"] if ab in ab_list else None

def get_ability_tiers(ab):
    ab = ability_search(ab)
    ab_list = ability_list()
    return ab_list[ab]["tiers"] if ab in ab_list else None