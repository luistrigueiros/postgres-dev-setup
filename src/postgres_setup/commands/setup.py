"""Setup command - Initialize the development environment."""

from .base import BaseCommand


class SetupCommand(BaseCommand):
    """Initialize PostgreSQL development environment."""

    name = "setup"
    description = "Initialize configuration and scripts"

    def execute(self) -> None:
        """Initialize the development environment."""
        print("🚀 Setting up PostgreSQL development environment\n")

        # Load or create config
        config = self.config_manager.load()
        self.config_manager.save(config)
        self.print_success(f"Configuration saved to {self.config_manager.config_file}")

        # Generate docker-compose.yml
        self.docker.generate_compose_file(
            self.config_manager.compose_file,
            config
        )
        self.print_success(f"Generated {self.config_manager.compose_file.name}")

        # Generate init scripts
        self.docker.generate_init_scripts(
            self.config_manager.init_scripts_dir,
            config
        )
        self.print_success(f"Generated extension scripts for: {', '.join(config['extensions'])}")

        if config['custom_types']:
            self.print_success(f"Generated {len(config['custom_types'])} custom type(s)")

        self.print_success("Generated sample data template")

        print("\n" + "=" * 60)
        print("✅ Setup complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Review config/postgres-config.json to customize")
        print("  2. Run: ./pgctl start")
        print("  3. Connect with: ./pgctl psql")