"""User resource file."""

from flask import request, make_response, current_app as app
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
)

from quotes_api.auth.models import User
from quotes_api.extensions import pwd_context
from quotes_api.auth.helpers import (
    add_token_to_database,
)
from quotes_api.auth.decorators import Role, role_required
from quotes_api.common import HttpStatus, paginator
from quotes_api.auth.schemas import UserSchema


class UserSignup(Resource):
    """
    User sign up resource.

    ---
    post:
      tags:
        - Authentication
      description: |
        Register a `new user` into the platform.
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  required: true
                email:
                  type: string
                  required: true
                password:
                  type: string
                  required: true
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Successful sign up.
        400:
          description: Missing data.
        500:
          description: Could not sign up user.
    """

    # Decorators applied to all class methods
    method_decorators = []

    def post(self):
        """User registration to the database."""
        try:
            # Create user schema instance
            user_schema = UserSchema(only=["username", "email", "password"])
            data = user_schema.load(request.json)
            data["password"] = pwd_context.hash(data["password"])

            try:
                user = User(**data)
                user.save()

                return {"message": "Successful sign up."}, HttpStatus.CREATED_201.value

            except Exception:
                return (
                    {"error": "Could not sign up user."},
                    HttpStatus.INTERNAL_SERVER_ERROR_500.value,
                )

        except Exception:
            return (
                {"error": "Missing data."},
                HttpStatus.BAD_REQUEST_400.value,
            )


