from argparse import Namespace

from . import Command


class PsqlCommand(Command):
    def __init__(self):
        super().__init__("psql", "Connect with psql client")

    def run(self, args: Namespace):
        """Connect to PostgreSQL with psql"""
        config = self.load_config()
        print(f"🔌 Connecting to {config['database']}...\n")
        self.run_command([
            "docker", "exec", "-it", config['container_name'],
            "psql", "-U", config['user'], "-d", config['database']
        ], capture_output=False)

