"""Configuration management for PostgreSQL development environment."""

import json
from pathlib import Path
from typing import Dict, Any


class Config:
    """Manages PostgreSQL configuration."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.config_file = project_root / "config" / "postgres-config.json"
        self.compose_file = project_root / "docker-compose.yml"
        self.init_scripts_dir = project_root / "init-scripts"

    @staticmethod
    def default() -> Dict[str, Any]:
        """Return default PostgreSQL configuration."""
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
                "pgcrypto"  # Cryptographic functions
            ],
            "custom_types": [],
            "container_name": "dev-postgres"
        }

    def load(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        if not self.config_file.exists():
            return self.default()

        with open(self.config_file) as f:
            return json.load(f)

    def save(self, config: Dict[str, Any]) -> None:
        """Save configuration to JSON file."""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(config, indent=2, fp=f)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        config = self.load()
        return config.get(key, default)