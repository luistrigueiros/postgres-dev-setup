
import time
from argparse import Namespace
from . import Command


class RestartCommand(Command):
    def __init__(self):
        super().__init__("restart", "Restart PostgreSQL container")

    def run(self, args: Namespace):
        """Restart PostgreSQL container"""
        print("🔄 Restarting PostgreSQL...")
        
        # Stop the container
        stop_success, stop_output = self.run_command(["docker-compose", "down"], use_build_root=True)
        if not stop_success:
            print(f"❌ Failed to stop: {stop_output}")
            return
        
        print("✓ PostgreSQL stopped")
        time.sleep(2)

        # Start the container
        start_success, start_output = self.run_command(["docker-compose", "up", "-d"], use_build_root=True)
        if not start_success:
            print(f"❌ Failed to start: {start_output}")
            return
            
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
