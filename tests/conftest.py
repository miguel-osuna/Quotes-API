"""
Defines fixtures available to all tests.
"""

from datetime import datetime

import pytest
import mongoengine
from flask import url_for
from flask_mongoengine import MongoEngine
from passlib.context import CryptContext

from quotes_api.app import create_app
from quotes_api.api.models import QuoteFields
from quotes_api.auth.models import UserFields, TokenBlacklistFields


@pytest.fixture(name="password_hasher")
def fixture_password_hasher():
    """Hashes a password using sha256 encryption."""

    pwd_context = CryptContext(schemes=["sha256_crypt"])
    return pwd_context


@pytest.fixture(name="app")
def fixture_app():
    """Create application for testing."""

    app = create_app("testing")

    with app.app_context():
        yield app

    mongoengine.connection.disconnect_all()


@pytest.fixture(name="database")
def fixture_database(app):
    """Create database for testing."""

    test_db = MongoEngine(app)
    db_name = test_db.connection.get_database("test_quotes_database").name

    if not db_name.endswith("_quotes_database"):
        raise RuntimeError(
            f"DATABASE_URL must point to testing database, not to master database ({db_name})"
        )

    # Clear database before tests, for cases when some test failed before.
    test_db.connection.drop_database(db_name)

    yield test_db  # This is where testing happens

    # Clear database after tests, for graceful exit.
    test_db.connection.drop_database(db_name)


@pytest.fixture(name="user_model")
def fixture_user_model(database):
    """Create user model instance for test database."""

    class User(database.Document, UserFields):
        """Test user database model."""

        def __init__(self, *args, **kwargs):  # pylint: disable=useless-super-delegation
            super().__init__(*args, **kwargs)

    return User


@pytest.fixture(name="token_blacklist_model")
def fixture_token_blacklist_model(database):
    """Create token blacklist model instance for test database."""

    class TokenBlacklist(database.Document, TokenBlacklistFields):
        """Test token blacklist database model."""

        def __init__(self, *args, **kwargs):  # pylint: disable=useless-super-delegation
            super().__init__(*args, **kwargs)

    return TokenBlacklist


@pytest.fixture(name="quote_model")
def fixture_quote_model(database):
    """Create quote model instance for test database."""

    class Quote(database.Document, QuoteFields):
        """Test quote database model."""

        def __init__(self, *args, **kwargs):  # pylint: disable=useless-super-delegation
            super().__init__(*args, **kwargs)

    return Quote


@pytest.fixture(name="new_user")
def fixture_new_user(user_model, password_hasher):
    """Create new user for testing."""

    # User mock data
    user_data = {
        "username": "user",
        "email": "user@email.com",
        "password": password_hasher.hash("user"),
    }

    new_user = user_model(**user_data)
    new_user.save()

    return new_user


@pytest.fixture(name="new_admin")
def fixture_new_admin(user_model, password_hasher):
    """Create new admin user for testing."""

    # Admin user mock data
    admin_user_data = {
        "username": "admin",
        "email": "admin@email.com",
        "password": password_hasher.hash("admin"),
        "roles": ["basic", "admin"],
    }

    new_admin = user_model(**admin_user_data)
    new_admin.save()

    return new_admin


@pytest.fixture(name="new_quote")
def fixture_new_quote(quote_model):
    """Create new quote for testing."""

    # Quote mock data
    quote_data = {
        "quote_text": "Quote.",
        "author_name": "Author",
        "author_image": "https://www.goodreads.com/quotes/tag/books",
        "tags": ["test-tag"],
    }

    new_quote = quote_model(**quote_data)
    new_quote.save()

    return new_quote


@pytest.fixture(name="new_access_token")
def fixture_new_access_token(new_user, token_blacklist_model):
    """Create new access token for testing."""

    access_token_data = {
        "jti": "jti_example",
        "token_type": "access",
        "user": new_user,
        "revoked": False,
        "expires": datetime.fromtimestamp(1608057500),
    }

    token = token_blacklist_model(**access_token_data)
    token.save()

    return token


@pytest.fixture(name="new_refresh_token")
def fixture_new_refresh_token(new_user, token_blacklist_model):
    """Create new refresh token for testing."""

    refresh_token_data = {
        "jti": "jti_example",
        "token_type": "refresh",
        "user": new_user,
        "revoked": False,
        "expires": datetime.fromtimestamp(1608057500),
    }

    token = token_blacklist_model(**refresh_token_data)
    token.save()

    return token


@pytest.fixture(name="user_headers")
def fixture_user_headers(new_user, client):
    """Generate access token authorization headers for a user."""

    data = {"username": new_user.username, "password": "user"}
    login_url = url_for("auth.user_login")
    res = client.post(login_url, json=data)
    data = res.get_json()
    access_token = data["access_token"]

    return {
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}",
    }


@pytest.fixture(name="admin_headers")
def fixture_admin_headers(new_admin, client):
    """Generate access token authorization headers for admin."""

    data = {"username": new_admin.username, "password": "admin"}
    login_url = url_for("auth.user_login")
    res = client.post(login_url, json=data)
    data = res.get_json()
    access_token = data["access_token"]

    return {
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}",
    }


@pytest.fixture(name="admin_refresh_headers")
def fixture_admin_refresh_headers(new_admin, client):
    """Generate refresh token authorization headers for admin."""

    data = {"username": new_admin.username, "password": "admin"}
    login_url = url_for("auth.user_login")
    res = client.post(login_url, json=data)
    data = res.get_json()
    refresh_token = data["refresh_token"]

    return {
        "content-type": "application/json",
        "authorization": f"Bearer {refresh_token}",
    }
