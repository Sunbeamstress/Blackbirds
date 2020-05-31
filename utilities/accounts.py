from evennia.server.sessionhandler import SESSION_HANDLER

def all_accounts():
    return SESSION_HANDLER.all_connected_accounts()

def all_accounts_limited(perm):
    return [acc for acc in SESSION_HANDLER.all_connected_accounts() if acc.check_permstring(perm)]