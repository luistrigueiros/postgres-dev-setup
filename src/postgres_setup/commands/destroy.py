"""Destroy command - Stop and remove all data."""

import sys
from .base import BaseCommand


class DestroyCommand(BaseCommand):
    """Stop and remove all PostgreSQL data."""

    name = "destroy"
    description = "Stop and remove all data (⚠️  destructive)"

    def execute(self) -> None:
        """Stop and remove all data."""
        confirm = input("⚠️  This will DELETE ALL DATA. Type 'yes' to confirm: ")
        if confirm.lower() != 'yes':
            self.print_error("Aborted")
            return

        print("💥 Destroying PostgreSQL (including data)...")
        success, output = self.docker.compose_down(remove_volumes=True)

        if success:
            self.print_success("PostgreSQL destroyed (all data removed)")
            print("  Run './pgctl setup && ./pgctl start' to recreate")
        else:
            self.print_error(f"Failed to destroy: {output}")
            sys.exit(1)