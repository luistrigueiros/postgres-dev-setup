"""Start command - Start PostgreSQL container."""

import sys
from .base import BaseCommand


class StartCommand(BaseCommand):
    """Start PostgreSQL container."""

    name = "start"
    description = "Start PostgreSQL container"

    def execute(self) -> None:
        """Start PostgreSQL container."""
        print("🐘 Starting PostgreSQL...")

        success, output = self.docker.compose_up()

        if not success:
            self.print_error(f"Failed to start: {output}")
            sys.exit(1)

        self.print_success("PostgreSQL container started")
        print("\n⏳ Waiting for PostgreSQL to be healthy...")

        config = self.config_manager.load()
        is_healthy = self.docker.wait_for_healthy(
            config['container_name'],
            config['user']
        )

        if is_healthy:
            print("\n✅ PostgreSQL is ready!")
            self._show_connection_info()
            self._show_extensions()
        else:
            print("\n⚠️  PostgreSQL may still be starting.")
            print("Check with: ./pgctl logs")

    def _show_connection_info(self) -> None:
        """Display connection information."""
        config = self.config_manager.load()
        print("\n" + "=" * 60)
        print("📋 Connection Information")
        print("=" * 60)
        print(f"  Host:     localhost")
        print(f"  Port:     {config['port']}")
        print(f"  Database: {config['database']}")
        print(f"  User:     {config['user']}")
        print(f"  Password: {config['password']}")
        print(f"\n  Connection URI:")
        print(f"  postgresql://{config['user']}:{config['password']}@localhost:{config['port']}/{config['database']}")
        print(f"\n  JDBC URL (for IntelliJ):")
        print(f"  jdbc:postgresql://localhost:{config['port']}/{config['database']}")
        print("=" * 60)

    def _show_extensions(self) -> None:
        """Show installed extensions."""
        config = self.config_manager.load()
        success, output = self.docker.exec_command(
            config['container_name'],
            [
                "psql", "-U", config['user'], "-d", config['database'],
                "-c", "SELECT extname, extversion FROM pg_extension ORDER BY extname;"
            ]
        )

        if success:
            print("\n📦 Installed Extensions:")
            print(output)