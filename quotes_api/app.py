import os
from flask import Flask

from quotes_api import api, auth
from quotes_api.extensions import jwt, odm, ma, apispec


def create_app(configuration="ProductionConfig"):
    """ Applicaiton factory, used to create an application. """

    # Create Flaks application
    app = Flask("quotes_api")

    # Setup app configuration from configuration object
    settings = "quotes_api.config.{}".format(configuration)
    app.config.from_object(settings)

    configure_extensions(app)
    configure_apispec(app)
    register_blueprints(app)

    return app


def configure_apispec(app):
    """ Configure APISpec for swagger support. """
    apispec.init_app(app)  # security=[{"user_api_key": []}])

    jwt_scheme = {
        "type": "http",
        "description": "Enter a valid api key",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    apispec.spec.components.security_scheme("user_api_key", jwt_scheme)
    apispec.spec.components.security_scheme("admin_api_key", jwt_scheme)


def configure_extensions(app):
    """ Configure flask extensions. """
    odm.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)


def register_blueprints(app):
    """ Register all blueprints for an application. """

    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(auth.views.blueprint)

