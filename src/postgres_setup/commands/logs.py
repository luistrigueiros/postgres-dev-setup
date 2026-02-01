from . import app, run_shell_command


@app.command()
def logs():
    """Show PostgreSQL logs"""
    print("📜 Showing PostgreSQL logs (Ctrl+C to exit)...\n")
    run_shell_command(["docker-compose", "logs", "-f", "postgres"], capture_output=False, use_build_root=True)
