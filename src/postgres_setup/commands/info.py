
from argparse import Namespace
from postgres_setup.commands import Command
from postgres_setup.core import PostgresDevSetup


class InfoCommand(Command):
    def __init__(self):
        super().__init__("info", "Show connection information")

    def run(self, args: Namespace):
        """Display connection information"""
        setup = PostgresDevSetup()
        setup.show_connection_info()
