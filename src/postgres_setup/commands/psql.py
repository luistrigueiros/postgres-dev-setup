from . import app, load_config, run_shell_command, get_instance_name


@app.command()
def psql():
    """Connect with psql client"""
    config = load_config()
    instance = get_instance_name()
    print(f"🔌 Connecting to {config['database']} (Instance: {instance})...\n")
    run_shell_command([
        "docker", "exec", "-it", config['container_name'],
        "psql", "-U", config['user'], "-d", config['database']
    ], capture_output=False)

