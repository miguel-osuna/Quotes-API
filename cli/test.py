"""Test (Pytest) CLI Command"""
import subprocess

import click


@click.command()
@click.argument("path", default="tests")
def test(path):
    """
    Run tests with Pytest (pytest-sugar).

    :param path: Test path
    :return: Subprocess call result
    """
    command = f"py.test -s {path}"
    return subprocess.call(command, shell=True)
