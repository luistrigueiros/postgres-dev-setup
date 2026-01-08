from argparse import Namespace
from postgres_setup.commands import Command
from postgres_setup.core import PostgresDevSetup


class SetupCommand(Command):
    def __init__(self):
        super().__init__("setup", "Initialize configuration and scripts")

    def run(self, args: Namespace):
        """Initialize the development environment"""
        setup = PostgresDevSetup()
        print("🚀 Setting up PostgreSQL development environment\n")

        config = setup.load_config()
        setup.save_config(config)
        print(f"✓ Configuration saved to {setup.config_file}")

        setup.generate_docker_compose(config)
        setup.generate_init_scripts(config)

        print("\n" + "=" * 60)
        print("✅ Setup complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Review config/postgres-config.json to customize")
        print("  2. Run: uv run python src/postgres_setup/setup.py start")
        print("  3. Connect with: uv run python src/postgres_setup/setup.py psql")

