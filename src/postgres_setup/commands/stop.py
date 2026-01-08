
from argparse import Namespace
from postgres_setup.commands import Command
from postgres_setup.core import PostgresDevSetup


class StopCommand(Command):
    def __init__(self):
        super().__init__("stop", "Stop PostgreSQL container")

    def run(self, args: Namespace):
        """Stop PostgreSQL container"""
        setup = PostgresDevSetup()
        print("🛑 Stopping PostgreSQL...")
        success, output = setup.run_command(["docker-compose", "down"])

        if success:
            print("✓ PostgreSQL stopped (data preserved)")
        else:
            print(f"❌ Failed to stop: {output}")
