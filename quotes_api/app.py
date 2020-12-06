import os
from flask import Flask

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from quotes_api import api, auth
from quotes_api.extensions import jwt, odm, docs
from quotes_api.api.resources import TestResource


def create_app(configuration="ProductionConfig"):
    """ Applicaiton factory, used to create an application. """

    # Create Flaks application
    app = Flask("quotes_api")

    # print("Class: ", os.getenv("APP_CONFIGURATION"))
    # print("Application File: ", configuration)
    # print("Initial App Configuration: ", app.config)

    # Uses a configuration object as the app's settings
    settings = "quotes_api.config.{}".format(configuration)

    # Setup app configuration from configuration object
    app.config.from_object(settings)

    # print("Final App Configuration: ", app.config)

    configure_extensions(app)
    register_blueprints(app)

    # Register APISpec endopints
    docs.register(TestResource, blueprint="api", endpoint="Test")

    return app


def configure_apispec(app):
    """ Configure apispec for documentation. """
    app.config.update(
        {
            "APISPEC_SPEC": APISpec(
                title="Quotes API",
                version="v1",
                plugins=[MarshmallowPlugin()],
                openapi_version="3.0.3",
            ),
            "APISPEC_SWAGGER_URL": "/docs-text/",
            "APISPEC_SWAGGER_UI_URL": "/docs/",
        }
    )


def configure_extensions(app):
    """ Configure flask extensions. """
    odm.init_app(app)
    jwt.init_app(app)
    docs.init_app(app)


def register_blueprints(app):
    """ Register all blueprints for an application. """

    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(auth.views.blueprint)

