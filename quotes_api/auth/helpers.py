""" Various helpers for auth. Maily for token blacklisting. """

from datetime import datetime

from flask_jwt_extended import decode_token

from quotes_api.extensions import odm
from quotes_api.models import TokenBlacklist, User


def add_token_to_database(encoded_token, identity_claim):
    """ Adds a new token to the database. It is not revoked when it's added. """
    # Decode token to get its contents
    decoded_token = decode_token(encoded_token, allow_expired=False)

    # Unused variables: "iat", "nbf"

    # Decoded token variables
    jti = decoded_token["jti"]
    token_type = decoded_token["type"]
    expires = datetime.fromtimestamp(decoded_token["exp"])
    revoked = False
    user_identity = decoded_token[identity_claim]

    # Get user document to add to the token blacklist
    user = User.objects.get(id=user_identity)

    db_token = TokenBlacklist(
        jti=jti, tokenType=token_type, user=user, expires=expires, revoked=revoked
    )
    db_token.save()


def is_token_revoked(decoded_token):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present in the
    database, we are going to consider it revoked, as we don't know where it was
    created.
    """
    jti = decoded_token["jti"]

    try:
        token = TokenBlacklist.get(jti=jti)
        return token.revoked
    except:
        return True


def revoke_token(token_jti, user_identity):
    """ Revokes the given token.

    Since we use it only on logout that already requires a valid access token, 
    if token is not found we raise an exception.
    """
    try:
        # Get user by its id
        user = User.objects.get(id=user_identity)

    except:
        raise Exception("Could not find user with id {}".format(user_identity))

    try:
        token = TokenBlacklist.objects.get(jti=token_jti, user=user)
        token.revoked = True
        token.save()

    except:
        raise Exception("Couldn't find token with jti {}".format(token_jti))


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

