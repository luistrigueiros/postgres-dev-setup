"""Base command class for all PostgreSQL commands."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from ..config import Config
from ..docker_manager import DockerManager


class BaseCommand(ABC):
    """Base class for all commands."""

    # Override these in subclasses
    name: str = ""
    description: str = ""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize command with project root."""
        if project_root is None:
            # Auto-detect project root from this file's location
            project_root = Path(__file__).parent.parent.parent.parent

        self.project_root = project_root
        self.config_manager = Config(project_root)
        self.docker = DockerManager(project_root)

    @abstractmethod
    def execute(self) -> None:
        """Execute the command. Override in subclasses."""
        pass

    @classmethod
    def get_name(cls) -> str:
        """Get command name."""
        return cls.name

    @classmethod
    def get_description(cls) -> str:
        """Get command description."""
        return cls.description

    def print_success(self, message: str) -> None:
        """Print success message."""
        print(f"✓ {message}")

    def print_error(self, message: str) -> None:
        """Print error message."""
        print(f"✗ {message}")

    def print_info(self, message: str) -> None:
        """Print info message."""
        print(f"ℹ {message}")

    def print_warning(self, message: str) -> None:
        """Print warning message."""
        print(f"⚠️  {message}")