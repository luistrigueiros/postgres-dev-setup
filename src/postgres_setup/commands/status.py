from argparse import Namespace

from . import Command


class StatusCommand(Command):
    def __init__(self):
        super().__init__("status", "Show container status")

    def run(self, args: Namespace):
        """Show status of PostgreSQL container"""
        print("📊 PostgreSQL Status\n")
        success, output = self.run_command([
            "docker", "ps", "-a",
            "--filter", "name=dev-postgres",
            "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        ])

        if success:
            print(output)
        else:
            print("❌ Could not check status")
