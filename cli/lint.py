import click
import subprocess


@click.command()
@click.argument("path", default=".")
def lint(path):
    """Run pylint linter to analyze the codebase.

    :param path: Execution path
    :return: Subprocess call result
    """
    command = f"pylint {path}"
    return subprocess.cal(command, shell=True)
