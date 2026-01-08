"""Psql command - Connect to PostgreSQL with psql."""

from .base import BaseCommand


class PsqlCommand(BaseCommand):
    """Connect to PostgreSQL with psql client."""

    name = "psql"
    description = "Connect with psql client"

    def execute(self) -> None:
        """Connect to PostgreSQL with psql."""
        config = self.config_manager.load()
        print(f"🔌 Connecting to {config['database']}...\n")

        self.docker.exec_command(
            config['container_name'],
            [
                "psql",
                "-U", config['user'],
                "-d", config['database']
            ],
            interactive=True
        )
