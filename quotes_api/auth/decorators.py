"""Various custom decorators for role access."""

from functools import wraps
from enum import Enum

from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt,
)

from quotes_api.common import HttpStatus


class Role(Enum):
    """Role Enum Class"""

    ADMIN = "admin"
    BASIC = "basic"


def role_required(role_list):
    """Custom decorator that verefies a list of possible roles for a user.

    It also verifies that the JWT is present in the request.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # First verify a valid access token was sent
            verify_jwt_in_request()

            # Get the user claims defined in decorator "additional_claims_loader"
            claims = get_jwt()
            roles = claims["roles"]

            denied = False
            for role in roles:
                if Role(role) not in role_list:
                    denied = True

                if Role(role) in role_list:
                    denied = False
                    break

            if denied:
                return {"error": "Access denied."}, HttpStatus.FORBIDDEN_403.value

            return func(*args, **kwargs)

        return wrapper

    return decorator
