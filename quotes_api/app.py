import os
from flask import Flask

from quotes_api import api
from quotes_api.extensions import odm


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

    return app


def configure_extensions(app):
    """ Configure flask extensions. """
    odm.init_app(app)


def register_blueprints(app):
    """ Register all blueprints for an application. """
    app.register_blueprint(api.views.blueprint)

