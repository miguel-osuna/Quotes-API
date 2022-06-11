import importlib
import os


def register_cli_commands(app):
    """
    Register 0 or more Flask CLI commands (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    for file in os.listdir(os.path.dirname(__file__)):
        if file.startswith("flask_") and file.endswith(".py"):
            # Get the file name
            filename = file[:-3]
            command_name = file[4:-3]

            # Import the cli command module
            module = importlib.import_module(f"cli.{filename}")

            command = getattr(module, command_name)

            # Register the cli command under the Flask app
            app.cli.add_command(command)

    return None
