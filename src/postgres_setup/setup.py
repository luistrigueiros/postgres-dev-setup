#!/usr/bin/env python3
"""
PostgreSQL Development Environment Setup
Requires: uv, docker
Usage: uv run python src/postgres_setup/setup.py [command]
"""
import argparse
import importlib
import pkgutil
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from postgres_setup import commands

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="PostgreSQL Development Environment Manager"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Discover and load commands
    command_map = {}
    for _, name, _ in pkgutil.iter_modules(commands.__path__):
        module = importlib.import_module(f"postgres_setup.commands.{name}")
        for attr in dir(module):
            if attr.endswith("Command") and not attr.startswith("_") and attr != "Command":
                command_class = getattr(module, attr)
                command_instance = command_class()
                command_map[command_instance.name] = command_instance
                
                # Add subcommand parser
                cmd_parser = subparsers.add_parser(
                    command_instance.name,
                    help=command_instance.description,
                    description=command_instance.description,
                )
                command_instance.add_arguments(cmd_parser)

    # Parse arguments
    args = parser.parse_args()

    # Show help if no command is given
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute the command
    if args.command in command_map:
        command_map[args.command].run(args)
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()