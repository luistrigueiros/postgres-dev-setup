from argparse import Namespace
from postgres_setup.commands import Command
from postgres_setup.core import PostgresDevSetup


class StatusCommand(Command):
    def __init__(self):
        super().__init__("status", "Show container status")

    def run(self, args: Namespace):
        """Show status of PostgreSQL container"""
        setup = PostgresDevSetup()
        print("📊 PostgreSQL Status\n")
        success, output = setup.run_command([
            "docker", "ps", "-a",
            "--filter", "name=dev-postgres",
            "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        ])

        if success:
            print(output)
        else:
            print("❌ Could not check status")
