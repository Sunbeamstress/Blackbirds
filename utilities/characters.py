from server.conf import settings
from utilities.accounts import all_accounts

typeclass = settings.BASE_CHARACTER_TYPECLASS

def name_is_taken(name):
    "Returns True if there is an existing character by the chosen name."
    from evennia.objects.models import ObjectDB
    if ObjectDB.objects.filter(db_typeclass_path = typeclass, db_key__iexact = name):
        return True

    return False

def all_characters():
    return [acc.character for acc in all_accounts()]