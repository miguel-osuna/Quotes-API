""" 
Environment configuration
"""

import os


class Config(object):
    """ Configuration base class. """

    # Flask Configuration
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")


class ProductionConfig(Config):
    """ Production environment configuration class. """

    # Flask Configuration
    ENV = "production"

    # Mongoengine Configuration
    MONGODB_DB = os.getenv("MONGODB_DB")
    MONGODB_HOST = os.getenv("MONGODB_HOST")


class StagingConfig(Config):
    """ Staging environment configuration class. """

    # Flask Configuration
    ENV = "production"

    # Mongoengine Configuration
    MONGODB_DB = os.getenv("MONGODB_DB")
    MONGODB_HOST = os.getenv("MONGODB_HOST")


class DevelopmentConfig(Config):
    """ Development environment configuration class. """

    # Flask Configuration
    ENV = "development"
    DEBUG = True
    SERVER_NAME = "127.0.0.1:8000"

    # Mongoengine Configuration
    MONGODB_DB = os.getenv("MONGODB_DB")
    MONGODB_HOST = os.getenv("MONGODB_HOST")
    MONGODB_PORT = int(os.getenv("MONGODB_PORT"))


class TestingConfig(Config):
    """ Testing environment configuration class. """

    # Flask Configuration
    ENV = "development"
    TESTING = True

