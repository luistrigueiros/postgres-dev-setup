import pytest
from pydantic import ValidationError

from postgres_setup.domain import PostgresConfig


def test_postgres_config_defaults():
    config = PostgresConfig()
    assert config.port == 5432
    assert config.user == "devuser"
    assert "pg_trgm" in config.extensions

def test_postgres_config_validation():
    # Valid port
    config = PostgresConfig(port=1234)
    assert config.port == 1234

    # Invalid port (low)
    with pytest.raises(ValidationError):
        PostgresConfig(port=0)

    # Invalid port (high)
    with pytest.raises(ValidationError):
        PostgresConfig(port=70000)

def test_postgres_config_immutability():
    config = PostgresConfig()
    with pytest.raises(AttributeError):
        config.port = 5433

def test_postgres_config_extra_ignored():
    config = PostgresConfig(extra_field="ignored")
    assert not hasattr(config, "extra_field")

def test_postgres_config_to_dict():
    config = PostgresConfig(port=1234)
    d = config.to_dict()
    assert d["port"] == 1234
    assert "image" in d
