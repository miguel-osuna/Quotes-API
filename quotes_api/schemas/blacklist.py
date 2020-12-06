from marshmallow import Schema, fields
from quotes_api.schemas import UserResponseSchema


class TokenBlacklistSchema(Schema):
    """ Token Blacklist Schema. """


class TokenBlacklistResponseSchema(Schema):
    """ Token Blacklist Response Schema. """

    id = fields.String()
    jti = fields.String()
    tokenType = fields.String()
    user = fields.Nested(UserResponseSchema)
    revoked = fields.Boolean()
    expires = fields.DateTime()

