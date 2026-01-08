"""Logs command - Show PostgreSQL logs."""

from .base import BaseCommand


class LogsCommand(BaseCommand):
    """Show PostgreSQL logs."""

    name = "logs"
    description = "Show PostgreSQL logs"

    def execute(self) -> None:
        """Show PostgreSQL logs."""
        print("📜 Showing PostgreSQL logs (Ctrl+C to exit)...\n")
        self.docker.compose_logs("postgres")
