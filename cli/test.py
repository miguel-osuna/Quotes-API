"""Test (Pytest) CLI Command"""
import subprocess

import click


@click.command()
@click.argument("path", default="tests")
def test(path):
    """
    Run tests with Pytest.

    :param path: Test path
    :return: Subprocess call result
    """
    command = f"pytest -s {path}"
    return subprocess.call(command, shell=True)
