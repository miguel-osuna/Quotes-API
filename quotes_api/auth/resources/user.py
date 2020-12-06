from flask import request, jsonify, make_response, current_app as app
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    fresh_jwt_required,
    get_jwt_identity,
)
from flask_apispec import use_kwargs, marshal_with, doc
from flask_apispec.views import MethodResource

from quotes_api.models import User, TokenBlacklist
from quotes_api.extensions import pwd_context, jwt
from quotes_api.auth.helpers import (
    get_user_tokens,
    add_token_to_database,
)
from quotes_api.auth.decorators import user_required, admin_required
from quotes_api.common import HttpStatus, paginator
from quotes_api.schemas import UserSchema, UserResponseSchema


class UserSignup(MethodResource, Resource):
    """ User sign up resource. """

    # Decorators applied to all class methods
    method_decorators = []

    @doc(description="Registers a new user.", tags=["User"])
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


class UserLogin(MethodResource, Resource):
    """ User login resource. """

    # Decorators applied to all class methods
    method_decorators = []

    @doc(description="Login a user.", tags=["User"])
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

                if user is None:
                    raise Exception("User does not exist")

                # Check the passwords match
                if not pwd_context.verify(password, user.password):
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


class UserLogout(MethodResource, Resource):
    """ User logout resource. """

    # Decorators applied to all class methods
    method_decorators = []

    @doc(description="Logout a user.", tags=["User"])
    @fresh_jwt_required
    def post(self):
        pass


class UserResource(MethodResource, Resource):
    """ Single user resource. """

    # Decorators applied to all class methods
    method_decorators = []

    @doc(description="Get user resource by id.", tags=["User"])
    @admin_required
    def get(self, user_id):
        " Get user by id. "
        try:
            user = User.objects.get_or_404(id=user_id)

        except:
            return (
                {"error": "The requested URL was not found on the server."},
                HttpStatus.not_found_404.value,
            )

        response_body = {"user": user.to_dict()}

        return make_response(jsonify(response_body), HttpStatus.ok_200.value)

    @doc(description="Update user resource by id.", tags=["User"])
    @admin_required
    def put(self, user_id):
        """ Replace entire user. """
        try:
            user = User.objects.get_or_404(id=user_id)
        except:
            return {"error": "The requested URL was not found on the server."}

        try:
            data = request.get_json()
            user.update(**data)
            user.save()

            return "", HttpStatus.no_content_204.value

        except:
            return {"error": "Missing data."}, HttpStatus.bad_request_400.value

    @doc(description="Patch user resource by id.", tags=["User"])
    @admin_required
    def patch(self, user_id):
        """ Update user fields. """
        try:
            user = User.objects.get_or_404(id=user_id)

        except:
            return (
                {"error": "The requested URL was not found on the server."},
                HttpStatus.not_found_404.value,
            )

        try:
            data = request.get_json()
            user.update(**data)
            user.save()

            return "", HttpStatus.no_content_204.value

        except:
            return {"error": "Missing data."}, HttpStatus.bad_request_400.value

    @doc(description="Delete a user resource by id.", tags=["User"])
    @admin_required
    def delete(self, user_id):
        """ Delete user from the database. """

        try:
            user = User.objects.get_or_404(id=user_id)
        except:

            return (
                {"error": "The requested URL was not found on the server."},
                HttpStatus.not_found_404.value,
            )

        try:
            user.delete()
            return "", HttpStatus.no_content_204.value

        except:
            return (
                {"error": "Could not delete user"},
                HttpStatus.internal_server_error_500.value,
            )


class UserList(MethodResource, Resource):
    """ User list resource. """

    # Decorators applied to all class methods
    method_decorators = []

    @doc(description="Get list of user resources.", tags=["User"])
    @admin_required
    def get(self):

        args = request.args

        page = int(args.get("page", 1))
        per_page = int(args.get("per_page", 5))

        try:
            # Generating pagination of quotes
            pagination = User.objects.paginate(page=page, per_page=per_page)

            response_body = paginator(pagination, "auth.users")

            return make_response(jsonify(response_body), HttpStatus.ok_200.value)

        except:
            return (
                {"error": "Could not retrieve quotes"},
                HttpStatus.internal_server_error_500.value,
            )

