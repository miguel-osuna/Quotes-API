"""Token resource file."""

from datetime import timedelta
from flask import request, make_response, current_app as app
from flask_restful import Resource

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from quotes_api.models import User, TokenBlacklist
from quotes_api.auth.helpers import (
    revoke_token,
    add_token_to_database,
)
from quotes_api.auth.decorators import Role, role_required
from quotes_api.common import HttpStatus, paginator
from quotes_api.auth.schemas import TokenBlacklistSchema


class UserTokens(Resource):
    """
    User tokens list resource.

    Provides a way for a user to look at their tokens

    ---
    get:
      tags:
        - User
      description: |
        Get list of `token` resources. Requires a valid `admin` `api key` for authentication.
      security:
        - admin_api_key: []
      parameters:
        - in: path
          name: user_id
          required: true
          schema:
            type: string
          description: User ID.
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - type: object
                    properties:
                      records:
                        type: array
                        items:
                          $ref: '#/components/schemas/TokenBlacklistSchema'
        401:
          description: Missing authentication header.
    """

    # Decorators applied to all class methods
    method_decorators = []

    @role_required([Role.ADMIN])
    def get(self, user_id):
        """Gets all the revoked and unrevoked tokens from a user."""

        try:
            user = User.objects.get_or_404(id=user_id)

        except Exception:
            return (
                {"error": "User does not exist."},
                HttpStatus.NOT_FOUND_404.value,
            )

        try:
            # Generating pagination of tokens
            tokens = TokenBlacklist.objects(user=user)

            token_blacklist_schema = TokenBlacklistSchema(many=True, exclude=["user"])
            response_body = {"records": token_blacklist_schema.dump(tokens)}

            return make_response(response_body, HttpStatus.OK_200.value)

        except Exception:
            return (
                {"error": "Could not retrieve tokens."},
                HttpStatus.INTERNAL_SERVER_ERROR_500.value,
            )


class TokenRefresh(Resource):
    """
    Token refresh.

    ---
    post:
      tags:
        - Authentication
      description: |
        Create an `access token` from a `refresh token`. Requires valid `admin` `access token`.
      security:
        - admin_api_key: []
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                    example: myaccesstoken
        400:
          description: Bad request.
        401:
          description: Missing authentication header.
    """

    @role_required([Role.ADMIN])
    def post(self):
        """Get an access token from a refresh token."""

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

            response_body = {"access_token": access_token}
            return make_response(response_body, HttpStatus.OK_200.value)

        except Exception:
            return (
                {"error": "Missing valid refresh token"},
                HttpStatus.BAD_REQUEST_400.value,
            )


class AccessTokenRevoke(Resource):
    """
    Access Token Revoke resource.

    ---
    delete:
      tags:
        - Authentication
      description: |
        Revoke an `access token`. Requires a valid `admin` `access token`.
      security:
        - admin_api_key: []
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: token revoked
        400:
          description: Bad request.
        401:
          description: Missing authentication header.
    """

    @jwt_required()
    def delete(self):
        """Revokes an access token from the database.

        Used mainly for logout
        """
        try:
            # Get the JWT ID and the user identity respectively
            jti = get_jwt()["jti"]
            user_identity = get_jwt_identity()

            revoke_token(jti, user_identity)
            return "", HttpStatus.NO_CONTENT_204.value

        except Exception:
            return (
                {"error": "Could not revoke access token."},
                HttpStatus.INTERNAL_SERVER_ERROR_500.value,
            )


class RefreshTokenRevoke(Resource):
    """
    Refresh Token Revoked resource.

    ---
    delete:
      tags:
        - Authentication
      description: |
        Revokes a `refresh token`. Requires a valid `admin` `refresh token`.
      security:
        - admin_api_key: []
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: token revoked
        400:
          description: Bad request.
        401:
          description: Missing authentication header.
    """

    @jwt_required(refresh=True)
    def delete(self):
        """
        Revokes a refresh token from the database.

        Used mainly for logout.
        """

        try:
            # Get the JWT ID and the user identity respectively
            jti = get_jwt()["jti"]
            user_identity = get_jwt_identity()

            revoke_token(jti, user_identity)
            return "", HttpStatus.NO_CONTENT_204.value

        except Exception:
            return (
                {"error": "Could not revoke refresh token."},
                HttpStatus.INTERNAL_SERVER_ERROR_500.value,
            )


class TrialToken(Resource):
    """
    Trial api key creation resource.

    ---
    post:
      tags:
        - Authentication
      description: |
        Create a `trial` `api key`. Requires a valid `admin` `api key` for authentication.
        This trial api key lasts for `30 days`.
      security:
        - admin_api_key: []
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  trial_api_key:
                    type: string
                    example: myapikey
        400:
          description: Bad request.
        401:
          description: Missing authentication header.
    """

    @role_required([Role.ADMIN])
    def post(self):
        """Creates a trial api key."""

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

            response_body = {"trial_api_key": token}
            return make_response(response_body, HttpStatus.CREATED_201.value)

        except Exception:
            return (
                {"error": "Missing valid refresh token"},
                HttpStatus.BAD_REQUEST_400.value,
            )


class PermanentToken(Resource):
    """
    Permanent api key creation resource.

    ---
    post:
      tags:
        - Authentication
      description: |
        Create a `permanent` `api key`. Requires a valid `admin` `api key` for authentication.
      security:
        - admin_api_key: []
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  permanent_api_key:
                    type: string
                    example: myapikey
        400:
          description: Bad request.
        401:
          description: Missing authentication header.
    """

    @role_required([Role.ADMIN])
    def post(self):
        """Creates a permanent api key."""

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

            response_body = {"permanent_api_key": token}
            return make_response(response_body, HttpStatus.CREATED_201.value)

        except Exception:
            return (
                {"error": "Missing valid refresh token"},
                HttpStatus.BAD_REQUEST_400.value,
            )
