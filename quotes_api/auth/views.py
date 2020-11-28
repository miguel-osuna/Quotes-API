from datetime import timedelta
from flask import make_response, request, jsonify, Blueprint, current_app as app

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)

from quotes_api.models import User
from quotes_api.extensions import pwd_context, jwt
from quotes_api.auth.helpers import (
    revoke_token,
    is_token_revoked,
    add_token_to_database,
)
from quotes_api.common import HttpStatus

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@blueprint.route("/login", methods=["POST"])
def login():
    """ Authenticate a user and return tokens. """

    try:
        # Get data from request
        data = request.get_json()

        username = data["username"]
        password = data["password"]

        print("Username:", username)
        print("Password:", password)

        try:
            # Check if there's a match for the user in the database
            user = User.objects.first(username=username)
            print("User:", user)

            # Check the passwords match
            if not pwd_context.verify(password, user.password):
                raise Exception

            # Create an access token and refresh token
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))

            # JWT_IDENTITY_CLAIM is an identity claim and it defaults to "identity"
            add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
            add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])

            response_body = {"accessToken": access_token, "refreshToken": refresh_token}
            return make_response(jsonify(response_body), HttpStatus.ok_200.value)

        except:
            return {"error": "Wrong credentials"}, HttpStatus.unauthorized_401.value

    except:
        return {"error": "Missing data."}, HttpStatus.bad_request_400.value


@blueprint.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    """ Get an access token from a refresh token. """

    # Get the current user ID from the access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    # Add new access token to the database
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])

    response_body = {"accessToken": access_token}
    return make_response(jsonify(response_body), HttpStatus.ok_200.value)


@blueprint.route("/revoke_access", methods=["DELETE"])
@jwt_required
def revoke_access_token():
    """ Revoke an access token. """

    # Get the JWT ID and the User ID respectively
    jti = get_raw_jwt()["jti"]
    user_identity = get_jwt_identity()

    revoke_token(jti, user_identity)
    return {"message": "Token revoked."}, HttpStatus.ok_200.value


@blueprint.route("revoke_refresh", methods=["DELETE"])
@jwt_refresh_token_required
def revoke_refresh_token():
    """ Revoke a refresh token, used mainly for logout. """

    # Get the JWT ID and the User ID respectively
    jti = get_raw_jwt()["jti"]
    user_identity = get_jwt_identity()

    revoke_token(jti, user_identity)
    return {"message": "Token revoked."}, HttpStatus.ok_200.value


@blueprint.route("/create_dev_token", methods=["POST"])
@jwt_required
def create_dev_token():
    """ Creates a trial development token. """
    user_identity = get_jwt_identity()
    expires = timedelta(days=365)
    token = create_access_token(user_identity, expires_delta=expires)

    response_body = {"token": token}
    return make_response(jsonify(response_body), HttpStatus.created_201.value)


@blueprint.route("/create_api_token", methods=["POST"])
@jwt_required
def create_api_token():
    """ Creates a permanent api token. """
    user_identity = get_jwt_identity()
    expires = False
    token = create_access_token(user_identity, expires)

    response_body = {"token": token}
    return make_response(jsonify(response_body), HttpStatus.created_201.value)


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    """ JWT callback function that is called to load a user object using the id from the token. """
    return User.objects.first(id=identity)


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    """ JWT callback function that is called to check if the JWT has been revoked. """
    return is_token_revoked(decoded_token)

