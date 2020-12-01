""" Various helpers for auth. Maily for token blacklisting. """

from datetime import datetime

from flask_jwt_extended import decode_token

from quotes_api.extensions import odm
from quotes_api.models import TokenBlacklist, User


def add_token_to_database(encoded_token, identity_claim):
    """ Adds a new token to the database. It is not revoked when it's added. """

    # Decode token to get its contents
    decoded_token = decode_token(encoded_token)

    # Decoded token variables
    jti = decoded_token.get("jti")
    token_type = decoded_token.get("type")
    user_identity = decoded_token.get(identity_claim)

    exp = decoded_token.get("exp", None)
    if exp != None:
        expires = datetime.fromtimestamp(exp)
    else:
        expires = None

    revoked = False

    # Get user document to add to the token blacklist
    user = User.objects.get(id=user_identity)

    db_token = TokenBlacklist(
        jti=jti, tokenType=token_type, user=user, expires=expires, revoked=revoked
    )
    db_token.save()


def is_token_revoked(decoded_token):
    """ Checks if the given token is revoked or not. 

    Because we are adding all the tokens (access and refresh), if the token is not present
    in the database, automatically it's going to be considered as "revoked", as we don't know
    its origin (where it was created).
    """

    jti = str(decoded_token["jti"])

    try:
        token = TokenBlacklist.objects.get(jti=jti)
        return token.revoked
    except:
        return True


def get_user_tokens(user_identity):
    """ Gets all the revoked and unrevoked tokens from a user. """
    try:
        pass
        user = User.objects.get(id=str(user_identity))
        tokens = TokenBlacklist.objects.filter(user=user)
        return tokens
    except:
        raise Exception(f"Could not find tokens for user with id {user_identity}")


def revoke_token(token_jti, user_identity):
    """ Revokes the given token.

    If no token is found we raise an exception.
    """
    try:
        # Get user by its id
        user = User.objects.get(id=user_identity)

    except:
        raise Exception(f"Could not find user with id {user_identity}")

    try:
        token = TokenBlacklist.objects.get(jti=token_jti, user=user)
        token.revoked = True
        token.save()

    except:
        raise Exception(f"Could not find token with jti {token_jti}")


def unrevoke_token(token_jti, user_identity):
    """ Unrevokes the given token. 

    If no token is found, we raise an exception.
    """
    try:
        # Get user by its id
        user = User.objects.get(id=user_identity)

    except:
        raise Exception(f"Could not find user with id {user_identity}")

    try:
        token = TokenBlacklist.objects.get(jti=token_jti, user=user)
        token.revoked = False
        token.save()

    except:
        raise Exception(f"Could not find token with jti {token_jti}")


def prune_database():
    """
    Delete tokens that have expired from the database. 

    How (and if) you call this function is entirely up to you. You could expose it to
    an endpoint that only administrators could call, you could run it as a cron, set it up with
    flask cli, etc. 
    """

    now = datetime.now()
    expired = TokenBlacklist.objects.filter(expires__lte=now)

    for token in expired:
        token.delete()

