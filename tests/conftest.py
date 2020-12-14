""" Defines fixtures available to all tests. """

import pytest

from quotes_api.extensions import odm as _db


@pytest.fixture
def app():
    """ Create application for the tests. """
    pass


@pytest.fixture
def db(app):
    """ Create database for the tests. """
    pass


@pytest.fixture
def basic_user(db):
    """ Create basic user for the tests. """
    pass


@pytest.fixture
def admin_user(db):
    """ Create admin user for the tests. """
    pass

