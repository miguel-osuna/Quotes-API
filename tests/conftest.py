""" Defines fixtures available to all tests. """

import pytest
from datetime import datetime

from quotes_api.app import create_app
from quotes_api.extensions import odm as _db
from quotes_api.models import Quote, User, TokenBlacklist


@pytest.fixture
def app():
    """ Create application for testing. """
    app = create_app("testing")
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def db(app):
    """ Create database for testing. """
    pass


@pytest.fixture
def user():
    """ Create basic user for testing. """
    # User mock data
    user_data = {
        "username": "user",
        "email": "user@email.com",
        "password": "user",
    }

    user = User(**user_data)
    user.save()

    return user


@pytest.fixture
def admin_user():
    """ Create admin user for testing. """
    # Admin user mock data
    admin_user_data = {
        "username": "admin",
        "email": "admin@email.com",
        "password": "admin",
    }

    user = User(**admin_user_data)
    user.save()

    return user


@pytest.fixture
def quote():
    """ Create quote for testing. """

    # Quote mock data
    quote_data = {
        "quote_text": "Quote.",
        "author_name": "Author",
        "author_image": "URL",
        "tags": ["test-tag"],
    }

    quote = Quote(**quote_data)
    quote.save()

    return quote


@pytest.fixture
def access_token(user):
    """ Create access token for testing. """
    access_token_data = {
        "jti": "jti_example",
        "token_type": "access",
        "user": user,
        "revoked": False,
        "expires": datetime.fromtimestamp(1608057500),
    }

    token = TokenBlacklist(**access_token_data)
    token.save()

    return token


@pytest.fixture
def refresh_token(user):
    """ Create refresh token for testing. """
    refresh_token_data = {
        "jti": "jti_example",
        "token_type": "refresh",
        "user": user,
        "revoked": False,
        "expires": datetime.fromtimestamp(1608057500),
    }

    token = TokenBlacklist(**refresh_token_data)
    token.save()

    return token
