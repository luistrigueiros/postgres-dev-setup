
import argparse
import json
from pathlib import Path
from typing import Optional

class Command:
    """Base class for commands."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

        self.project_root = Path(__file__).parent.parent.parent
        self.config_file = self.project_root / "config" / "postgres-config.json"

    def default_config(self) -> dict:
        """Default PostgreSQL configuration"""
        return {
            "image": "postgres:16",
            "user": "devuser",
            "password": "devpass",
            "database": "devdb",
            "port": 5432,
            "extensions": [
                "pg_trgm",  # Text search
                "btree_gin",  # Additional index types
                "btree_gist",  # Additional index types
                "pgcrypto",  # Cryptographic functions
            ],
            "custom_types": [],
            "container_name": "dev-postgres",
        }

    def load_config(self) -> dict:
        """Load PostgreSQL configuration from JSON file"""
        if not self.config_file.exists():
            return self.default_config()

        with open(self.config_file) as f:
            return json.load(f)

    def add_arguments(self, parser: argparse.ArgumentParser):
        """Add command-specific arguments to the parser."""
        pass

    def run(self, args: argparse.Namespace):
        """Execute the command."""
        raise NotImplementedError
