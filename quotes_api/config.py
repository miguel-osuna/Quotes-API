""" 
Environment configuration
"""

import os


class Config(object):
    """ Configuration base class. """

    # FLask Configuration
    DEBUG = False
    TESTING = False

    # Mongoengine Configuration
    DATABASE_URI = os.getenv("DATABASE_URI")  # Remove it?
    MONGO_INITDB_ROOT_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")  # Remove it?
    MONGO_INITDB_ROOT_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")  # Remove it?
    MONGO_INITDB_DATABASE = os.getenv("MONGO_INIDB_DATABASE")  # Remove it?


class ProductionConfig(Config):
    """ Production environment configuration class. """

    ENV = "production"
    DATABASE_URI = ""


class DevelopmentConfig(Config):
    """ Development environment configuration class. """

    ENV = "development"
    DEBUG = True


class TestingConfig(Config):
    """ Testing environment configuration class. """

    ENV = "development"
    TESTING = True

