"""Restore command - Restore PostgreSQL database from backup."""

import sys
from pathlib import Path
from .base import BaseCommand


class RestoreCommand(BaseCommand):
    """Restore PostgreSQL database from backup."""

    name = "restore"
    description = "Restore database from backup"

    def execute(self) -> None:
        """Restore database from backup."""
        if len(sys.argv) < 3:
            self.print_error("Usage: ./pgctl restore <backup_file>")
            sys.exit(1)

        backup_file = Path(sys.argv[2])

        if not backup_file.exists():
            self.print_error(f"Backup file not found: {backup_file}")
            sys.exit(1)

        print(f"📥 Restoring from {backup_file}...")

        config = self.config_manager.load()

        # Copy backup to container
        success, _ = self.docker.run_command([
            "docker", "cp",
            str(backup_file),
            f"{config['container_name']}:/tmp/restore.sql"
        ])

        if not success:
            self.print_error("Failed to copy backup to container")
            sys.exit(1)

        # Restore using psql
        success, output = self.docker.exec_command(
            config['container_name'],
            [
                "psql",
                "-U", config['user'],
                "-d", config['database'],
                "-f", "/tmp/restore.sql"
            ]
        )

        if success:
            self.print_success("Restore completed successfully")
        else:
            self.print_error(f"Restore failed: {output}")