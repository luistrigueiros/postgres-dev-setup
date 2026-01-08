"""Restart command - Restart PostgreSQL container."""

import time
from .base import BaseCommand
from .stop import StopCommand
from .start import StartCommand


class RestartCommand(BaseCommand):
    """Restart PostgreSQL container."""

    name = "restart"
    description = "Restart PostgreSQL container"

    def execute(self) -> None:
        """Restart PostgreSQL container."""
        print("🔄 Restarting PostgreSQL...")

        # Use existing stop and start commands
        stop_cmd = StopCommand(self.project_root)
        stop_cmd.execute()

        time.sleep(2)

        start_cmd = StartCommand(self.project_root)
        start_cmd.execute()
