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

from quotes_api.auth.resources import (
    UserSignup,
    UserLogin,
    UserLogout,
    UserResource,
    UserList,
    UserTokens,
    TokenRefresh,
    AccessTokenRevoke,
    RefreshTokenRevoke,
    TrialToken,
    PermanentToken,
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
    tag_object = [
        {"name": "Quote", "description": "Access to quote service."},
        {"name": "Authors", "description": "Access to authors service."},
        {"name": "Tags", "description": "Access to tags service."},
        {"name": "User", "description": "Access to user service."},
        {"name": "Api Key", "description": "Access to api key service."},
    ]

    info_object = {
        "description": "Quotes API is a *REST API* that offers access to its feature rich platform. Serve some of the most **famous quotes** from all time. This is an interactive API documentation, feel free to try it.",
        "contact": {
            "name": "Miguel Osuna",
            "url": "https://www.miguel-osuna.com",
            "email": "contact@miguel-osuna.com",
        },
    }

    security_requirement_object = {}

    app.config.update(
        {
            "APISPEC_SPEC": APISpec(
                title="Quotes API",
                version="v1",
                plugins=[MarshmallowPlugin()],
                openapi_version="3.0.3",
                info=info_object,
                tags=tag_object,
                # security=security_requirement_object,
            ),
            "APISPEC_SWAGGER_URL": "/docs-text/",
            "APISPEC_SWAGGER_UI_URL": "/docs/",
        }
    )


def register_apispec_resources(docs):
    """ Register apispec endpoints for documentation. """
    api_blueprint = "api"
    auth_blueprint = "auth"

    docs.register(QuoteResource, blueprint=api_blueprint, endpoint="quote")
    docs.register(QuoteList, blueprint=api_blueprint, endpoint="quotes")
    docs.register(QuoteRandom, blueprint=api_blueprint, endpoint="random_quote")
    docs.register(AuthorList, blueprint=api_blueprint, endpoint="authors")
    docs.register(TagList, blueprint=api_blueprint, endpoint="tags")

    docs.register(UserSignup, blueprint=auth_blueprint, endpoint="user_signup")
    docs.register(UserLogin, blueprint=auth_blueprint, endpoint="user_login")
    docs.register(UserLogout, blueprint=auth_blueprint, endpoint="user_logout")
    docs.register(UserResource, blueprint=auth_blueprint, endpoint="user_by_id")
    docs.register(UserList, blueprint=auth_blueprint, endpoint="users")
    docs.register(UserTokens, blueprint=auth_blueprint, endpoint="tokens")
    docs.register(TokenRefresh, blueprint=auth_blueprint, endpoint="token_refresh")
    docs.register(
        AccessTokenRevoke, blueprint=auth_blueprint, endpoint="revoke_access_revoke"
    )
    docs.register(
        RefreshTokenRevoke, blueprint=auth_blueprint, endpoint="revoke_refresh_token"
    )
    docs.register(TrialToken, blueprint=auth_blueprint, endpoint="trial_token")
    docs.register(PermanentToken, blueprint=auth_blueprint, endpoint="permanent_token")


def configure_extensions(app):
    """ Configure flask extensions. """
    odm.init_app(app)
    jwt.init_app(app)
    docs.init_app(app)


def register_blueprints(app):
    """ Register all blueprints for an application. """

    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(auth.views.blueprint)

