"""Info command - Show connection information."""

from .base import BaseCommand


class InfoCommand(BaseCommand):
    """Show connection information."""

    name = "info"
    description = "Show connection information"

    def execute(self) -> None:
        """Display connection information."""
        config = self.config_manager.load()

        print("\n" + "=" * 60)
        print("📋 Connection Information")
        print("=" * 60)
        print(f"  Host:     localhost (or 127.0.0.1)")
        print(f"  Port:     {config['port']}")
        print(f"  Database: {config['database']}")
        print(f"  User:     {config['user']}")
        print(f"  Password: {config['password']}")
        print(f"\n  Connection URI:")
        print(f"  postgresql://{config['user']}:{config['password']}@localhost:{config['port']}/{config['database']}")
        print(f"\n  JDBC URL (for IntelliJ):")
        print(f"  jdbc:postgresql://localhost:{config['port']}/{config['database']}")
        print(f"\n  For connection issues, run: ./pgctl test")
        print("=" * 60)
