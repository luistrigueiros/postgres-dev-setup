import json

from . import app, get_config, get_default_config


@app.command(name="config-gen")
def config_gen():
    """Dump sample configuration to console to be used for a new instance"""
    config = get_default_config()
    print(json.dumps(config.to_dict(), indent=4))

@app.command(name="config-display")
def config_display():
    """Display current configuration in the console for the selected instance"""
    config = get_config()
    print(json.dumps(config.to_dict(), indent=4))
