from datetime import timedelta
from flask import Blueprint, current_app, jsonify, current_app as app
from flask_restful import Api

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
from quotes_api.models import User
from quotes_api.auth.schemas import UserSchema, TokenBlacklistSchema
from quotes_api.extensions import pwd_context, jwt, apispec
from quotes_api.common import HttpStatus
from quotes_api.auth.helpers import is_token_revoked

blueprint = Blueprint("auth", __name__, url_prefix="/auth")

api = Api(blueprint)

# Ruote all resources
api.add_resource(UserSignup, "/signup", endpoint="user_signup")
api.add_resource(UserLogin, "/login", endpoint="user_login")
api.add_resource(UserLogout, "/logout", endpoint="user_logout")
api.add_resource(UserResource, "/users/<user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")
api.add_resource(UserTokens, "/tokens", endpoint="tokens")
api.add_resource(TokenRefresh, "/refresh", endpoint="token_refresh")
api.add_resource(
    AccessTokenRevoke, "/revoke_access_token", endpoint="revoke_access_revoke"
)
api.add_resource(
    RefreshTokenRevoke, "/revoke_refresh_token", endpoint="revoke_refresh_token"
)
api.add_resource(TrialToken, "/generate_trial_key", endpoint="trial_token")
api.add_resource(PermanentToken, "/generate_permanent_key", endpoint="permanent_token")


# Callback functions
@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    """ 
    Callback function that is called when a protected endpoint is accessed, 
    and checks if the JWT has been revoked. 
    """
    return is_token_revoked(decoded_token)


# It might be unnecessary
@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    """    
    Callback function that will be called to automatically load an object when a protected endpoint
    is accessed. 
    """
    try:
        return User.objects.get(username=identity)
    except:
        return None


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    """ 
    Callback function that is called whenever "create_access_token" is used.
    
    Adds custom user claims to the access token, and takes a User instance object as an argument.
    Because we have a "User" instance, and not just an ID, it's not necessary to query the database.
    """

    # Dictionary accessible with function "get_jwt_claims"
    return {"roles": user.roles}


@jwt.user_identity_loader
def user_identity_lookup(user):
    """ 
    Callback function for getting a JSON serializable identity out of a "User" object passed into
    "create_access_token" or "create_refresh_token".

    We can define what the identity of the token will be like. We want it to be a string representing
    the username. 
    """

    return user.username


# Apispec view configuration
@blueprint.before_app_first_request
def register_views():
    """ Register views for API documentation. """

    # Adding User views
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)
    apispec.spec.path(view=UserTokens, app=current_app)

    # Adding authentication views
    apispec.spec.path(view=UserSignup, app=current_app)
    apispec.spec.path(view=UserLogin, app=current_app)
    apispec.spec.path(view=UserLogout, app=current_app)
    apispec.spec.path(view=TokenRefresh, app=current_app)
    apispec.spec.path(view=AccessTokenRevoke, app=current_app)
    apispec.spec.path(view=RefreshTokenRevoke, app=current_app)
    apispec.spec.path(view=TrialToken, app=current_app)
    apispec.spec.path(view=PermanentToken, app=current_app)

