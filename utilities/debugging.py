from evennia.server.sessionhandler import SESSION_HANDLER

def debug_echo(string):
    "Displays a message to everyone online with the permission to see it. Use responsibly."
    devs = [acc.echo(f"|r[|RD|r]:|n {string}") for acc in SESSION_HANDLER.all_connected_accounts() if acc.check_permstring("Developer")]