"""Backup command - Backup PostgreSQL database."""

from datetime import datetime
from pathlib import Path
from .base import BaseCommand


class BackupCommand(BaseCommand):
    """Backup PostgreSQL database."""

    name = "backup"
    description = "Create database backup"

    def execute(self) -> None:
        """Create database backup."""
        print("💾 Creating backup...")

        config = self.config_manager.load()

        # Create backup directory
        backup_dir = self.project_root / "backups"
        backup_dir.mkdir(exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"backup_{timestamp}.sql"

        # Run pg_dump
        success, output = self.docker.exec_command(
            config['container_name'],
            [
                "pg_dump",
                "-U", config['user'],
                "-d", config['database'],
                "-f", f"/tmp/backup_{timestamp}.sql"
            ]
        )

        if success:
            # Copy from container to host
            self.docker.run_command([
                "docker", "cp",
                f"{config['container_name']}:/tmp/backup_{timestamp}.sql",
                str(backup_file)
            ])
            self.print_success(f"Backup saved to {backup_file}")
        else:
            self.print_error(f"Backup failed: {output}")