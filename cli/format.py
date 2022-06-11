import click
import subprocess


@click.command()
@click.argument("path", default=".")
def format(path):
    """
    Run black code formatter on the codebase.

    :param path: Execution path
    :return: Subprocess call result
    """
    command = f"black {path}"
    return subprocess.call(command, shell=True)


if __name__ == "__main__":
    format()
