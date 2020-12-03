from datetime import timedelta
from flask import request, jsonify, make_response, current_app as app
from flask_restful import Resource

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)

from quotes_api.models import User
from quotes_api.auth.helpers import (
    revoke_token,
    add_token_to_database,
)
from quotes_api.auth.decorators import user_required, admin_required
from quotes_api.common import HttpStatus


class TokenRefresh(Resource):
    """ Token refresh. """

    @jwt_refresh_token_required
    def post(self):
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


class AccessTokenRevoke(Resource):
    """ Access Token Revoke resource. """

    @jwt_required
    def delete(self):
        """ Revokes an access token from the database. 
        
        Used mainly for logout
        """
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


class RefreshTokenRevoke(Resource):
    """ Refresh Token Revoked resource. """

    @jwt_refresh_token_required
    def delete(self):
        """ Revokes a refresh token from the database.
        
        Used mainly for logout.
        """

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


class TrialToken(Resource):
    """ Trial api key creation resource. """

    @admin_required
    def post(self):
        """ Creates a trial development token. """

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


class PermanentToken(Resource):
    """ Permanent api key creation resource. """

    @admin_required
    def post(self):
        """ Creates a permanent api token. """

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
