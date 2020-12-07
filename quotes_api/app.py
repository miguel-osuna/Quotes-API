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


# def configure_apispec(app):


#     """ Configure apispec for api documentation. """
#     tag_object = [
#         {"name": "Quote", "description": "Access to quote service."},
#         {"name": "Authors", "description": "Access to authors service."},
#         {"name": "Tags", "description": "Access to tags service."},
#         {"name": "User", "description": "Access to user service."},
#         {"name": "Api Key", "description": "Access to api key service."},
#     ]

#     info_object = {
#         "description": "",
#         "contact": {
#             "name": "Miguel Osuna",
#             "url": "https://www.miguel-osuna.com",
#             "email": "contact@miguel-osuna.com",
#         },
#     }

#     security_requirement_object = {}

#     app.config.update(
#         {
#             "APISPEC_SPEC": APISpec(
#                 title="Quotes API",
#                 version="v1",
#                 plugins=[MarshmallowPlugin()],
#                 openapi_version="3.0.3",
#                 info=info_object,
#                 tags=tag_object,
#                 # security=security_requirement_object,
#             ),
#             "APISPEC_SWAGGER_URL": "/docs-text/",
#             "APISPEC_SWAGGER_UI_URL": "/docs/",
#         }
#     )


def configure_apispec(app):
    """ Configure APISpec for swagger support. """
    apispec.init_app(app, security=[{"jwt": []}])

    jwt_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    apispec.spec.components.security_scheme("jwt", jwt_scheme)


def configure_extensions(app):
    """ Configure flask extensions. """
    odm.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)


def register_blueprints(app):
    """ Register all blueprints for an application. """

    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(auth.views.blueprint)

