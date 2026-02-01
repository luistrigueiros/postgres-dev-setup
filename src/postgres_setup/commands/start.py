
import sys
import time
from argparse import Namespace
from . import Command


class StartCommand(Command):
    def __init__(self):
        super().__init__("start", "Start PostgreSQL container")

    def run(self, args: Namespace):
        """Start PostgreSQL container"""
        print("🐘 Starting PostgreSQL...")

        success, output = self.run_command(["docker-compose", "up", "-d"], use_build_root=True)

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

