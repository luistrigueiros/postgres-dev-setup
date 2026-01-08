"""Status command - Show PostgreSQL container status."""

from .base import BaseCommand


class StatusCommand(BaseCommand):
    """Show status of PostgreSQL container."""

    name = "status"
    description = "Show container status"

    def execute(self) -> None:
        """Show status of PostgreSQL container."""
        print("📊 PostgreSQL Status\n")

        config = self.config_manager.load()
        success, output = self.docker.get_container_status(
            config['container_name']
        )

        if success:
            print(output)
        else:
            self.print_error("Could not check status")