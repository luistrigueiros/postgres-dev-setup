#!/usr/bin/env python3
"""
PostgreSQL Development Environment CLI
Usage: uv run python src/postgres_setup/cli.py [command]
"""

import sys
from pathlib import Path

from .commands import discover_commands


def main():
    """Main CLI entry point."""
    # Discover all available commands
    commands = discover_commands()

    # Check if command provided
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print("PostgreSQL Development Environment Manager")
        print("\nUsage: ./pgctl [command]")
        print("\nAvailable commands:")

        # Sort commands alphabetically for better UX
        for cmd_name in sorted(commands.keys()):
            cmd_class = commands[cmd_name]
            print(f"  {cmd_name:12} - {cmd_class.get_description()}")

        sys.exit(1)

    # Get command name and instantiate command class
    command_name = sys.argv[1]
    command_class = commands[command_name]

    # Auto-detect project root
    project_root = Path(__file__).parent.parent.parent

    # Execute command
    try:
        command = command_class(project_root)
        command.execute()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error executing command: {e}")
        if "--debug" in sys.argv:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()