import time

from . import app, get_instance_name, load_config, run_shell_command, show_connection_info, show_extensions


@app.command()
def restart():
    """Restart PostgreSQL container"""
    instance = get_instance_name()
    print(f"🔄 Restarting PostgreSQL (Instance: {instance})...")

    # Stop the container
    stop_success, stop_output = run_shell_command(["docker-compose", "down"], use_build_root=True)
    if not stop_success:
        print(f"❌ Failed to stop: {stop_output}")
        return

    print("✓ PostgreSQL stopped")
    time.sleep(2)

    # Start the container
    start_success, start_output = run_shell_command(["docker-compose", "up", "-d"], use_build_root=True)
    if not start_success:
        print(f"❌ Failed to start: {start_output}")
        return

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
