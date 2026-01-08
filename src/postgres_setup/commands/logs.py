from argparse import Namespace
from postgres_setup.commands import Command
from postgres_setup.core import PostgresDevSetup


class LogsCommand(Command):
    def __init__(self):
        super().__init__("logs", "Show PostgreSQL logs")

    def run(self, args: Namespace):
        """Show PostgreSQL logs"""
        setup = PostgresDevSetup()
        print("📜 Showing PostgreSQL logs (Ctrl+C to exit)...\n")
        setup.run_command(["docker-compose", "logs", "-f", "postgres"], capture_output=False)
