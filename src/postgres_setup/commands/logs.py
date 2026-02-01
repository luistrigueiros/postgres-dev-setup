from argparse import Namespace

from . import Command


class LogsCommand(Command):
    def __init__(self):
        super().__init__("logs", "Show PostgreSQL logs")

    def run(self, args: Namespace):
        """Show PostgreSQL logs"""
        print("📜 Showing PostgreSQL logs (Ctrl+C to exit)...\n")
        self.run_command(["docker-compose", "logs", "-f", "postgres"], capture_output=False, use_build_root=True)
