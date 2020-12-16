""" Defines fixtures available to all tests. """

import pytest
import mongoengine
from datetime import datetime
from flask_mongoengine import MongoEngine

from quotes_api.app import create_app
from quotes_api.models import QuoteFields, UserFields, TokenBlacklistFields


@pytest.fixture(scope="session")
def app():
    """ Create application for testing. """
    app = create_app("testing")

    with app.app_context():
        yield app  # This is where testing happens

    mongoengine.connection.disconnect_all()


@pytest.fixture(scope="session")
def client():
    """ Create app client for testing. """
    with app.test_client() as client:
        yield client  # This is where testing happens


@pytest.fixture(scope="session")
def db(app):
    """ Create database for testing. """

    # app.config["MONGODB_HOST"] = "mongo"
    test_db = MongoEngine(app)
    db_name = test_db.connection.get_database("test_quotes_database").name

    if not db_name.endswith("_quotes_database"):
        raise RuntimeError(
            f"DATABASE_URL must point to testing db, not to master db ({db_name})"
        )

    # Clear database before tests, for cases when some test failed before.
    test_db.connection.drop_database(db_name)

    print(db_name)

    yield test_db  # This is where testing happens

    # Clear database after tests, for graceful exit.
    test_db.connection.drop_database(db_name)


@pytest.fixture(scope="session")
def user(db):
    """ Create user model instance for test database. """

    class User(db.Document, UserFields):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    return User


@pytest.fixture(scope="session")
def token_blacklist(db):
    """ Create token blacklist model instance for test database. """

    class TokenBlacklist(db.Document, TokenBlacklistFields):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    return TokenBlacklist


@pytest.fixture(scope="session")
def quote(db):
    """ Create quote model instance for test database. """

    class Quote(db.Document, QuoteFields):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    return Quote


@pytest.fixture(scope="module")
def new_user(user):
    """ Create new user for testing. """

    User = user

    # User mock data
    user_data = {
        "username": "user",
        "email": "user@email.com",
        "password": "user",
    }

    new_user = User(**user_data)
    new_user.save()

    return new_user


@pytest.fixture(scope="module")
def new_admin(user):
    """ Create new admin user for testing. """
    User = user

    # Admin user mock data
    admin_user_data = {
        "username": "admin",
        "email": "admin@email.com",
        "password": "admin",
    }

    new_admin = User(**admin_user_data)
    new_admin.save()

    return new_admin


@pytest.fixture(scope="module")
def new_quote(quote):
    """ Create new quote for testing. """

    Quote = quote

    # Quote mock data
    quote_data = {
        "quote_text": "Quote.",
        "author_name": "Author",
        "author_image": "URL",
        "tags": ["test-tag"],
    }

    new_quote = Quote(**quote_data)
    new_quote.save()

    return new_quote


@pytest.fixture(scope="module")
def new_access_token(new_user, token_blacklist):
    """ Create new access token for testing. """

    TokenBlacklist = token_blacklist

    access_token_data = {
        "jti": "jti_example",
        "token_type": "access",
        "user": new_user,
        "revoked": False,
        "expires": datetime.fromtimestamp(1608057500),
    }

    token = TokenBlacklist(**access_token_data)
    token.save()

    return token


@pytest.fixture(scope="module")
def new_refresh_token(new_user, token_blacklist):
    """ Create new refresh token for testing. """

    TokenBlacklist = token_blacklist

    refresh_token_data = {
        "jti": "jti_example",
        "token_type": "refresh",
        "user": new_user,
        "revoked": False,
        "expires": datetime.fromtimestamp(1608057500),
    }

    token = TokenBlacklist(**refresh_token_data)
    token.save()

    return token
