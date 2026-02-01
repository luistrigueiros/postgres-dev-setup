from . import app, get_instance_name, run_shell_command


@app.command()
def stop():
    """Stop PostgreSQL container"""
    instance = get_instance_name()
    print(f"🛑 Stopping PostgreSQL (Instance: {instance})...")
    success, output = run_shell_command(["docker-compose", "down"], use_build_root=True)

    if success:
        print("✓ PostgreSQL stopped (data preserved)")
    else:
        print(f"❌ Failed to stop: {output}")
