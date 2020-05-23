from evennia.server.sessionhandler import SESSION_HANDLER

def all_accounts():
    return SESSION_HANDLER.all_connected_accounts()