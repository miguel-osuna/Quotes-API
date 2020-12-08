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
from quotes_api.auth.schemas import TokenBlacklistSchema


class UserTokens(Resource):
    """ 
    User tokens list resource. 
    
    Provides a way for a user to look at their tokens

    ---
    get:
      tags: 
        - Authentication
      description: |
        Get list of token resources.
      parameters:
        - in: query
          name: page
          schema: 
            type: integer
            default: 1
          description: Page number for pagination
        - in: query
          name: per_page
          schema:
            type: integer
            default: 5
          description: Number of results per page
        - in: header
          name: Authorization
          required: true 
          description: Valid API Key
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/MetadataSchema'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/TokenBlacklistSchema'
    """

    # Decorators applied to all class methods
    method_decorators = []

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
    """ Token refresh. 
    
    ---
    post:
      tags:
        - Authentication
      description: |
        Create an access token from a refresh token.
      parameters:
        - in: header
          name: Authorization
          required: true
          description: Valid refresh token
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
          description: bad request
        401:
          description: unautorized
    """

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

            response_body = {"access_token": access_token}
            return make_response(response_body, HttpStatus.ok_200.value)

        except:
            return (
                {"error": "Missing valid refresh token"},
                HttpStatus.bad_request_400.value,
            )


class AccessTokenRevoke(Resource):
    """ Access Token Revoke resource. 
    
    ---
    delete:
      tags:
        - Authentication
      description: |
        Revoke an access token.
      parameters:
        - in: header
          name: Authorization
          required: true 
          description: Valid access token
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
          description: bad request
        401:
          description: unauthorized
    """

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
    """ Refresh Token Revoked resource. 
    
    ---
    delete:
      tags:
        - Authentication
      description: |
        Revokes a refresh token.
      parameters:
        - in: header
          name: Authorization
          required: true 
          description: Valid refresh token
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
          description: bad request
        401:
          description: unauthorized
    """

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
    """ Trial api key creation resource. 
    
    ---
    post:
      tags:
        - Authentication
      description: |
        Create a trial api key.
      parameters:
        - in: header
          name: Authorization
          required: true 
          description: Valid admin API Key
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
          description: bad request
        401:
          description: unauthorized
    """

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

            response_body = {"trial_api_key": token}
            return make_response(response_body, HttpStatus.created_201.value)

        except:
            return (
                {"error": "Missing valid refresh token"},
                HttpStatus.bad_request_400.value,
            )


class PermanentToken(Resource):
    """ Permanent api key creation resource. 
    
    ---
    post:
      tags:
        - Authentication
      description: |
        Create a permanent api key.
      parameters:
        - in: header
          name: Authorization
          required: true 
          description: Valid admin API Key
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
          description: bad request
        401:
          description: unauthorized
    """

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

            response_body = {"permanent_api_key": token}
            return make_response(response_body, HttpStatus.created_201.value)

        except:
            return (
                {"error": "Missing valid refresh token"},
                HttpStatus.bad_request_400.value,
            )

