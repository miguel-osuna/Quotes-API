"""Linter (Pylint) CLI Command"""
import subprocess

import click


@click.command()
@click.argument("path", default="quots_api")
def lint(path):
    """
    Run pylint linter to analyze the codebase.

    :param path: Execution path
    :return: Subprocess call result
    """
    command = f"pylint {path}"
    return subprocess.call(command, shell=True)


if __name__ == "__main__":
    lint()
