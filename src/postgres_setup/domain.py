from typing import List

from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass


@dataclass(frozen=True, config=ConfigDict(extra="ignore"))
class PostgresConfig:
    image: str = Field(default="postgres:16")
    user: str = Field(default="devuser")
    password: str = Field(default="devpass")
    database: str = Field(default="devdb")
    port: int = Field(default=5432, ge=1, le=65535)
    extensions: List[str] = Field(default_factory=lambda: ["pg_trgm", "btree_gin", "btree_gist", "pgcrypto"])
    custom_types: List[str] = Field(default_factory=list)
    container_name: str = Field(default="dev-postgres")

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "image": self.image,
            "user": self.user,
            "password": self.password,
            "database": self.database,
            "port": self.port,
            "extensions": self.extensions,
            "custom_types": self.custom_types,
            "container_name": self.container_name,
        }
