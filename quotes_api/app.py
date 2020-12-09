import os
from flask import Flask

from quotes_api import api, auth
from quotes_api.extensions import jwt, odm, ma, apispec


def create_app(configuration="ProductionConfig"):
    """ Application factory, used to create an application. """

    # Create Flaks application
    app = Flask("quotes_api")

    print("Initial configuration:", app.config)

    # Setup app configuration from configuration object
    settings = "quotes_api.config.{}".format(configuration)

    print("Settings:", settings)
    app.config.from_object(settings)

    print("Final configuration:", app.config)

    configure_extensions(app)
    configure_apispec(app)
    register_blueprints(app)

    return app


def configure_apispec(app):
    """ Configure APISpec for swagger support. """
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
    """ Configure flask extensions. """
    odm.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)


def register_blueprints(app):
    """ Register all blueprints for an application. """

    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(auth.views.blueprint)

