import os
from flask import Flask, render_template

from cli import register_cli_commands
from quotes_api import api, auth
from quotes_api.config import app_config
from quotes_api.extensions import jwt, odm, ma, cors, apispec


def create_app(configuration="production"):
    """Application factory, used to create an application."""

    # Create Flaks application
    app = Flask("quotes_api", template_folder="templates")

    # Setup app configuration from configuration object
    app.config.from_object(app_config[configuration])

    configure_extensions(app)
    configure_apispec(app)
    register_blueprints(app)
    register_commands(app)

    return app


def configure_apispec(app):
    """Configure APISpec for swagger support."""
    apispec.init_app(app)

    user_api_key_scheme = {
        "type": "http",
        "description": "Enter a valid user api key",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    admin_api_key_scheme = {
        "type": "http",
        "description": "Enter a valid admin api key",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    apispec.spec.components.security_scheme("user_api_key", user_api_key_scheme)
    apispec.spec.components.security_scheme("admin_api_key", admin_api_key_scheme)


def configure_extensions(app):
    """Configure flask extensions."""
    odm.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    cors.init_app(app)


def register_blueprints(app):
    """Register all blueprints for an application."""

    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(auth.views.blueprint)


def register_commands(app):
    """
    Register commands for the Flask application.

    :param app: Flask application instance
    :return: None
    """
    register_cli_commands(app)
    return None
