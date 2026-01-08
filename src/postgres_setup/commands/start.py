
import sys
import time
from argparse import Namespace
from postgres_setup.commands import Command
from postgres_setup.core import PostgresDevSetup


class StartCommand(Command):
    def __init__(self):
        super().__init__("start", "Start PostgreSQL container")

    def run(self, args: Namespace):
        """Start PostgreSQL container"""
        setup = PostgresDevSetup()
        print("🐘 Starting PostgreSQL...")

        success, output = setup.run_command(["docker-compose", "up", "-d"])

        if success:
            print("✓ PostgreSQL container started")
            print("\n⏳ Waiting for PostgreSQL to be healthy...")

            config = setup.load_config()
            for i in range(30):
                time.sleep(1)
                success, _ = setup.run_command([
                    "docker", "exec", config['container_name'],
                    "pg_isready", "-U", config['user']
                ])
                if success:
                    print("✅ PostgreSQL is ready!")
                    setup.show_connection_info()
                    setup.show_extensions()
                    return
                print(".", end="", flush=True)

            print("\n⚠️  PostgreSQL may still be starting. Check with: uv run python src/postgres_setup/setup.py logs")
        else:
            print(f"❌ Failed to start: {output}")
            sys.exit(1)

