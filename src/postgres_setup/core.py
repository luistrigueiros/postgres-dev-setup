
import subprocess

from postgres_setup.commands import Command


class PostgresDevSetup(Command):
    def __init__(self):
        super().__init__(name="__postgres_dev_setup__", description="Internal helper")

    def run_command(self, cmd: list[str], capture_output: bool = True) -> tuple[bool, str]:
        """Execute shell command and return success status and output"""
        try:
            if capture_output:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True,
                    cwd=self.project_root,
                )
                return True, result.stdout

            subprocess.run(cmd, check=True, cwd=self.project_root)
            return True, ""
        except subprocess.CalledProcessError as e:
            return False, e.stderr if capture_output else str(e)

    def show_connection_info(self):
        """Display connection information"""
        config = self.load_config()
        print("\n" + "=" * 60)
        print("📋 Connection Information")
        print("=" * 60)
        print("  Host:     localhost")
        print(f"  Port:     {config['port']}")
        print(f"  Database: {config['database']}")
        print(f"  User:     {config['user']}")
        print(f"  Password: {config['password']}")
        print("\n  Connection URI:")
        print(
            f"  postgresql://{config['user']}:{config['password']}@localhost:{config['port']}/{config['database']}"
        )
        print("=" * 60)

    def show_extensions(self):
        """Show installed extensions"""
        config = self.load_config()
        success, output = self.run_command(
            [
                "docker",
                "exec",
                config["container_name"],
                "psql",
                "-U",
                config["user"],
                "-d",
                config["database"],
                "-c",
                "SELECT extname, extversion FROM pg_extension ORDER BY extname;",
            ]
        )

        if success:
            print("\n📦 Installed Extensions:")
            print(output)
