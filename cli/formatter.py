"""Formating CLI Command"""
import subprocess

import click


@click.command()
@click.argument("path", default=".")
def formatter(path):
    """
    Run black code formatter on the codebase.

    :param path: Execution path
    :return: Subprocess call result
    """
    command = f"black {path}"
    return subprocess.call(command, shell=True)


if __name__ == "__main__":
    formatter()
