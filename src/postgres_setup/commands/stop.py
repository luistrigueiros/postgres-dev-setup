
from argparse import Namespace
from . import Command


class StopCommand(Command):
    def __init__(self):
        super().__init__("stop", "Stop PostgreSQL container")

    def run(self, args: Namespace):
        """Stop PostgreSQL container"""
        print("🛑 Stopping PostgreSQL...")
        success, output = self.run_command(["docker-compose", "down"], use_build_root=True)

        if success:
            print("✓ PostgreSQL stopped (data preserved)")
        else:
            print(f"❌ Failed to stop: {output}")
