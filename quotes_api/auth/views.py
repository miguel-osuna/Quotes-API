from datetime import timedelta
from flask import make_response, request, jsonify, Blueprint, current_app as app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    fresh_jwt_required,
    get_jwt_identity,
    get_raw_jwt,
    decode_token,
)

from quotes_api.models import User
from quotes_api.extensions import pwd_context, jwt
from quotes_api.auth.helpers import (
    revoke_token,
    is_token_revoked,
    get_user_tokens,
    add_token_to_database,
)
from quotes_api.common import HttpStatus

blueprint = Blueprint("auth", __name__, url_prefix="/auth")

# CALLBACK FUNCTIONS
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


# ROUTING
@blueprint.route("/signup", methods=["POST"])
def register():
    """ User registration to the database. """
    try:
        # Get data from request
        data = request.get_json()

        username = data["username"]
        email = data["email"]
        password = data["password"]

        try:
            user = User(username=username, email=email, password=password)
            user.save()

            return {"message": "Successful sign up."}, HttpStatus.created_201.value

        except:
            return (
                {"error": "Could not sign up user."},
                HttpStatus.internal_server_error_500.value,
            )

    except:
        return {"error": "Missing data"}, HttpStatus.bad_request_400.value


@blueprint.route("/login", methods=["POST"])
def login():
    """ Authenticate a user and return tokens. """

    try:
        # Get data from request
        data = request.get_json()

        username = data["username"]
        password = data["password"]

        try:
            # Check if there's a match for the user in the database
            user = User.objects(username=str(username)).first()

            # Check the passwords match
            if not pwd_context.verify(password, user.password):
                print("Password:", password)
                print("Hashed password:", user.password)
                raise Exception("Wrong password")

            # Store tokens in our database with a status of currently not revoked

            # We pass the user instance as the "identity" for the tokens.  With this,
            # callback function have access to the complete object, avoiding
            # queries to the database.
            access_token = create_access_token(identity=user, fresh=True)
            refresh_token = create_refresh_token(identity=user)

            # Add new tokens to the database
            # JWT_IDENTITY_CLAIM is an identity claim and it defaults to "identity"
            add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
            add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])

            response_body = {"accessToken": access_token, "refreshToken": refresh_token}
            return make_response(jsonify(response_body), HttpStatus.ok_200.value)

        except:
            return (
                {"error": "Wrong credentials"},
                HttpStatus.unauthorized_401.value,
            )

    except:
        return {"error": "Missing data."}, HttpStatus.bad_request_400.value


@blueprint.route("/logout", methods=["POST"])
@fresh_jwt_required
def logout():
    pass


# Provide a way for a user to look at their tokens
@blueprint.route("/tokens", methods=["GET"])
@jwt_required
def get_tokens():
    """ Get all the tokens from the user identity stored in the jwt. """
    try:
        user_identity = get_jwt_identity()
        all_tokens = get_user_tokens(user_identity)
        response_body = {"tokens": [token.to_dict() for token in all_tokens]}

        return make_response(jsonify(response_body), HttpStatus.ok_200.value)

    except Exception as e:
        return (
            {"error": "Could not get tokens", "detail": str(e)},
            HttpStatus.internal_server_error_500.value,
        )


# Revoked refresh tokens will not be able to access this endpoint
@blueprint.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    """ Get an access token from a refresh token. """

    try:
        # Get the current user id from the access token to retrieve
        # the user from the database
        user_identity = get_jwt_identity()
        current_user = User.objects.get(username=user_identity)

        # We pass the "current_user" User instance as the token identity.
        access_token = create_access_token(identity=current_user, fresh=False)

        # Add new access token to the database
        # JWT_IDENTITY_CLAIM is an identity claim and it defaults to "identity"
        add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])

        response_body = {"accessToken": access_token}
        return make_response(jsonify(response_body), HttpStatus.ok_200.value)

    except:
        return (
            {"error": "Missing valid refresh token"},
            HttpStatus.bad_request_400.value,
        )


# Revoked access tokens will not be able to access this endpoint
@blueprint.route("/revoke_access", methods=["DELETE"])
@jwt_required
def revoke_access_token():
    """ Revoke an access token. """

    try:
        # Get the JWT ID and the user identity respectively
        jti = get_raw_jwt()["jti"]
        user_identity = get_jwt_identity()

        revoke_token(jti, user_identity)
        return "", HttpStatus.no_content_204.value

    except:
        return (
            {"error": "Could not revoke access token."},
            HttpStatus.internal_server_error_500.value,
        )


@blueprint.route("revoke_refresh", methods=["DELETE"])
@jwt_refresh_token_required
def revoke_refresh_token():
    """ Revoke a refresh token, used mainly for logout. """

    try:
        # Get the JWT ID and the user identity respectively
        jti = get_raw_jwt()["jti"]
        user_identity = get_jwt_identity()

        revoke_token(jti, user_identity)
        return "", HttpStatus.no_content_204.value

    except:
        return (
            {"error": "Could not revoke refresh token."},
            HttpStatus.internal_server_error_500.value,
        )


@blueprint.route("/create_dev_token", methods=["POST"])
@jwt_required
def create_dev_token():
    """ Creates a trial development token. This token is not added to the blacklist. """

    try:
        # Get the current identity from the access token to retrieve
        # the user from the database
        user_identity = get_jwt_identity()
        expires = timedelta(days=365)
        current_user = User.objects.get(username=user_identity)

        # We pass the "current_user" User instance as the token identity.
        token = create_access_token(
            identity=current_user, expires_delta=expires, fresh=False
        )

        # Add new tokens to the database
        # JWT_IDENTITY_CLAIM is an identity claim and it defaults to "identity"
        add_token_to_database(token, app.config["JWT_IDENTITY_CLAIM"])

        response_body = {"token": token}
        return make_response(jsonify(response_body), HttpStatus.created_201.value)

    except:
        return (
            {"error": "Missing valid refresh token"},
            HttpStatus.bad_request_400.value,
        )


@blueprint.route("/create_api_token", methods=["POST"])
@jwt_required
def create_api_token():
    """ Creates a permanent api token. This token is not added to the blacklist. """

    try:
        # Get the current user id from the access token to retrieve
        # the user from the database
        user_identity = get_jwt_identity()
        expires = False

        # We pass the "current_user" User instance as the token identity.
        current_user = User.objects.get(username=user_identity)
        token = create_access_token(
            identity=current_user, expires_delta=expires, fresh=False
        )

        # Add new tokens to the database
        # JWT_IDENTITY_CLAIM is an identity claim and it defaults to "identity"
        add_token_to_database(token, app.config["JWT_IDENTITY_CLAIM"])

        response_body = {"token": token}
        return make_response(jsonify(response_body), HttpStatus.created_201.value)

    except:
        return (
            {"error": "Missing valid refresh token"},
            HttpStatus.bad_request_400.value,
        )

