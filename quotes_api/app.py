from flask import Flask

from quotes_api import api
from quotes_api.extensions import odm


def create_app(configuration="ProductionConfig"):
    """ Applicaiton factory, used to create an application. """
    # Users a configuration object as the app's settings
    settings = "config.{}".format(configuration)
    app = Flask("quotes_api")
    app.config.from_object(settings)

    configure_extensions(app)
    register_blueprints(app)

    return app

def configure_extensions(app):
    """ Configure flask extensions. """
    odm.init_app(app)


def register_blueprints(app):
    """ Register all blueprints for an application. """
    app.register_blueprint(api.views.blueprint)

