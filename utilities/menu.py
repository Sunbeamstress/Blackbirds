from evennia.utils.evmenu import EvMenu
from evennia.utils.ansi import strip_ansi

from server.conf import settings
from utilities.utils_string import jright

class Menu(EvMenu):
    def nodetext_formatter(self, nodetext):
        """
        Format the node text itself.

        Args:
            nodetext (str): The full node text (the text describing the node).

        Returns:
            nodetext (str): The formatted node text.

        """
        return nodetext

    def helptext_formatter(self, helptext):
        """
        Format the node's help text

        Args:
            helptext (str): The unformatted help text for the node.

        Returns:
            helptext (str): The formatted help text.

        """
        return "|C" + helptext + "|n"

    def options_formatter(self, optionlist):
        """
        Formats the option block.

        Args:
            optionlist (list): List of (key, description) tuples for every
                option related to this node.
            caller (Object, Account or None, optional): The caller of the node.

        Returns:
            options (str): The formatted option display.

        """
        if not optionlist:
            return ""

        options = ""
        for key, desc in optionlist:
            key = "|513%s|n" % strip_ansi(key)
            key = jright(key, 3)
            sep = "|c|||n"
            desc = desc.replace("\n", "\n    |c|||n ")
            options += f"\n{key} {sep} {desc}"

        return options

    def node_formatter(self, nodetext, optionstext):
        """
        Formats the entirety of the node.

        Args:
            nodetext (str): The node text as returned by `self.nodetext_formatter`.
            optionstext (str): The options display as returned by `self.options_formatter`.
            caller (Object, Account or None, optional): The caller of the node.

        Returns:
            node (str): The formatted node to display.

        """
        return nodetext + "\n" + optionstext