from . import app, get_instance_name, load_config, run_shell_command


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

