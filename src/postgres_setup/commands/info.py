
from argparse import Namespace
from . import Command


class InfoCommand(Command):
    def __init__(self):
        super().__init__("info", "Show connection information")

    def run(self, args: Namespace):
        """Display connection information"""
        self.show_connection_info()
