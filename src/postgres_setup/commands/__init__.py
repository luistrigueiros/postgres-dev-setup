
import argparse
import json
import subprocess
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

    def run_command(self, cmd: list[str], capture_output: bool = True) -> tuple[bool, str]:
        """Execute shell command and return success status and output"""
        try:
            if capture_output:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True,
                    cwd=self.project_root,
                )
                return True, result.stdout

            subprocess.run(cmd, check=True, cwd=self.project_root)
            return True, ""
        except subprocess.CalledProcessError as e:
            return False, e.stderr if capture_output else str(e)

    def show_connection_info(self):
        """Display connection information"""
        config = self.load_config()
        print("\n" + "=" * 60)
        print("📋 Connection Information")
        print("=" * 60)
        print("  Host:     localhost")
        print(f"  Port:     {config['port']}")
        print(f"  Database: {config['database']}")
        print(f"  User:     {config['user']}")
        print(f"  Password: {config['password']}")
        print("\n  Connection URI:")
        print(
            f"  postgresql://{config['user']}:{config['password']}@localhost:{config['port']}/{config['database']}"
        )
        print("=" * 60)

    def show_extensions(self):
        """Show installed extensions"""
        config = self.load_config()
        success, output = self.run_command(
            [
                "docker",
                "exec",
                config["container_name"],
                "psql",
                "-U",
                config["user"],
                "-d",
                config["database"],
                "-c",
                "SELECT extname, extversion FROM pg_extension ORDER BY extname;",
            ]
        )

        if success:
            print("\n📦 Installed Extensions:")
            print(output)

    def add_arguments(self, parser: argparse.ArgumentParser):
        """Add command-specific arguments to the parser."""
        pass

    def run(self, args: argparse.Namespace):
        """Execute the command."""
        raise NotImplementedError
