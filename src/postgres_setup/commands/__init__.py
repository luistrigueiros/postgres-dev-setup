
import argparse
from typing import Optional

class Command:
    """Base class for commands."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def add_arguments(self, parser: argparse.ArgumentParser):
        """Add command-specific arguments to the parser."""
        pass

    def run(self, args: argparse.Namespace):
        """Execute the command."""
        raise NotImplementedError
