import json
from pathlib import Path

from . import PROJECT_ROOT, app, get_build_root, get_config_file, load_config


def _save_config(config_file: Path, config: dict) -> None:
    """Save configuration to JSON file"""
    config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(config_file, "w") as f:
        json.dump(config, indent=2, fp=f)

def _generate_docker_compose(build_root: Path, config: dict) -> None:
    """Generate docker-compose.yml from config"""
    compose_file = build_root / "docker-compose.yml"
    compose_content = (
        f"version: '3.8'\n\n"
        f"services:\n"
        f"  postgres:\n"
        f"    image: {config['image']}\n"
        f"    container_name: {config['container_name']}\n"
        f"    environment:\n"
        f"      POSTGRES_USER: {config['user']}\n"
        f"      POSTGRES_PASSWORD: {config['password']}\n"
        f"      POSTGRES_DB: {config['database']}\n"
        f"      # Performance tuning for development\n"
        f"      POSTGRES_INITDB_ARGS: '-E UTF8 --locale=en_US.UTF-8'\n"
        f"    ports:\n"
        f"      - '{config['port']}:5432'\n"
        f"    volumes:\n"
        f"      - postgres_data:/var/lib/postgresql/data\n"
        f"      - ./init-scripts:/docker-entrypoint-initdb.d:ro\n"
        f"    healthcheck:\n"
        f"      test: ['CMD-SHELL', 'pg_isready -U {config['user']}']\n"
        f"      interval: 10s\n"
        f"      timeout: 5s\n"
        f"      retries: 5\n"
        f"    networks:\n"
        f"      - postgres_network\n\n"
        f"volumes:\n"
        f"  postgres_data:\n"
        f"    driver: local\n\n"
        f"networks:\n"
        f"  postgres_network:\n"
        f"    driver: bridge\n"
    )
    compose_file.write_text(compose_content)
    print(f"✓ Generated {compose_file.name}")

def _generate_init_scripts(build_root: Path, config: dict) -> None:
    """Generate initialization SQL scripts"""
    init_scripts_dir = build_root / "init-scripts"
    init_scripts_dir.mkdir(parents=True, exist_ok=True)

    # Extensions script
    extensions_sql = """-- Install PostgreSQL extensions
-- This script runs automatically when the database is first created

"""
    for ext in config["extensions"]:
        extensions_sql += f"CREATE EXTENSION IF NOT EXISTS {ext};\n"

    extensions_sql += "\n-- Verify extensions\nSELECT extname, extversion FROM pg_extension ORDER BY extname;\n"
    (init_scripts_dir / "01-extensions.sql").write_text(extensions_sql)
    print(f"✓ Generated extension scripts for: {', '.join(config['extensions'])}")

    # Custom types script
    if config["custom_types"]:
        types_sql = """-- Custom data types
-- Define your custom PostgreSQL types here

"""
        for custom_type in config["custom_types"]:
            types_sql += f"{custom_type}\n\n"

        (init_scripts_dir / "02-custom-types.sql").write_text(types_sql)
        print(f"✓ Generated {len(config['custom_types'])} custom type(s)")

    # Sample data script (optional)
    sample_sql = """-- Sample initialization script
-- You can add your own tables and seed data here

-- Example: Create a sample table
-- CREATE TABLE IF NOT EXISTS users (
--     id SERIAL PRIMARY KEY,
--     email TEXT NOT NULL UNIQUE,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );
"""
    (init_scripts_dir / "03-sample-data.sql").write_text(sample_sql)
    print("✓ Generated sample data template")

@app.command()
def setup():
    """Initialize configuration and scripts"""
    print("🚀 Setting up PostgreSQL development environment\n")

    config = load_config()
    config_file = get_config_file()
    build_root = get_build_root()

    _save_config(config_file, config)
    print(f"✓ Configuration saved to {config_file}")

    _generate_docker_compose(build_root, config)
    _generate_init_scripts(build_root, config)

    print("\n" + "=" * 60)
    print("✅ Setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    root = PROJECT_ROOT if "PROJECT_ROOT" in globals() else Path.cwd()
    print(f"  1. Review {config_file.relative_to(root)} to customize")
    print("  2. Run: pgctl start")
    print("  3. Connect with: pgctl psql")
