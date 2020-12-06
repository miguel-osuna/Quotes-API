import os
from flask import Flask

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from quotes_api import api, auth
from quotes_api.extensions import jwt, odm, docs
from quotes_api.api.resources import (
    QuoteResource,
    QuoteList,
    QuoteRandom,
    AuthorList,
    TagList,
)


def create_app(configuration="ProductionConfig"):
    """ Applicaiton factory, used to create an application. """

    # Create Flaks application
    app = Flask("quotes_api")

    # print("Class: ", os.getenv("APP_CONFIGURATION"))
    # print("Application File: ", configuration)
    # print("Initial App Configuration: ", app.config)

    # Setup app configuration from configuration object
    settings = "quotes_api.config.{}".format(configuration)
    app.config.from_object(settings)

    # print("Final App Configuration: ", app.config)
    configure_apispec(app)
    configure_extensions(app)
    register_blueprints(app)
    register_apispec_resources(docs)

    return app


def configure_apispec(app):
    """ Configure apispec for api documentation. """
    app.config.update(
        {
            "APISPEC_SPEC": APISpec(
                title="Quotes API",
                version="v1",
                plugins=[MarshmallowPlugin()],
                openapi_version="3.0.3",
                info={
                    "description": "REST API that provides famous quotes from all time. "
                },
            ),
            "APISPEC_SWAGGER_URL": "/docs-text/",
            "APISPEC_SWAGGER_UI_URL": "/docs/",
        }
    )


def register_apispec_resources(docs):
    """ Register apispec endpoints for documentation. """
    docs.register(QuoteResource, blueprint="api", endpoint="quote")
    docs.register(QuoteList, blueprint="api", endpoint="quotes")
    docs.register(QuoteRandom, blueprint="api", endpoint="random_quote")
    docs.register(AuthorList, blueprint="api", endpoint="authors")
    docs.register(TagList, blueprint="api", endpoint="tags")


def configure_extensions(app):
    """ Configure flask extensions. """
    odm.init_app(app)
    jwt.init_app(app)
    docs.init_app(app)


def register_blueprints(app):
    """ Register all blueprints for an application. """

    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(auth.views.blueprint)

