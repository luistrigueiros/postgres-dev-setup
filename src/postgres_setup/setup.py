#!/usr/bin/env python3
"""
PostgreSQL Development Environment Setup
Requires: uv, docker
Usage: uv run python src/postgres_setup/setup.py [command]
"""

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
        compose_content = f"""version: '3.8'

services:
  postgres:
    image: {config['image']}
    container_name: {config['container_name']}
    environment:
      POSTGRES_USER: {config['user']}
      POSTGRES_PASSWORD: {config['password']}
      POSTGRES_DB: {config['database']}
      # Performance tuning for development
      POSTGRES_INITDB_ARGS: "-E UTF8 --locale=en_US.UTF-8"
    ports:
      - "{config['port']}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U {config['user']}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - postgres_network

volumes:
  postgres_data:
    driver: local

networks:
  postgres_network:
    driver: bridge
"""
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
        
        extensions_sql += """
-- Verify extensions
SELECT extname, extversion FROM pg_extension ORDER BY extname;
"""
        
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
    
    def setup(self):
        """Initialize the development environment"""
        print("🚀 Setting up PostgreSQL development environment\n")
        
        config = self.load_config()
        self.save_config(config)
        print(f"✓ Configuration saved to {self.config_file}")
        
        self.generate_docker_compose(config)
        self.generate_init_scripts(config)
        
        print("\n" + "="*60)
        print("✅ Setup complete!")
        print("="*60)
        print("\nNext steps:")
        print("  1. Review config/postgres-config.json to customize")
        print("  2. Run: uv run python src/postgres_setup/setup.py start")
        print("  3. Connect with: uv run python src/postgres_setup/setup.py psql")
    
    def start(self):
        """Start PostgreSQL container"""
        print("🐘 Starting PostgreSQL...")
        
        success, output = self.run_command(["docker-compose", "up", "-d"])
        
        if success:
            print("✓ PostgreSQL container started")
            print("\n⏳ Waiting for PostgreSQL to be healthy...")
            
            config = self.load_config()
            for i in range(30):
                time.sleep(1)
                success, _ = self.run_command([
                    "docker", "exec", config['container_name'],
                    "pg_isready", "-U", config['user']
                ])
                if success:
                    print("✅ PostgreSQL is ready!")
                    self.show_connection_info()
                    self.show_extensions()
                    return
                print(".", end="", flush=True)
            
            print("\n⚠️  PostgreSQL may still be starting. Check with: uv run python src/postgres_setup/setup.py logs")
        else:
            print(f"❌ Failed to start: {output}")
            sys.exit(1)
    
    def stop(self):
        """Stop PostgreSQL container"""
        print("🛑 Stopping PostgreSQL...")
        success, output = self.run_command(["docker-compose", "down"])
        
        if success:
            print("✓ PostgreSQL stopped (data preserved)")
        else:
            print(f"❌ Failed to stop: {output}")
    
    def restart(self):
        """Restart PostgreSQL container"""
        print("🔄 Restarting PostgreSQL...")
        self.stop()
        time.sleep(2)
        self.start()
    
    def destroy(self):
        """Stop and remove all data"""
        confirm = input("⚠️  This will DELETE ALL DATA. Type 'yes' to confirm: ")
        if confirm.lower() != 'yes':
            print("❌ Aborted")
            return
        
        print("💥 Destroying PostgreSQL (including data)...")
        success, output = self.run_command(["docker-compose", "down", "-v"])
        
        if success:
            print("✓ PostgreSQL destroyed (all data removed)")
            print("  Run 'setup' and 'start' again to recreate")
        else:
            print(f"❌ Failed to destroy: {output}")
    
    def logs(self):
        """Show PostgreSQL logs"""
        print("📜 Showing PostgreSQL logs (Ctrl+C to exit)...\n")
        self.run_command(["docker-compose", "logs", "-f", "postgres"], capture_output=False)
    
    def psql(self):
        """Connect to PostgreSQL with psql"""
        config = self.load_config()
        print(f"🔌 Connecting to {config['database']}...\n")
        self.run_command([
            "docker", "exec", "-it", config['container_name'],
            "psql", "-U", config['user'], "-d", config['database']
        ], capture_output=False)
    
    def status(self):
        """Show status of PostgreSQL container"""
        print("📊 PostgreSQL Status\n")
        success, output = self.run_command([
            "docker", "ps", "-a", 
            "--filter", "name=dev-postgres",
            "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        ])
        
        if success:
            print(output)
        else:
            print("❌ Could not check status")
    
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

def main():
    setup = PostgresDevSetup()
    
    commands = {
        "setup": ("Initialize configuration and scripts", setup.setup),
        "start": ("Start PostgreSQL container", setup.start),
        "stop": ("Stop PostgreSQL container", setup.stop),
        "restart": ("Restart PostgreSQL container", setup.restart),
        "destroy": ("Stop and remove all data (⚠️  destructive)", setup.destroy),
        "logs": ("Show PostgreSQL logs", setup.logs),
        "psql": ("Connect with psql client", setup.psql),
        "status": ("Show container status", setup.status),
        "info": ("Show connection information", setup.show_connection_info),
    }
    
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print("PostgreSQL Development Environment Manager")
        print("\nUsage: uv run python src/postgres_setup/setup.py [command]")
        print("\nAvailable commands:")
        for cmd, (description, _) in commands.items():
            print(f"  {cmd:12} - {description}")
        sys.exit(1)
    
    command = sys.argv[1]
    commands[command][1]()

if __name__ == "__main__":
    main()
