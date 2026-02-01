import time

from . import app, get_instance_name, handle_successful_start, run_shell_command


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

    handle_successful_start()
