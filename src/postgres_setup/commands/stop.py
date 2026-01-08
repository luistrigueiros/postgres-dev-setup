"""Stop command - Stop PostgreSQL container."""

from .base import BaseCommand


class StopCommand(BaseCommand):
    """Stop PostgreSQL container."""

    name = "stop"
    description = "Stop PostgreSQL container"

    def execute(self) -> None:
        """Stop PostgreSQL container."""
        print("🛑 Stopping PostgreSQL...")

        success, output = self.docker.compose_down()

        if success:
            self.print_success("PostgreSQL stopped (data preserved)")
        else:
            self.print_error(f"Failed to stop: {output}")