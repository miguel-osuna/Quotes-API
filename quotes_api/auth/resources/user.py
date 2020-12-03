from flask import request, jsonify, make_response, current_app as app
from flask_restful import Resource


from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    fresh_jwt_required,
    get_jwt_identity,
)

from quotes_api.models import User
from quotes_api.extensions import pwd_context, jwt
from quotes_api.auth.helpers import (
    get_user_tokens,
    add_token_to_database,
)
from quotes_api.auth.decorators import user_required, admin_required
from quotes_api.common import HttpStatus


class UserSignup(Resource):
    """ User sign up resource. """

    # Decorators applied to all class methods
    method_decorators = []

    def post(self):
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


class UserLogin(Resource):
    """ User login resource. """

    # Decorators applied to all class methods
    method_decorators = []

    def post(self):
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

                response_body = {
                    "accessToken": access_token,
                    "refreshToken": refresh_token,
                }
                return make_response(jsonify(response_body), HttpStatus.ok_200.value)

            except:
                return (
                    {"error": "Wrong credentials"},
                    HttpStatus.unauthorized_401.value,
                )

        except:
            return {"error": "Missing data."}, HttpStatus.bad_request_400.value


class UserLogout(Resource):
    """ User logout resource. """

    # Decorators applied to all class methods
    method_decorators = []

    @fresh_jwt_required
    def post(self):
        pass


class UserResource(Resource):
    """ Single user resource. """

    # Decorators applied to all class methods
    method_decorators = []

    @admin_required
    def get(self):
        pass

    @admin_required
    def delete(self, user_id):
        pass


class UserList(Resource):
    """ User list resource. """

    # Decorators applied to all class methods
    method_decorators = []

    @admin_required
    def get(self):
        pass


class UserTokens(Resource):
    """ 
    User tokens list resource. 
    
    Provides a way for a user to look at their tokens
    """

    # Decorators applied to all class methods
    method_decorators = []

    @user_required
    def get(self):
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

