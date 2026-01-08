"""Command registry - automatically discovers and registers all commands."""

import importlib
import inspect
from pathlib import Path
from typing import Dict, Type

from .base import BaseCommand


def discover_commands() -> Dict[str, Type[BaseCommand]]:
    """
    Automatically discover all command classes in the commands directory.

    This allows adding new commands by simply creating a new file with a
    command class that inherits from BaseCommand.
    """
    commands: Dict[str, Type[BaseCommand]] = {}

    # Get the commands directory
    commands_dir = Path(__file__).parent

    # Iterate through all Python files in commands directory
    for file_path in commands_dir.glob("*.py"):
        # Skip __init__.py and base.py
        if file_path.name in ("__init__.py", "base.py"):
            continue

        # Import the module
        module_name = file_path.stem
        try:
            module = importlib.import_module(f".{module_name}", package=__package__)

            # Find all classes that inherit from BaseCommand
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, BaseCommand) and
                        obj is not BaseCommand and
                        hasattr(obj, 'name') and
                        obj.name):
                    commands[obj.name] = obj
        except Exception as e:
            print(f"Warning: Could not load command from {module_name}: {e}")

    return commands


# Export for easy importing
__all__ = ["BaseCommand", "discover_commands"]