from random import randrange
from passlib.context import CryptContext

import click
from faker import Faker
from flask import current_app
from flask.cli import with_appcontext

from quotes_api.extensions import odm as database_ext
from quotes_api.api.models import Quote
from quotes_api.auth.models import User

fake = Faker()


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
    seed_quotes(Quote, 100)


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

    click.secho("Seeding admin user...", bg="magenta", fg="white", bold=True)
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
            click.secho(f"\nAdmin User: {admin}", bg="black", fg="white", bold=True)

    except Exception:
        click.secho(
            "Could not create admin user.", err=True, bg="red", fg="white", bold=True
        )


def seed_quotes(model, quotes_number):
    """
    Seed fake quotes.

    :param config: Flask application config
    :param model: Mongoengine document model
    :return: None
    """
    # Create all the quote models
    quote_instances = []

    for _ in range(0, quotes_number):
        quote = fake.text()
        author = fake.name()
        image = fake.image_url()
        tags = []
        for _ in range(randrange(1, 10)):
            tag = fake.word().lower()
            tags.append(tag)

        quote_data = {
            "quote_text": quote,
            "author_name": author,
            "author_image": image,
            "tags": tags,
        }
        quote = model(**quote_data)
        quote_instances.append(quote)

    click.secho("\nSeeding quotes...", bg="magenta", fg="white", bold=True)
    _bulk_insert(model, quote_instances, "Quote documents")


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
    # Delete the current data
    try:
        click.secho(
            f"Deleting existing {label} documents...",
            bg="blue",
            fg="white",
            bold=True,
        )
        model.objects().delete()
        click.secho("Documents deleted", bg="green", fg="white", bold=True)

    except Exception:
        click.secho(
            f"Could not delete previous documents for {label} collection.",
            bg="red",
            fg="white",
            bold=True,
            err=True,
        )
        return None

    # Bulk insert documents
    try:
        click.secho(
            f"Creating {len(data)} documents for {label} collection...",
            bg="blue",
            fg="white",
            bold=True,
        )
        model.objects.insert(data, load_bulk=False)
        click.secho(f"Created {len(data)} {label}", bg="green", fg="white", bold=True)

    except Exception:
        click.secho(
            f"Could not bulk insert documents for {label} collection.",
            bg="red",
            fg="white",
            bold=True,
            err=True,
        )
        return None
