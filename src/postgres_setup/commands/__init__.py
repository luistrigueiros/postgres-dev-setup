import json
import subprocess
import time
from functools import lru_cache
from pathlib import Path
from typing import Tuple

import typer

from ..domain import PostgresConfig

app = typer.Typer(
    help="PostgreSQL Development Environment Manager",
    no_args_is_help=True,
    rich_markup_mode="rich",
)

# project_root is the root of the repository
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DEFAULT_INSTANCE = "default"

# Global state for the selected instance
state = {"pg_instance": DEFAULT_INSTANCE}

@app.callback()
def main(
    pg_instance: str = typer.Option(
        None,
        "--pg-instance",
        "-pgi",
        envvar="PG_INSTANCE",
        help="Select the PostgreSQL instance to operate on",
    )
):
    if pg_instance:
        state["pg_instance"] = pg_instance

def get_instance_name() -> str:
    return state["pg_instance"]

def get_build_root() -> Path:
    """Return the build root for the current instance"""
    instance = get_instance_name()
    if instance == DEFAULT_INSTANCE:
        return PROJECT_ROOT / "build" / "DEFAULT"
    return PROJECT_ROOT / "build" / instance

def get_config_file_path() -> Path:
    """Return the configuration file path for the current instance"""
    return get_build_root() / "config" / "postgres-config.json"

def get_default_config() -> PostgresConfig:
    """Default PostgreSQL configuration"""
    instance = get_instance_name()
    container_name = "dev-postgres" if instance == DEFAULT_INSTANCE else f"dev-postgres-{instance}"
    return PostgresConfig(container_name=container_name)

@lru_cache(maxsize=None)
def get_config() -> PostgresConfig:
    """Shared immutable instance of the configuration"""
    return load_config()

def load_config() -> PostgresConfig:
    """Load PostgreSQL configuration from JSON file"""
    config_file = get_config_file_path()
    if not config_file.exists():
        return get_default_config()

    try:
        with open(config_file) as f:
            data = json.load(f)
            return PostgresConfig(**data)
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        # Fallback to default if config is invalid, but maybe should raise in production
        print(f"⚠️ Warning: Failed to load config from {config_file}: {e}. Using defaults.")
        return get_default_config()

def run_shell_command(
    cmd: list[str], capture_output: bool = True, use_build_root: bool = False
) -> Tuple[bool, str]:
    """Execute shell command and return success status and output"""
    build_root = get_build_root()
    cwd = build_root if use_build_root else PROJECT_ROOT

    # Ensure directory exists if we're using it as CWD
    if use_build_root:
        cwd.mkdir(parents=True, exist_ok=True)

    try:
        if capture_output:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd,
            )
            return True, result.stdout

        subprocess.run(cmd, check=True, cwd=cwd)
        return True, ""
    except subprocess.CalledProcessError as e:
        return False, e.stderr if capture_output else str(e)

def show_connection_info():
    """Display connection information"""
    pg_config = get_config()
    instance = get_instance_name()
    print("\n" + "=" * 60)
    print(f"📋 Connection Information (Instance: {instance})")
    print("=" * 60)
    print("  Host:     localhost")
    print(f"  Port:     {pg_config.port}")
    print(f"  Database: {pg_config.database}")
    print(f"  User:     {pg_config.user}")
    print(f"  Password: {pg_config.password}")
    print("\n  Connection URI:")
    print(
        f"  postgresql://{pg_config.user}:{pg_config.password}@localhost:{pg_config.port}/{pg_config.database}"
    )
    print("=" * 60)

def show_extensions():
    """Show installed extensions"""
    pg_config = get_config()
    success, output = run_shell_command(
        [
            "docker",
            "exec",
            pg_config.container_name,
            "psql",
            "-U",
            pg_config.user,
            "-d",
            pg_config.database,
            "-c",
            "SELECT extname, extversion FROM pg_extension ORDER BY extname;",
        ]
    )

    if success:
        print("\n📦 Installed Extensions:")
        print(output)

def handle_successful_start():
    """Handle successful container start by waiting for PostgreSQL to be ready"""
    print("✓ PostgreSQL container started")
    print("\n⏳ Waiting for PostgreSQL to be healthy...")

    pg_config = get_config()
    for i in range(30):
        time.sleep(1)
        success, _ = run_shell_command([
            "docker", "exec", pg_config.container_name,
            "pg_isready", "-U", pg_config.user
        ])
        if success:
            print("✅ PostgreSQL is ready!")
            show_connection_info()
            show_extensions()
            return
        print(".", end="", flush=True)

    print("\n⚠️  PostgreSQL may still be starting. Check with: pgctl logs")

from . import config as config  # noqa: E402
from . import destroy as destroy  # noqa: E402
from . import info as info  # noqa: E402
from . import logs as logs  # noqa: E402
from . import psql as psql  # noqa: E402
from . import restart as restart  # noqa: E402
from . import setup as setup  # noqa: E402
from . import start as start  # noqa: E402
from . import status as status  # noqa: E402
from . import stop as stop  # noqa: E402
