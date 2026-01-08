from argparse import Namespace
from postgres_setup.commands import Command
from postgres_setup.core import PostgresDevSetup


class PsqlCommand(Command):
    def __init__(self):
        super().__init__("psql", "Connect with psql client")

    def run(self, args: Namespace):
        """Connect to PostgreSQL with psql"""
        setup = PostgresDevSetup()
        config = setup.load_config()
        print(f"🔌 Connecting to {config['database']}...\n")
        setup.run_command([
            "docker", "exec", "-it", config['container_name'],
            "psql", "-U", config['user'], "-d", config['database']
        ], capture_output=False)

