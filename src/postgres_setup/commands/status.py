from . import app, get_instance_name, load_config, run_shell_command


@app.command()
def status():
    """Show status of PostgreSQL container"""
    config = load_config()
    instance = get_instance_name()
    print(f"📊 PostgreSQL Status (Instance: {instance}, Container: {config['container_name']})\n")
    success, output = run_shell_command([
        "docker", "ps", "-a",
        "--filter", f"name={config['container_name']}",
        "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    ])

    if success:
        print(output)
    else:
        print("❌ Could not check status")
