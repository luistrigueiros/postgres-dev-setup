from . import app, run_shell_command


@app.command()
def status():
    """Show status of PostgreSQL container"""
    print("📊 PostgreSQL Status\n")
    success, output = run_shell_command([
        "docker", "ps", "-a",
        "--filter", "name=dev-postgres",
        "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    ])

    if success:
        print(output)
    else:
        print("❌ Could not check status")
