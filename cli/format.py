import click
import subprocess


@click.group()
def format():
    """Run black code formatter on the project."""


@format.command()
@click.argument("path", default=".")
def check(path):
    """
    Checks the project files that can be formatted.

    :param path: Files path
    :return: Subprocess call result
    """
    cmd = f"black --check {path}"
    return subprocess.call(cmd, shell=True)


@format.command()
@click.argument("path", default=".")
def write(path):
    """
    Formats project files.

    :param path: Files path
    :return: Subprocess call result
    """
    cmd = f"black {path}"
    return subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    format()
