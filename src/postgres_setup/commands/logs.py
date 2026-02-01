from . import app, run_shell_command, get_instance_name


@app.command()
def logs():
    """Show PostgreSQL logs"""
    instance = get_instance_name()
    print(f"📜 Showing PostgreSQL logs for instance '{instance}' (Ctrl+C to exit)...\n")
    run_shell_command(["docker-compose", "logs", "-f", "postgres"], capture_output=False, use_build_root=True)
