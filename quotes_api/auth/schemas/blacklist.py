from quotes_api.extensions import ma
from quotes_api.auth.schemas.user import UserSchema


class TokenBlacklistSchema(ma.Schema):
    """ Token Blacklist Schema. """

    id = ma.String()
    jti = ma.String()
    tokenType = ma.String()
    user = ma.Nested(UserSchema(only=["id",]))
    revoked = ma.Boolean()
    expires = ma.DateTime(allow_none=True, data_key="exp")
