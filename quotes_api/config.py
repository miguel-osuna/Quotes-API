""" Environment configuration file."""

import os


class Config(object):
    """Configuration base class."""

    # Quotes API Variables
    SERVER = os.getenv("SERVER")

    # Flask Configuration
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Fask JWT Extended Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = 15 * 60  # 15 minutes in seconds
    JWT_REFRESH_TOKEN_EXPIRES = 30 * 24 * 60 * 60  # 30 days in seconds
    JWT_ERROR_MESSAGE_KEY = "message"


class ProductionConfig(Config):
    """Production environment configuration class."""

    # Flask Configuration
    ENV = "production"

    # Mongoengine Configuration
    MONGODB_DB = os.getenv("MONGODB_DB")
    MONGODB_HOST = os.getenv("MONGODB_HOST")


class DevelopmentConfig(Config):
    """Development environment configuration class."""

    # Flask Configuration
    ENV = "development"
    DEBUG = True

    # Mongoengine Configuration
    MONGODB_DB = os.getenv("MONGODB_DB")
    MONGODB_HOST = os.getenv("MONGODB_HOST")


class TestingConfig(Config):
    """Testing environment configuration class."""

    # Flask Configuration
    ENV = "development"
    DEBUG = True
    TESTING = True
    SECRET_KEY = "testing"

    # Mongoengine Configuration
    MONGODB_DB = "test_quotes_database"
    MONGODB_HOST = "mongo"


# App configuration dictionary
app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
