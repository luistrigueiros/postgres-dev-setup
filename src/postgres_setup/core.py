
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional
import json

class PostgresDevSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.compose_file = self.project_root / "docker-compose.yml"
        self.init_scripts_dir = self.project_root / "init-scripts"
        self.config_file = self.project_root / "config" / "postgres-config.json"
        
    def load_config(self) -> dict:
        """Load PostgreSQL configuration from JSON file"""
        if not self.config_file.exists():
            return self.default_config()
        
        with open(self.config_file) as f:
            return json.load(f)
    
    def default_config(self) -> dict:
        """Default PostgreSQL configuration"""
        return {
            "image": "postgres:16",
            "user": "devuser",
            "password": "devpass",
            "database": "devdb",
            "port": 5432,
            "extensions": [
                "pg_trgm",      # Text search
                "btree_gin",    # Additional index types
                "btree_gist",   # Additional index types
                "pgcrypto"      # Cryptographic functions
            ],
            "custom_types": [],
            "container_name": "dev-postgres"
        }
    
    def save_config(self, config: dict):
        """Save configuration to JSON file"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(config, indent=2, fp=f)
    
    def generate_docker_compose(self, config: dict):
        """Generate docker-compose.yml from config"""
        compose_content = f"""version: '3.8'\n\nservices:\n  postgres:\n    image: {config['image']}\n    container_name: {config['container_name']}\n    environment:\n      POSTGRES_USER: {config['user']}\n      POSTGRES_PASSWORD: {config['password']}\n      POSTGRES_DB: {config['database']}\n      # Performance tuning for development\n      POSTGRES_INITDB_ARGS: \"-E UTF8 --locale=en_US.UTF-8\"\n    ports:\n      - \"{config['port']}:5432\"\n    volumes:\n      - postgres_data:/var/lib/postgresql/data\n      - ./init-scripts:/docker-entrypoint-initdb.d:ro\n    healthcheck:\n      test: [\"CMD-SHELL\", \"pg_isready -U {config['user']}\"]\n      interval: 10s\n      timeout: 5s\n      retries: 5\n    networks:\n      - postgres_network\n\nvolumes:\n  postgres_data:\n    driver: local\n\nnetworks:\n  postgres_network:\n    driver: bridge\n"""
        self.compose_file.write_text(compose_content)
        print(f"✓ Generated {self.compose_file.name}")
    
    def generate_init_scripts(self, config: dict):
        """Generate initialization SQL scripts"""
        self.init_scripts_dir.mkdir(exist_ok=True)
        
        # Extensions script
        extensions_sql = """-- Install PostgreSQL extensions
-- This script runs automatically when the database is first created

"""
        for ext in config['extensions']:
            extensions_sql += f"CREATE EXTENSION IF NOT EXISTS {ext};\n"
        
        extensions_sql += "\n-- Verify extensions\nSELECT extname, extversion FROM pg_extension ORDER BY extname;\n"
        
        (self.init_scripts_dir / "01-extensions.sql").write_text(extensions_sql)
        print(f"✓ Generated extension scripts for: {', '.join(config['extensions'])}")
        
        # Custom types script
        if config['custom_types']:
            types_sql = """-- Custom data types
-- Define your custom PostgreSQL types here

"""
            for custom_type in config['custom_types']:
                types_sql += f"{custom_type}\n\n"
            
            (self.init_scripts_dir / "02-custom-types.sql").write_text(types_sql)
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
        (self.init_scripts_dir / "03-sample-data.sql").write_text(sample_sql)
        print("✓ Generated sample data template")
    
    def run_command(self, cmd: list[str], capture_output: bool = True) -> tuple[bool, str]:
        """Execute shell command and return success status and output"""
        try:
            if capture_output:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True,
                    cwd=self.project_root
                )
                return True, result.stdout
            else:
                subprocess.run(cmd, check=True, cwd=self.project_root)
                return True, ""
        except subprocess.CalledProcessError as e:
            return False, e.stderr if capture_output else str(e)
    
    def show_connection_info(self):
        """Display connection information"""
        config = self.load_config()
        print("\n" + "="*60)
        print("📋 Connection Information")
        print("="*60)
        print(f"  Host:     localhost")
        print(f"  Port:     {config['port']}")
        print(f"  Database: {config['database']}")
        print(f"  User:     {config['user']}")
        print(f"  Password: {config['password']}")
        print(f"\n  Connection URI:")
        print(f"  postgresql://{config['user']}:{config['password']}@localhost:{config['port']}/{config['database']}")
        print("="*60)
    
    def show_extensions(self):
        """Show installed extensions"""
        config = self.load_config()
        success, output = self.run_command([
            "docker", "exec", config['container_name'],
            "psql", "-U", config['user'], "-d", config['database'],
            "-c", "SELECT extname, extversion FROM pg_extension ORDER BY extname;"
        ])
        
        if success:
            print("\n📦 Installed Extensions:")
            print(output)
