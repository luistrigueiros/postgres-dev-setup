from . import app, run_shell_command


@app.command()
def destroy():
    """Stop and remove all data (⚠️ destructive)"""
    confirm = input("⚠️  This will DELETE ALL DATA. Type 'yes' to confirm: ")
    if confirm.lower() != 'yes':
        print("❌ Aborted")
        return

    print("💥 Destroying PostgreSQL (including data)...")
    success, output = run_shell_command(["docker-compose", "down", "-v"], use_build_root=True)

    if success:
        print("✓ PostgreSQL destroyed (all data removed)")
        print("  Run 'pgctl setup' and 'pgctl start' again to recreate")
    else:
        print(f"❌ Failed to destroy: {output}")
