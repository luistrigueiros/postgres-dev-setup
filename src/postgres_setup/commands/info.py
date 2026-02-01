from . import app, show_connection_info


@app.command()
def info():
    """Show connection information"""
    show_connection_info()
