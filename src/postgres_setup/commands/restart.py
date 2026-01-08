
import time
from argparse import Namespace
from postgres_setup.commands import Command
from postgres_setup.core import PostgresDevSetup


class RestartCommand(Command):
    def __init__(self):
        super().__init__("restart", "Restart PostgreSQL container")

    def run(self, args: Namespace):
        """Restart PostgreSQL container"""
        setup = PostgresDevSetup()
        print("🔄 Restarting PostgreSQL...")
        
        # Stop the container
        stop_success, stop_output = setup.run_command(["docker-compose", "down"])
        if not stop_success:
            print(f"❌ Failed to stop: {stop_output}")
            return
        
        print("✓ PostgreSQL stopped")
        time.sleep(2)

        # Start the container
        start_success, start_output = setup.run_command(["docker-compose", "up", "-d"])
        if not start_success:
            print(f"❌ Failed to start: {start_output}")
            return
            
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
