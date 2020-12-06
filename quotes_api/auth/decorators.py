""" Various custom decorators for role access. """

from functools import wraps

from flask import request, jsonify

from flask_jwt_extended import (
    verify_jwt_in_request,
    create_access_token,
    get_jwt_claims,
)

from quotes_api.extensions import jwt
from quotes_api.models import TokenBlacklist, User
from quotes_api.common import HttpStatus


def user_required(fn):
    """ 
    Custom decorator that verifies the user has a role of "basic" or "premium". 
    
    It also verifies that the JWT is present in the request. 
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        # First verify a valid access token was sent
        verify_jwt_in_request()

        # Get the user claims defined in decorator "user_claims_loader"
        claims = get_jwt_claims()
        roles = claims["roles"]

        if ("basic" in roles) or ("premium" in roles) or ("admin" in roles):
            return fn(*args, **kwargs)
        else:
            return {"error": "Access denied."}, HttpStatus.forbidden_403.value

    return wrapper


def admin_required(fn):
    """ 
    Custom decorator that verifies a user has a role of "admin. 
    
    It also verifies that the JWT is present in the request. 
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        # First verify a valid access token was sent
        verify_jwt_in_request()

        # Get the user claims defined in decorator "user_claims_loader"
        claims = get_jwt_claims()

        if "admin" in claims["roles"]:
            return fn(*args, **kwargs)
        else:
            return {"error": "Access denied."}, HttpStatus.forbidden_403.value

    return wrapper

