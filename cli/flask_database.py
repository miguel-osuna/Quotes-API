from passlib.context import CryptContext

import click
from flask import current_app
from flask.cli import with_appcontext

from quotes_api.extensions import odm as database_ext
from quotes_api.api.models import Quote
from quotes_api.auth.models import User, TokenBlacklist


@click.group()
def database():
    """Run database related tasks."""


@database.command()
@with_appcontext
def init():
    """
    Initialize the database

    :return: None
    """
    app_config = current_app.config

    # Check if databases exist.

    # Drop existing databases if they exist. Create them if they don't.

    # Create the database collections for Quote, User and TokenBlacklist


@database.command()
@with_appcontext
def seed():
    """
    Seed the database with initial values.
    :return: None
    """
    app_config = current_app.config
    pwd_hasher = CryptContext(schemes=["sha256_crypt"])

    seed_admin(app_config, User, pwd_hasher)


def seed_admin(config, model, pwd_hasher):
    """
    Seed initial admin user.

    :param config: Flask application config
    :param model: Mongoengine document model
    :param pwd_hasher: Crytographic hasher
    :return: None
    """

    admin = None
    admin_username = config["SEED_ADMIN_USERNAME"]
    admin_email = config["SEED_ADMIN_EMAIL"]
    admin_password = pwd_hasher.hash(config["SEED_ADMIN_PASSWORD"])

    try:
        admin = model.objects.get(username=admin_username)

        if admin:
            click.secho("Admin user already exists", bg="green", fg="white", bold=True)
            click.secho(f"\nAdmin User:\n {admin}", bg="black", fg="white", bold=True)

            return None

    except Exception:
        click.secho("Admin user does not exist.", bg="blue", fg="white", bold=True)

    try:
        if admin is None:
            admin_user_data = {
                "username": admin_username,
                "email": admin_email,
                "password": admin_password,
                "active": True,
                "roles": ["admin"],
            }
            click.secho("Creating admin user...", bg="blue", fg="white", bold=True)

            admin = model(**admin_user_data)
            admin.save()

            click.secho("Admin user created.", bg="green", fg="white", bold=True)
            click.secho(f"\nAdmin User:\n {admin}", bg="black", fg="white", bold=True)

    except Exception:
        click.secho(
            "Could not create admin user.", err=True, bg="red", fg="white", bold=True
        )


def seed_quotes(config, model):
    """
    Seed fake quotes.

    :param config: Flask application config
    :param model: Mongoengine document model
    :return: None
    """
    pass


def _bulk_insert(model, data, label):
    """
    Bulk insert data to a specific model and log it. This is more
    efficient than adding 1 row at a time in a loop.

    :param model: Model being affected
    :type model: Mongoengine Document
    :param data: Document fields to be saved
    :type data: list
    :param label: Label for the output
    :type label: str
    :return: None
    """
    pass


def _seed_logs(count, model_label):
    """
    Log the output of how many collection documents were created.

    :param count: Amount of documents
    :type count: int
    :param model_label: Name of the model
    :type model_label: str
    :return None:
    """
    click.secho(f"Created {count} {model_label}", bg="green", fg="white", bold=True)
