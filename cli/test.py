"""Test (Pytest) CLI Command"""
import subprocess

import click


@click.command()
def test():
    """
    Run tests with Pytest (pytest-sugar).

    :param path: Test path
    :return: Subprocess call result
    """
    command = "py.test --capture=no"
    return subprocess.call(command, shell=True)
