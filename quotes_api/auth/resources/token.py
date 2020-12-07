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

from quotes_api.models import User, TokenBlacklist
from quotes_api.auth.helpers import (
    revoke_token,
    add_token_to_database,
)
from quotes_api.auth.decorators import user_required, admin_required
from quotes_api.common import HttpStatus, paginator
from quotes_api.auth.schemas.blacklist import TokenBlacklistSchema


class UserTokens(Resource):
    """ 
    User tokens list resource. 
    
    Provides a way for a user to look at their tokens
    """

    # Decorators applied to all class methods
    method_decorators = []

    # @doc(description="Get list of token resources.", tags=["Api Key"])
    @user_required
    def get(self):
        """ Gets all the revoked and unrevoked tokens from a user. """

        args = request.args

        page = int(args.get("page", 1))
        per_page = int(args.get("per_page", 5))

        try:
            # Generating pagination of tokens
            user_identity = get_jwt_identity()
            user = User.objects.get(username=user_identity)
            pagination = TokenBlacklist.objects(user=user).paginate(
                page=page, per_page=per_page
            )

            response_body = paginator(pagination, "auth.tokens", TokenBlacklistSchema)
            return make_response(response_body, HttpStatus.ok_200.value)

        except Exception as e:
            return (
                {"erorr": "Could not retrieve tokens.", "detail": str(e)},
                HttpStatus.internal_server_error_500.value,
            )


class TokenRefresh(Resource):
    """ Token refresh. """

    # @doc(
    #     description="Create an access token from a refresh token.", tags=["Api Key"],
    # )
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
            return make_response(response_body, HttpStatus.ok_200.value)

        except:
            return (
                {"error": "Missing valid refresh token"},
                HttpStatus.bad_request_400.value,
            )


class AccessTokenRevoke(Resource):
    """ Access Token Revoke resource. """

    # @doc(description="Revoke an access token.", tags=["Api Key"])
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

    # @doc(description="Revokes a refresh token.", tags=["Api Key"])
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

    # @doc(description="Create a trial api key.", tags=["Api Key"])
    @admin_required
    def post(self):
        """ Creates a trial api key. """

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

            response_body = {"trialApiKey": token}
            return make_response(response_body, HttpStatus.created_201.value)

        except:
            return (
                {"error": "Missing valid refresh token"},
                HttpStatus.bad_request_400.value,
            )


class PermanentToken(Resource):
    """ Permanent api key creation resource. """

    # @doc(description="Create a permanent api key.", tags=["Api Key"])
    @admin_required
    def post(self):
        """ Creates a permanent api key. """

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

            response_body = {"permanentApiKey": token}
            return make_response(response_body, HttpStatus.created_201.value)

        except:
            return (
                {"error": "Missing valid refresh token"},
                HttpStatus.bad_request_400.value,
            )

