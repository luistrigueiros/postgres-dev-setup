
from argparse import Namespace

from . import Command


class DestroyCommand(Command):
    def __init__(self):
        super().__init__("destroy", "Stop and remove all data (⚠️  destructive)")

    def run(self, args: Namespace):
        """Stop and remove all data"""
        confirm = input("⚠️  This will DELETE ALL DATA. Type 'yes' to confirm: ")
        if confirm.lower() != 'yes':
            print("❌ Aborted")
            return

        print("💥 Destroying PostgreSQL (including data)...")
        success, output = self.run_command(["docker-compose", "down", "-v"], use_build_root=True)

        if success:
            print("✓ PostgreSQL destroyed (all data removed)")
            print("  Run 'setup' and 'start' again to recreate")
        else:
            print(f"❌ Failed to destroy: {output}")
