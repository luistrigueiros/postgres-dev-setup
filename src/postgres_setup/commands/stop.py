from . import app, run_shell_command


@app.command()
def stop():
    """Stop PostgreSQL container"""
    print("🛑 Stopping PostgreSQL...")
    success, output = run_shell_command(["docker-compose", "down"], use_build_root=True)

    if success:
        print("✓ PostgreSQL stopped (data preserved)")
    else:
        print(f"❌ Failed to stop: {output}")