class UserLogin(Resource):
    """
    User login resource.

    ---
    post:
      tags:
        - Authentication
      description: |
        Login a `user`. Returns an `access_token` and `refresh_token`.
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  required: true
                password:
                  type: string
                  required: true
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                  refresh_token:
                    type: string
        400:
          description: Missing data.
        401:
          description: Wrong credentials.
    """

    # Decorators applied to all class methods
    method_decorators = []

    def post(self):
        """Authenticate a user and return tokens."""

        try:
            # Create user schema instance
            user_schema = UserSchema(only=["username", "password"])

            # Get data from request
            data = user_schema.load(request.json)
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
                access_token = create_access_token(
                    identity=user,
                    fresh=True,
                )
                refresh_token = create_refresh_token(identity=user)

                # Add new tokens to the database
                # JWT_IDENTITY_CLAIM is an identity claim and it defaults to "sub"
                add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
                add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])

                response_body = {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
                return make_response(response_body, HttpStatus.OK_200.value)

            except Exception:
                return (
                    {"error": "Wrong credentials."},
                    HttpStatus.UNAUTHORIZED_401.value,
                )

        except Exception:
            return {
                "error": "Missing data, could not login user."
            }, HttpStatus.BAD_REQUEST_400.value


class UserLogout(Resource):
    """User logout resource."""

    # Decorators applied to all class methods
    method_decorators = []

    @jwt_required(fresh=True)
    def post(self):
        """Logout a user."""


class UserResource(Resource):
    """
    Single user resource.

    ---
    get:
      tags:
        - User
      description: |
        Get `user` resource by id. Requires a valid `admin` `api key` for authentication.
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
                type: object
                properties:
                  user: UserSchema
        401:
          description: Missing authentication header.
        404:
          description: User does not exist.

    put:
      tags:
        - User
      description: |
        Update `user` resource by id. Requires a valid `admin` `api key` for authentication.
      security:
        - admin_api_key: []
      parameters:
        - in: path
          name: user_id
          required: true
          schema:
            type: string
          description: User ID.
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        204:
          description: The user resource was successfully updated.
        400:
          description: Missing data.
        401:
          description: Missing authentication header.
        404:
          description: User does not exist.

    patch:
      tags:
        - User
      description: |
        Patch `user` resource by id. Requires a valid `admin` `api key` for authentication.
      security:
        - admin_api_key: []
      parameters:
        - in: path
          name: user_id
          required: true
          schema:
            type: string
          description: User ID.
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        204:
          description: The user resource was successfully patched.
        400:
          description: Missing data.
        401:
          description: Missing authentication header.
        404:
          description: User does not exist.

    delete:
      tags:
        - User
      description: |
        Delete a `user` resource by id. Requires a valid `admin` `api key` for authentication.
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
        204:
          description: User resources were successfully deleted.
        401:
          description: Missing authentication header.
        404:
          description: User does not exist.
        500:
          description: Could not delete user.
    """

    # Decorators applied to all class methods
    method_decorators = []

    @role_required([Role.ADMIN])
    def get(self, user_id):
        """Get user by id."""
        try:
            user = User.objects.get_or_404(id=user_id)

        except Exception:
            return (
                {"error": "User does not exist."},
                HttpStatus.NOT_FOUND_404.value,
            )

        # Create user schema instance
        user_schema = UserSchema()
        return make_response(user_schema.dump(user), HttpStatus.OK_200.value)

    @role_required([Role.ADMIN])
    def put(self, user_id):
        """Replace entire user."""
        try:
            user = User.objects.get_or_404(id=user_id)

        except Exception:
            return (
                {"error": "User does not exist."},
                HttpStatus.NOT_FOUND_404.value,
            )

        try:
            # Create user schema instance
            user_schema = UserSchema()

            data = user_schema.load(request.json)
            user.update(**data)
            user.save()

            return "", HttpStatus.NO_CONTENT_204.value

        except Exception:
            return {"error": "Missing data."}, HttpStatus.BAD_REQUEST_400.value

    @role_required([Role.ADMIN])
    def patch(self, user_id):
        """Update user fields."""
        try:
            user = User.objects.get_or_404(id=user_id)

        except Exception:
            return (
                {"error": "User does not exist."},
                HttpStatus.NOT_FOUND_404.value,
            )

        try:
            # Create user schema instance and ignore any missing fields
            user_schema = UserSchema(partial=True)

            data = user_schema.load(request.json, partial=True)
            user.update(**data)
            user.save()

            return "", HttpStatus.NO_CONTENT_204.value

        except Exception:
            return {"error": "Missing data."}, HttpStatus.BAD_REQUEST_400.value

    @role_required([Role.ADMIN])
    def delete(self, user_id):
        """Delete user from the database."""

        try:
            user = User.objects.get_or_404(id=user_id)

        except Exception:
            return (
                {"error": "User does not exist."},
                HttpStatus.NOT_FOUND_404.value,
            )

        try:
            user.delete()
            return "", HttpStatus.NO_CONTENT_204.value

        except Exception:
            return (
                {"error": "Could not delete user"},
                HttpStatus.INTERNAL_SERVER_ERROR_500.value,
            )


class UserList(Resource):
    """
    User list resource.

    ---
    get:
      tags:
        - User
      description:
        Get list of `user` resources. Requires a valid `admin` `api key` for authentication.
      security:
        - admin_api_key: []
      parameters:
        - in: query
          name: page
          schema:
            type: integer
            default: 1
          description: Page number for pagination.
        - in: query
          name: per_page
          schema:
            type: integer
            default: 5
          description: Number of results per page.
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - type: object
                    properties:
                      meta:
                        $ref: '#/components/schemas/MetadataSchema'
                  - type: object
                    properties:
                      records:
                        type: array
                        items:
                          $ref: '#/components/schemas/UserSchema'

        401:
          description: Missing authentication header.
        500:
          description: Could not retrieve users.
    """

    # Decorators applied to all class methods
    method_decorators = []

    @role_required([Role.ADMIN])
    def get(self):
        """Get list of users."""
        args = request.args

        page = int(args.get("page", 1))
        per_page = int(args.get("per_page", 5))

        try:
            # Generating pagination of quotes
            pagination = User.objects.paginate(page=page, per_page=per_page)
            response_body = paginator(pagination, "auth.users", UserSchema)

            return make_response(response_body, HttpStatus.OK_200.value)

        except Exception:
            return (
                {"error": "Could not retrieve users."},
                HttpStatus.INTERNAL_SERVER_ERROR_500.value,
            )
