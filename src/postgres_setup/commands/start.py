import sys
import time

from . import app, get_instance_name, load_config, run_shell_command, show_connection_info, show_extensions


@app.command()
def start():
    """Start PostgreSQL container"""
    instance = get_instance_name()
    print(f"🐘 Starting PostgreSQL (Instance: {instance})...")

    success, output = run_shell_command(["docker-compose", "up", "-d"], use_build_root=True)

    if success:
        print("✓ PostgreSQL container started")
        print("\n⏳ Waiting for PostgreSQL to be healthy...")

        config = load_config()
        for i in range(30):
            time.sleep(1)
            success, _ = run_shell_command([
                "docker", "exec", config['container_name'],
                "pg_isready", "-U", config['user']
            ])
            if success:
                print("✅ PostgreSQL is ready!")
                show_connection_info()
                show_extensions()
                return
            print(".", end="", flush=True)

        print("\n⚠️  PostgreSQL may still be starting. Check with: pgctl logs")
    else:
        print(f"❌ Failed to start: {output}")
        sys.exit(1)

