import sys

from . import app, get_instance_name, handle_successful_start, run_shell_command


@app.command()
def start():
    """Start PostgreSQL container"""
    instance = get_instance_name()
    print(f"🐘 Starting PostgreSQL (Instance: {instance})...")

    success, output = run_shell_command(["docker-compose", "up", "-d"], use_build_root=True)

    if success:
        handle_successful_start()
    else:
        print(f"❌ Failed to start: {output}")
        sys.exit(1)

