""" Various custom decorators for role access. """

from functools import wraps
from enum import Enum
from flask import request, jsonify
from flask_jwt_extended import (
    verify_jwt_in_request,
    create_access_token,
    get_jwt_claims,
)

from quotes_api.extensions import jwt
from quotes_api.models import TokenBlacklist, User
from quotes_api.common import HttpStatus


class Role(Enum):
    ADMIN = "admin"
    BASIC = "basic"


def role_required(role_list):
    """Custom decorator that verefies a list of possible roles for a user.

    It also verifies that the JWT is present in the request.
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # First verify a valid access token was sent
            verify_jwt_in_request()

            # Get the user claims defined in decorator "user_claims_loader"
            claims = get_jwt_claims()
            roles = claims["roles"]

            denied = False
            for role in roles:
                if Role(role) not in role_list:
                    denied = True
                    break

            if denied:
                return {"error": "Access denied."}, HttpStatus.forbidden_403.value
            else:
                return fn(*args, **kwargs)

        return wrapper

    return decorator
